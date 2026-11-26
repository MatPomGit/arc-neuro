"""Known-parameter recovery and fail-closed numerical checks."""
import unittest
import numpy as np
import pandas as pd
from scipy.special import expit
from mixed_models import _quadrature, logistic_ri, rt_mixed, switching_frame
from synthetic import synthetic


class MixedTests(unittest.TestCase):
    def test_quadrature_score(self):
        x=np.c_[np.ones(8),np.arange(8)/8]
        y=np.array([0,1,1,0,1,1,0,0])
        f=_quadrature(x,y,np.repeat([0,1],4),32)
        theta=np.array([.1,-.4,-.2])
        _,g=f(theta)
        for j in range(3):
            d=np.zeros(3);d[j]=1e-5
            self.assertAlmostEqual(g[j],(f(theta+d)[0]-f(theta-d)[0])/2e-5,places=6)

    def test_logistic_parameter_recovery(self):
        rng=np.random.default_rng(216)
        n,t=200,24
        groups=np.repeat(np.arange(n),t)
        gad=np.repeat(rng.normal(size=n),t)
        contrast=np.tile(np.linspace(-1,1,t),n)
        x=pd.DataFrame(dict(intercept=np.ones(n*t),gad5=gad,contrast=contrast))
        y=rng.binomial(1,expit(-.2-.55*gad+.6*contrast+np.repeat(rng.normal(0,.65,n),t)))
        fit=logistic_ri(y,x,groups,"gad5")
        self.assertAlmostEqual(fit["gad_effect"]["estimate"],-.55,delta=.22)
        self.assertAlmostEqual(fit["random_intercept_sd"],.65,delta=.25)
        self.assertLess(fit["gad_effect"]["ci95"][1],0)

    def test_rt_parameter_recovery(self):
        rng=np.random.default_rng(92)
        n,t=80,16
        groups=np.repeat(np.arange(n),t)
        gad=np.repeat(rng.normal(size=n),t)
        sw=np.tile(np.arange(t)%2,n)
        x=pd.DataFrame(dict(intercept=np.ones(n*t),gad5=gad,switch=sw,interaction=gad*sw))
        y=6.4+.12*sw+.04*gad*sw+np.repeat(rng.normal(0,.15,n),t)+sw*np.repeat(rng.normal(0,.08,n),t)+rng.normal(0,.1,n*t)
        fit=rt_mixed(pd.DataFrame(dict(participant_id=groups,outcome=y)),x,random_slope=True)
        self.assertAlmostEqual(fit["interaction"]["estimate"],.04,delta=.035)

    def test_constant_outcome_rejected(self):
        x=pd.DataFrame(dict(intercept=np.ones(60),gad5=np.arange(60)))
        with self.assertRaises(ValueError):
            logistic_ri(np.ones(60),x,np.arange(60),"gad5")

    def test_task_specific_filter(self):
        records=list(synthetic(17,35))
        r=next(t for t in records[0]["switching"] if t["mixed"] and t["transition"]=="switch")
        r.update(timeout=True,correct=False,rt_ms=None,focus_lost=False,technical_error=False)
        accuracy,*_=switching_frame(records,accuracy=True)
        rt,*_=switching_frame(records)
        self.assertGreater(len(accuracy),len(rt))
        self.assertTrue((accuracy["outcome"]==0).any())
        self.assertTrue(np.isfinite(rt["outcome"]).all())


if __name__=="__main__":
    unittest.main()
