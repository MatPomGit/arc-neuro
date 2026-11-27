# Marginal estimands for a five-category proportional odds model.
# Input draws must come from a validated joint bootstrap or sampling procedure.
marginal_surface <- function(eta, thresholds, random_sd) {
  stopifnot(is.matrix(eta), identical(dim(eta),c(4L,4L)),
            length(thresholds)==4L, all(diff(thresholds)>0),
            length(random_sd)==1L, is.finite(random_sd), random_sd>=0,
            all(is.finite(eta)), all(is.finite(thresholds)))
  matrix(vapply(as.vector(eta),function(e) {
    1+sum(vapply(thresholds,function(t) {
      if(random_sd==0) return(plogis(e-t))
      integrate(function(z) plogis(e+random_sd*z-t)*dnorm(z),
                -Inf,Inf,rel.tol=1e-8)$value
    },numeric(1)))
  },numeric(1)),4,4)
}
peak_contrasts <- function(surface) {
  stopifnot(identical(dim(surface),c(4L,4L)))
  result <- numeric()
  for(i in 2:3) for(j in 2:3) {
    x <- surface[i,j]-c(surface[i-1,j],surface[i+1,j],
                         surface[i,j-1],surface[i,j+1])
    names(x) <- paste(i,j,c("up","down","left","right"),sep="_")
    result <- c(result,x)
  }
  result
}
simultaneous_peaks <- function(estimate, bootstrap_surfaces, alpha=.05) {
  stopifnot(length(bootstrap_surfaces)>=200,alpha>0,alpha<1)
  theta <- peak_contrasts(estimate)
  draws <- t(vapply(bootstrap_surfaces,peak_contrasts,numeric(16)))
  se <- apply(draws,2,sd)
  stopifnot(all(is.finite(se)),all(se>0))
  centered <- sweep(draws,2,theta,"-")
  standardized <- sweep(centered,2,se,"/")
  critical <- as.numeric(quantile(apply(standardized,1,max),1-alpha))
  lower <- theta-critical*se
  list(contrasts=data.frame(estimate=theta,lower=lower),
       peaks=matrix(vapply(split(lower,rep(1:4,each=4)),function(x) all(x>0),logical(1)),2,2,byrow=TRUE),
       critical=critical)
}
