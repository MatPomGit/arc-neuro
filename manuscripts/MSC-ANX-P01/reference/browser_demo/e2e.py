"""Local Chromium E2E: no network or research records."""
import functools
import http.server
import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
import sys

from playwright.sync_api import sync_playwright, expect
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from export_demo import demo_manifest

HERE=Path(__file__).resolve().parent


class BrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(HERE))
        cls.server=http.server.ThreadingHTTPServer(("127.0.0.1",0),handler)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True)
        cls.thread.start()
        cls.playwright=sync_playwright().start()
        cls.browser=cls.playwright.chromium.launch(executable_path=os.environ["ANX_CHROME"],headless=True)
        cls.url=f"http://127.0.0.1:{cls.server.server_port}/"

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def setUp(self):
        self.context=self.browser.new_context(accept_downloads=True)
        self.page=self.context.new_page()
        self.errors=[]
        self.page.on("pageerror",lambda e:self.errors.append(str(e)))
        self.page.goto(self.url)
        self.page.bring_to_front()

    def tearDown(self):
        self.context.close()
        self.assertEqual(self.errors,[])

    def start(self,seed):
        data=demo_manifest(seed)
        self.page.locator("#manifest").set_input_files(
            {"name":"demo.json","mimeType":"application/json","buffer":json.dumps(data).encode()})
        expect(self.page.locator("#start")).to_be_enabled()
        self.page.locator("#start").click()
        self.page.locator("#resume").click()
        return data

    def export(self):
        self.page.locator("#stop").click()
        with self.page.expect_download() as info:
            self.page.locator("#export").click()
        return json.loads(info.value.path().read_text())

    def test_decision_quiz_and_export(self):
        self.start(42)
        expect(self.page.locator("#quiz")).to_be_visible()
        self.page.locator("#quiz-submit").click()
        expect(self.page.locator("#quiz-feedback")).to_contain_text("Sprawdź")
        for field,value in (("q1","known"),("q2","unknown"),("q3","higher")):
            self.page.locator("#"+field).select_option(value)
        self.page.locator("#quiz-submit").click()
        self.page.locator("#resume").click()
        expect(self.page.locator("#left")).to_contain_text("pkt")
        self.page.keyboard.press("f")
        expect(self.page.locator("#bar")).to_have_attribute("value","1")
        result=self.export()
        self.assertEqual(result["data_origin"],"demonstration")
        self.assertEqual(result["completed_trials"],1)
        self.assertTrue(result["comprehension_passed"])
        self.assertEqual(result["comprehension_attempts"],2)
        self.assertEqual(result["trials"][0]["response"],"left")

    def test_failed_comprehension_skips_decisions(self):
        self.start(42)
        self.page.locator("#quiz-submit").click()
        self.page.locator("#quiz-submit").click()
        expect(self.page.locator("#instruction")).to_contain_text("Pominięto")
        self.page.locator("#resume").click()
        expect(self.page.locator("#progress")).to_contain_text("Trening 1")
        result=self.export()
        self.assertEqual(len(result["skipped_trials"]),96)
        self.assertEqual(result["comprehension_attempts"],2)
        self.assertFalse(result["comprehension_passed"])
        self.assertEqual(result["completed_trials"],0)

    def test_two_failed_practices_preserve_decisions(self):
        data=self.start(0)
        # This test checks practice gating, not physical timing. A delayed
        # cue or key event may invalidate a trial and pause on a busy runner.
        # Resume only after verifying the explicit invalidation and progress.
        invalid=0
        for attempt in (1,2):
            i=0
            while i<24:
                row=data["practice"][attempt-1][i]
                progress=f"Trening {attempt}: {i+1} / 24"
                self.page.wait_for_function(
                    """({progress,stimulus}) => {
                        const resume=document.querySelector('#resume');
                        return !resume.hidden || (
                            document.querySelector('#progress').textContent===progress &&
                            document.querySelector('#stimulus').textContent===stimulus
                        );
                    }""",arg={"progress":progress,"stimulus":str(row["stimulus"])})
                if self.page.locator("#resume").is_visible():
                    instruction=self.page.locator("#instruction").inner_text()
                    if i==23 and ("Powtórz trening" in instruction if attempt==1 else "Pominięto" in instruction):
                        # A technical failure on the final trial can complete
                        # the attempt without the intermediate invalidation UI.
                        invalid+=1
                        i+=1
                        break
                    self.assertIn("Próba treningowa nieważna",instruction)
                    actual=self.page.locator("#progress").inner_text()
                    if actual==progress and i>0:
                        # The previous key event was technically invalid.
                        pass
                    elif i<23 and actual==f"Trening {attempt}: {i+2} / 24":
                        # The current cue was invalid before presentation.
                        i+=1
                    else:
                        self.fail(f"Unexpected progress after invalidation: {actual}")
                    invalid+=1
                    self.page.locator("#resume").click()
                    continue
                expect(self.page.locator("#progress")).to_have_text(progress)
                self.page.keyboard.press("f" if row["correct_key"] else "j")
                i+=1
            expect(self.page.locator("#resume")).to_be_visible()
            expect(self.page.locator("#instruction")).to_contain_text(
                "Powtórz trening" if attempt==1 else "Pominięto")
            if attempt==1:
                self.page.locator("#resume").click()
        self.assertLessEqual(invalid,2,"Excessive technical timing failures on CI runner")
        expect(self.page.locator("#instruction")).to_contain_text("Pominięto")
        self.page.locator("#resume").click()
        expect(self.page.locator("#quiz")).to_be_visible()
        report=self.export()
        self.assertEqual(len(report["skipped_trials"]),240)
        self.assertEqual(len(report["practice_history"]),2)
        self.assertEqual([x["correct"] for x in report["practice_history"]],[0,0])
        self.assertEqual([x["total"] for x in report["practice_history"]],[24,24])
        self.assertFalse(report["training_passed"])
        self.assertEqual(report["completed_trials"],0)

    def test_held_keys_do_not_leak_into_next_trial(self):
        self.start(42)
        for field,value in (("q1","known"),("q2","unknown"),("q3","higher")):
            self.page.locator("#"+field).select_option(value)
        self.page.locator("#quiz-submit").click()
        self.page.locator("#resume").click()
        expect(self.page.locator("#left")).to_contain_text("pkt")
        self.page.keyboard.down("f")
        self.page.keyboard.down("j")
        self.page.keyboard.up("f")
        expect(self.page.locator("#resume")).to_be_visible()
        self.page.locator("#resume").click()
        expect(self.page.locator("#resume")).to_be_visible()
        self.page.keyboard.up("j")
        self.page.locator("#resume").click()
        expect(self.page.locator("#left")).to_contain_text("pkt")
        self.page.keyboard.press("j")
        expect(self.page.locator("#bar")).to_have_attribute("value","2")
        report=self.export()
        self.assertEqual([x["response"] for x in report["trials"]],["left","right"])

    def test_focus_during_cue_and_iti(self):
        self.start(0)
        expect(self.page.locator("#cue")).not_to_have_text("")
        self.page.evaluate("window.dispatchEvent(new Event('blur'))")
        expect(self.page.locator("#resume")).to_be_visible()
        self.page.locator("#resume").click()
        expect(self.page.locator("#progress")).to_contain_text("2 / 24")
        expect(self.page.locator("#stimulus")).not_to_have_text("")
        self.page.keyboard.press("f")
        self.page.evaluate("window.dispatchEvent(new Event('blur'))")
        expect(self.page.locator("#resume")).to_be_visible()
        self.page.wait_for_timeout(650)
        expect(self.page.locator("#progress")).to_contain_text("3 / 24")
        report=self.export()
        self.assertEqual(report["incomplete_practice_trials"],2)
        self.assertEqual(report["completed_trials"],0)

    def test_training_then_main_and_timing(self):
        data=self.start(0)
        expect(self.page.locator("#progress")).to_contain_text("Trening 1")
        for i,row in enumerate(data["practice"][0]):
            expect(self.page.locator("#progress")).to_contain_text(f"{i+1} / 24")
            expect(self.page.locator("#stimulus")).to_have_text(str(row["stimulus"]))
            self.page.wait_for_timeout(175)
            self.page.keyboard.press("j" if row["correct_key"] else "f")
        expect(self.page.locator("#resume")).to_be_visible()
        expect(self.page.locator("#instruction")).to_contain_text("Trening zaliczony")
        self.page.locator("#resume").click()
        expect(self.page.locator("#stimulus")).to_have_text(str(data["switching"][0]["stimulus"]))
        self.page.wait_for_timeout(175)
        self.page.keyboard.press("j" if data["switching"][0]["correct_key"] else "f")
        expect(self.page.locator("#bar")).to_have_attribute("value","1")
        result=self.export()
        self.assertTrue(result["training_passed"])
        self.assertEqual(result["practice_history"][0]["correct"],24)
        self.assertEqual(result["completed_trials"],1)
        self.assertFalse(result["trials"][0].get("practice",False))
        self.assertGreaterEqual(result["trials"][0]["rt_ms"],150)
        self.assertGreaterEqual(len(result["timing_diagnostics"]),25)

    def test_focus_interruption(self):
        self.start(0)
        expect(self.page.locator("#stimulus")).not_to_have_text("")
        self.page.evaluate("window.dispatchEvent(new Event('blur'))")
        expect(self.page.locator("#resume")).to_be_visible()
        expect(self.page.locator("#instruction")).to_contain_text("nieważna")
        result=self.export()
        self.assertEqual(result["completed_trials"],0)
        self.assertEqual(result["incomplete_practice_trials"],1)


if __name__=="__main__":
    unittest.main()
