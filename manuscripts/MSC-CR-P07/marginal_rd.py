"""Marginal risk difference for eligible wrong-advice trials.

Independent participant clusters; inference conditional on the fixed task bank.
Equal probability tone assignment, no carryover and MCAR observation assumed.
"""
import numpy as np
from scipy.stats import t


def estimate_rd(person, tone, outcome):
    """Trial-weighted Hajek contrast with participant-cluster sandwich CI."""
    p, a, y = map(np.asarray, (person, tone, outcome))
    if any(v.ndim != 1 for v in (p, a, y)) or not len(p) == len(a) == len(y):
        raise ValueError("Expected aligned vectors")
    if not np.isin(a, [0, 1]).all() or not np.isin(y, [0, 1]).all():
        raise ValueError("Expected binary treatment and outcome")
    groups, ix = np.unique(p, return_inverse=True)
    g = len(groups)
    n1, n0 = int(a.sum()), int((1-a).sum())
    if g < 3 or min(n1, n0) == 0:
        return None
    r1, r0 = y[a == 1].mean(), y[a == 0].mean()
    rd = float(r1-r0)
    influence = a*(y-r1)/n1 - (1-a)*(y-r0)/n0
    scores = np.bincount(ix, weights=influence, minlength=g)
    se = float(np.sqrt(g/(g-1)*np.sum(scores**2)))
    if not np.isfinite(se) or se <= 0:
        return None
    q = float(t.ppf(.975, g-1))
    return dict(rd=rd, se=se, lower=rd-q*se, upper=rd+q*se,
                clusters=g, n1=n1, n0=n0)
