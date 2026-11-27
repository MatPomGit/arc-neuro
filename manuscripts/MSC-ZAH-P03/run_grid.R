# Run from manuscript directory. Requires ordinal.
args <- commandArgs(trailingOnly=TRUE)
B <- if(length(args)) as.integer(args[1]) else 100L
stopifnot(is.finite(B),B>=1)
grid <- expand.grid(n=c(40,80,120,200),k=c(16,24,40))
for(i in seq_len(nrow(grid))) {
  n <- grid$n[i]; k <- grid$k[i]
  target <- sprintf("results/power_n%d_k%d_b%d.csv",n,k,B)
  if(file.exists(target)) stop("Existing output: ",target,"; archive before rerunning")
  status <- system2(file.path(R.home("bin"),"Rscript"),c("simulate_power.R",n,k,B))
  if(status!=0 || !file.exists(target)) stop("Simulation failed: ",target)
}
