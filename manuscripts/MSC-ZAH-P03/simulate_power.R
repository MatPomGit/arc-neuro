library(ordinal)
args <- commandArgs(trailingOnly=TRUE)
n <- if(length(args)>0) as.integer(args[1]) else 80L
k <- if(length(args)>1) as.integer(args[2]) else 24L
B <- if(length(args)>2) as.integer(args[3]) else 100L
stopifnot(n>=16,k>=8,k%%4==0,B>=1)
set.seed(20261127)
one <- function(beta,missing=.05) {
  d <- expand.grid(clip=seq_len(k),person=seq_len(n))
  d$direction <- as.integer(d$clip>k/2)
  d$violation <- (d$clip+d$person)%%2
  d$avatar <- (d$clip-1)%%4+1
  eta <- .3*d$direction+.3*d$violation+beta*d$direction*d$violation+
    rnorm(n,0,.7)[d$person]+rnorm(k,0,.5)[d$clip]+
    rnorm(4,0,.4)[d$avatar]+rlogis(nrow(d))
  d$y <- ordered(cut(eta,c(-Inf,-1.5,-.5,.5,1.5,Inf),labels=FALSE))
  d <- d[runif(nrow(d))>=missing,]
  for(v in c("person","clip","avatar")) d[[v]] <- factor(d[[v]])
  tryCatch({
    m0 <- clmm(y~direction+violation+(1|person)+(1|clip)+(1|avatar),data=d,Hess=TRUE)
    m1 <- clmm(y~direction*violation+(1|person)+(1|clip)+(1|avatar),data=d,Hess=TRUE)
    ok <- function(m) !is.null(m$gradient) && all(is.finite(m$gradient)) &&
      max(abs(m$gradient))<.001 && all(is.finite(m$Hessian)) &&
      min(eigen(m$Hessian,symmetric=TRUE,only.values=TRUE)$values)>0
    if(!ok(m0)||!ok(m1)) return(NA_real_)
    lr <- 2*(as.numeric(logLik(m1))-as.numeric(logLik(m0)))
    if(!is.finite(lr)||lr< -1e-6) return(NA_real_)
    pchisq(max(0,lr),1,lower.tail=FALSE)
  },error=function(e) NA_real_)
}
out <- do.call(rbind,lapply(c(0,.25,.5,.75),function(beta){
  p <- replicate(B,one(beta))
  valid <- sum(!is.na(p)); hits <- sum(p<.05,na.rm=TRUE)
  rate <- if(valid>0) hits/valid else NA_real_
  data.frame(n=n,clips=k,beta=beta,reps=B,valid=valid,rate=rate,
             mcse=if(valid>0) sqrt(rate*(1-rate)/valid) else NA_real_,
             lower=hits/B,upper=(hits+B-valid)/B)
}))
dir.create("results",showWarnings=FALSE)
write.csv(out,sprintf("results/power_n%d_k%d_b%d.csv",n,k,B),row.names=FALSE)
print(out)
