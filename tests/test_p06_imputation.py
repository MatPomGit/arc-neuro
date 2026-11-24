"""Synthetic tests for the reference chained-equations PMM implementation."""
import sys
import random
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"papers/cognition/MSC-CR-P06/materials"))
import imputation as p
import analysis as a
sys.path.pop(0)


def fixture():
    rng=random.Random(12)
    rows=[]
    for arm in (0,1):
        for st in (0,1):
            for seq in a.SEQUENCES:
                for k in range(5):
                    row=dict(participant_id=f"synthetic-{len(rows)}",arm=arm,stratum=st,sequence=seq)
                    for field in p.FIELDS:
                        row[field]=rng.uniform(.1,.8)+(0.5 if field.startswith("justification") else 0)
                    rows.append(row)
    for i,row in enumerate(rows):
        if i%7==0:
            row["accuracy_T1"]=None
        if i%11==0:
            row["brier_T0"]=None
    return rows


class P06ImputationTests(unittest.TestCase):
    def test_donor_support_and_observed_values(self):
        rows=fixture()
        result=p.generate_imputations(rows,m=3,iterations=3,seed=4)
        self.assertEqual(len(result["datasets"]),3)
        self.assertEqual(len(result["traces"][0]),3)
        for ds in result["datasets"]:
            a._align(a.validate(rows),ds)
            for old,new in zip(rows,ds):
                for field in p.FIELDS:
                    if old[field] is None:
                        self.assertIn(new[field],{r[field] for r in rows if r["arm"]==old["arm"] and r[field] is not None})
        pooled=a.analyze_imputations(rows,result["datasets"],expected_m=3)
        self.assertEqual(pooled["H1"]["n_used"],120)
        self.assertIsNone(rows[0]["accuracy_T1"])

    def test_reproducibility_and_stochasticity(self):
        rows=fixture()
        x=p.generate_imputations(rows,m=3,iterations=3,seed=12)
        y=p.generate_imputations(rows,m=3,iterations=3,seed=12)
        self.assertEqual(x,y)
        self.assertNotEqual(x["datasets"][0],x["datasets"][1])
        self.assertNotEqual(x["datasets"],p.generate_imputations(rows,m=3,iterations=3,seed=13)["datasets"])

    def test_complete_inputs(self):
        rows=fixture()
        for row in rows:
            for f in p.FIELDS:
                if row[f] is None:
                    row[f]=.5
        result=p.generate_imputations(rows,m=2,iterations=1)
        self.assertEqual(result["datasets"],[rows,rows])
        self.assertEqual(result["traces"],[[{}],[{}]])

    def test_fail_closed_sparse(self):
        rows=fixture()
        for row in rows:
            if row["arm"]==1:
                row["accuracy_T1"]=None
        with self.assertRaises(ValueError):
            p.generate_imputations(rows,m=2,iterations=1)
        with self.assertRaises(ValueError):
            p.generate_imputations(fixture(),m=1)


if __name__=="__main__":
    unittest.main()
