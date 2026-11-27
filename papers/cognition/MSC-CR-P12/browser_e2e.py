"""Exercise the four prototype phases and download in local Chromium."""
import functools
import http.server
import json
import os
from pathlib import Path
import shutil
import tempfile
import threading

from playwright.sync_api import expect, sync_playwright

from materials import bank


def main():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        shutil.copyfile(Path(__file__).with_name("demo.html"), root / "demo.html")
        (root / "items.json").write_text(json.dumps(bank(), ensure_ascii=False), encoding="utf-8")
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=directory)
        with http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler) as server:
            worker = threading.Thread(target=server.serve_forever, daemon=True)
            worker.start()
            try:
                with sync_playwright() as playwright:
                    browser = playwright.chromium.launch(executable_path=os.environ["ANX_CHROME"])
                    page = browser.new_page(accept_downloads=True)
                    errors = []
                    page.on("pageerror", lambda error: errors.append(str(error)))
                    page.goto(f"http://127.0.0.1:{server.server_port}/demo.html")
                    page.get_by_role("button", name="Rozpocznij demonstrację").click()
                    for phase in (0, 1, 2, 3):
                        for _ in range(2 if phase == 1 else 6):
                            page.get_by_label("Wybór początkowy").select_option("1")
                            page.get_by_role("button", name="Pokaż rekomendację").click()
                            page.get_by_label("Pewność trafności tej decyzji").select_option("4")
                            page.get_by_role("button", name="Zatwierdź").click()
                            if phase == 1:
                                page.get_by_role("button", name="Dalej").click()
                    expect(page.get_by_role("heading", name="Sesja zakończona")).to_be_visible()
                    with page.expect_download() as result:
                        page.get_by_role("button", name="Pobierz dane demonstracyjne").click()
                    rows = json.loads(result.value.path().read_text())
                    assert len(rows) == len({row["id"] for row in rows}) == 20
                    assert [sum(row["phase"] == phase for row in rows) for phase in range(4)] == [6, 2, 6, 6]
                    assert all(row["initial"] == 1 and row["confidence"] == 0.9 for row in rows)
                    assert not errors, errors
                    browser.close()
            finally:
                server.shutdown()
                worker.join()
    print("PASS: Chromium prototype and export")


if __name__ == "__main__":
    main()
