import numpy as np
from scipy.special import expit
from scipy.integrate import quad
from scipy.stats import norm

def marginal_surface(eta, thresholds, random_sd):
    eta, t = np.asarray(eta, float), np.asarray(thresholds, float)
    if eta.shape != (4,4) or t.shape != (4,) or not np.isfinite(eta).all() or not np.isfinite(t).all() or not np.all(np.diff(t)>0) or not np.isfinite(random_sd) or random_sd<0:
        raise ValueError("Invalid surface parameters")
    return np.array([1+sum(expit(e-x) if random_sd==0 else quad(lambda z: expit(e+random_sd*z-x)*norm.pdf(z), -np.inf,np.inf,epsabs=1e-9)[0] for x in t) for e in eta.flat]).reshape(4,4)

def peak_contrasts(surface):
    s=np.asarray(surface,float)
    if s.shape!=(4,4) or not np.isfinite(s).all():
        raise ValueError("Invalid surface")
    return np.array([s[i,j]-s[u,v] for i in (1,2) for j in (1,2) for u,v in ((i-1,j),(i+1,j),(i,j-1),(i,j+1))])

def simultaneous_peaks(estimate, bootstrap_surfaces, alpha=.05):
    theta=peak_contrasts(estimate)
    draws=np.array([peak_contrasts(s) for s in bootstrap_surfaces])
    if len(draws)<200 or not 0<alpha<1:
        raise ValueError("Invalid bootstrap")
    se=draws.std(axis=0,ddof=1)
    if not np.all(np.isfinite(se)&(se>0)):
        raise ValueError("Degenerate bootstrap")
    critical=np.quantile(((draws-theta)/se).max(axis=1),1-alpha)
    lower=theta-critical*se
    return dict(estimate=theta,lower=lower,peaks=(lower.reshape(2,2,4)>0).all(axis=2),critical=critical)
