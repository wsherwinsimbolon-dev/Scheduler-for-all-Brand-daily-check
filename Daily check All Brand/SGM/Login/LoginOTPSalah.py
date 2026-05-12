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
        sgm.tombolOTPclick()
        page.wait_for_timeout(5000)

        #Input nomor HP
        sgm.kolomHP("082281116519")
        page.wait_for_timeout(5000)

        #Button masuk melalui OTP
        sgm.buttonClickMasukOTP()
        page.wait_for_timeout(5000)

        #masukan nomor otp
        sgm.inputMasukinOTPboxes("123456")
        page.wait_for_timeout(5000)

        #Click button Kirim OTP
        sgm.buttonClickOTPSekarang()
        page.wait_for_timeout(5000)
        page.screenshot(path="LoginwithOTPsalah.png")

        browser.close()

if __name__ == "__main__":
    login()