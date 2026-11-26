# Prospective planning only. Requires R and lme4; no participant data.
# Run: Rscript power_simulation.R [replicates] [seed]
simulate_trials <- function(n, tasks, alpha, beta, sd_person, sd_task,
                            initial_correct, missing = 0) {
  stopifnot(n >= 2, tasks >= 4, tasks %% 4 == 0,
            initial_correct > 0, initial_correct <= 1,
            missing >= 0, missing < 1, sd_person >= 0, sd_task >= 0)
  d <- expand.grid(task = seq_len(tasks), person = seq_len(n))
  # Balanced 2x2 allocation within each person, independent of initial choice.
  condition <- unlist(lapply(seq_len(n), function(i)
    sample(rep(0:3, each = tasks / 4))))
  d$tone <- condition %% 2L
  d$wrong <- condition %/% 2L
  d$initial <- rbinom(nrow(d), 1, initial_correct)
  u <- rnorm(n, 0, sd_person)
  v <- rnorm(tasks, 0, sd_task)
  d$y <- rbinom(nrow(d), 1,
                plogis(alpha + beta * d$tone + u[d$person] + v[d$task]))
  observed <- runif(nrow(d)) >= missing
  d <- d[d$wrong == 1 & d$initial == 1 & observed, ]
  d$person <- factor(d$person)
  d$task <- factor(d$task)
  d
}

fit_trial <- function(d) {
  if (nrow(d) == 0 || length(unique(d$tone)) < 2 ||
      length(unique(d$y)) < 2 || nlevels(d$person) < 2 || nlevels(d$task) < 2)
    return("failed")
  fit <- tryCatch(suppressWarnings(suppressMessages(
    lme4::glmer(y ~ tone + (1 | person) + (1 | task), data = d,
                family = binomial, nAGQ = 1))),
    error = function(e) NULL)
  if (is.null(fit) || lme4::isSingular(fit) ||
      !is.null(fit@optinfo$conv$lme4$messages) ||
      !isTRUE(fit@optinfo$conv$opt == 0))
    return("failed")
  co <- coef(summary(fit))
  p <- co["tone", "Pr(>|z|)"]
  if (!is.finite(p)) return("failed")
  if (p < .05) "reject" else "retain"
}

scenario <- function(n, tasks, alpha, beta, sd_person, sd_task,
                     initial_correct, missing, replicates, seed) {
  stopifnot(replicates >= 1)
  set.seed(seed)
  outcomes <- replicate(replicates, fit_trial(simulate_trials(
    n, tasks, alpha, beta, sd_person, sd_task, initial_correct, missing)))
  rejected <- sum(outcomes == "reject")
  failed <- sum(outcomes == "failed")
  valid <- replicates - failed
  # Treat failed fits as non-rejections for conservative planning.
  ci <- binom.test(rejected, replicates)$conf.int
  data.frame(n, tasks, alpha, beta, sd_person, sd_task, initial_correct,
             missing, replicates, seed, rejected, failed,
             rejection_rate = rejected / replicates,
             lower95 = ci[1], upper95 = ci[2],
             conditional_rate = if (valid) rejected / valid else NA_real_)
}

main <- function() {
  if (!requireNamespace("lme4", quietly = TRUE)) stop("Install lme4 in an isolated R environment.")
  args <- commandArgs(trailingOnly = TRUE)
  reps <- if (length(args)) as.integer(args[1]) else 200L
  seed <- if (length(args) > 1) as.integer(args[2]) else 20261126L
  stopifnot(!is.na(reps), reps >= 1, !is.na(seed), seed >= 0)
  # Illustrative grid, not pilot estimates or a recruitment recommendation.
  grid <- expand.grid(n = c(80, 160, 240), beta = c(0, log(1.3), log(1.6)),
                      initial_correct = c(.55, .75), sd_person = c(.5, 1),
                      sd_task = c(.3, .7), missing = c(0, .1))
  result <- do.call(rbind, lapply(seq_len(nrow(grid)), function(i) {
    g <- grid[i, ]
    scenario(g$n, 24L, qlogis(.2), g$beta, g$sd_person, g$sd_task,
             g$initial_correct, g$missing, reps, seed)
  }))
  write.csv(result, stdout(), row.names = FALSE)
}

if (sys.nframe() == 0L) main()
