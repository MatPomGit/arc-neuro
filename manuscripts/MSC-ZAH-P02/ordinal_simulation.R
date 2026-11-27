# Synthetic sensitivity analysis; no empirical data.
# Dependencies: ordinal
library(ordinal)
args <- commandArgs(trailingOnly=TRUE)
n <- if(length(args)>=1) as.integer(args[1]) else 80L
reps <- if(length(args)>=2) as.integer(args[2]) else 100L
stopifnot(is.finite(n), n>=16, is.finite(reps), reps>=1)
set.seed(20261127)
one <- function(effect, scenario) {
  d <- expand.grid(A=1:4,B=1:4,person=seq_len(n))
  # Each participant sees every cell, with randomized source and avatar.
  d$source <- unlist(lapply(seq_len(n),function(i) sample(1:24,16)))
  d$avatar <- sample(1:8,nrow(d),replace=TRUE)
  a <- (d$A-2.5)/1.5; b <- (d$B-2.5)/1.5
  mu <- switch(scenario,null=0,additive=effect*(a+b),
               interaction=effect*a*b,
               peak=effect*exp(-((a-1/3)^2+(b+1/3)^2)/.2))
  eta <- mu+rnorm(n,0,.7)[d$person]+rnorm(24,0,.5)[d$source]+
    rnorm(8,0,.4)[d$avatar]+rlogis(nrow(d))
  d$y <- ordered(cut(eta,c(-Inf,-1.5,-.5,.5,1.5,Inf),labels=FALSE))
  for(k in c("A","B","person","source","avatar")) d[[k]] <- factor(d[[k]])
  tryCatch({
    m0 <- clmm(y~A+B+(1|person)+(1|source)+(1|avatar),data=d,Hess=TRUE)
    m1 <- clmm(y~A*B+(1|person)+(1|source)+(1|avatar),data=d,Hess=TRUE)
    ok <- function(m) {
      g <- m$gradient
      !is.null(g) && all(is.finite(g)) && max(abs(g))<.001 &&
        all(is.finite(m$Hessian)) && min(eigen(m$Hessian,symmetric=TRUE,only.values=TRUE)$values)>0
    }
    if(!ok(m0)||!ok(m1)) return(NA_real_)
    lr <- 2*(as.numeric(logLik(m1))-as.numeric(logLik(m0)))
    if(!is.finite(lr)||lr< -1e-6) return(NA_real_)
    pchisq(max(0,lr),9,lower.tail=FALSE)
  },error=function(e) NA_real_)
}
rows <- do.call(rbind,lapply(c("null","additive","interaction","peak"),function(s) {
  p <- replicate(reps,one(.5,s))
  data.frame(scenario=s,n=n,reps=reps,valid=sum(!is.na(p)),
    rejected=sum(p<.05,na.rm=TRUE),
    rate=if(all(is.na(p))) NA_real_ else mean(p<.05,na.rm=TRUE),
    lower_bound=sum(p<.05,na.rm=TRUE)/reps,
    upper_bound=(sum(p<.05,na.rm=TRUE)+sum(is.na(p)))/reps)
}))
dir.create("results",showWarnings=FALSE)
write.csv(rows,"results/ordinal_power.csv",row.names=FALSE)
print(rows)
