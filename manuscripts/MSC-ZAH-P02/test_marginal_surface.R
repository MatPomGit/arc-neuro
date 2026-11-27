source("marginal_surface.R")
t <- c(-1.5,-.5,.5,1.5)
s <- marginal_surface(matrix(0,4,4),t,1)
stopifnot(max(abs(s-3))<1e-7)
stopifnot(all(abs(peak_contrasts(s))<1e-7))
s[2,2] <- 4
stopifnot(all(peak_contrasts(s)[1:4]>0))
stopifnot(all(marginal_surface(matrix(2,4,4),t,0)>3))
cat("Deterministic marginal estimand tests passed\n")
