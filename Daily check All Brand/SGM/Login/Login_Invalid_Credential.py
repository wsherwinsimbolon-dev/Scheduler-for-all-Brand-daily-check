"""
==============================================
  PLAYWRIGHT PYTHON - LOGIN BASIC
  Install dulu: pip install playwright
                playwright install chromium
==============================================
"""

from playwright.sync_api import sync_playwright
from Locator_Login import LoginSGM
import os
HEADLESS = os.environ.get("CI", "").lower() == "true"

# ─────────────────────────────────────────
# FUNGSI UTAMA
# ─────────────────────────────────────────
def login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()

        # Buat objek dulu, url & goto sudah otomatis di dalam __init__
        sgm = LoginSGM(page)
        print(f"✓ Membuka: {sgm.url}")
        page.wait_for_timeout(5000)

        #Input Username
        sgm.noHP("0822811165199")
        page.wait_for_timeout(5000)

        #Input Password
        sgm.pasWort("Tes12345!")
        page.wait_for_timeout(5000)

        #button Masuk
        sgm.tombolMasuk()
        page.wait_for_timeout(5000)
        #screenshoot
        page.screenshot(path="gagal_login_salahnomor.png")

        browser.close()

if __name__ == "__main__":
    login()