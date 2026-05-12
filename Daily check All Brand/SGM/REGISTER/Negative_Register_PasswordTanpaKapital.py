"""
==============================================
  PLAYWRIGHT PYTHON - NEGATIVE TEST REGISTER
  Skenario: Register dengan password tanpa huruf kapital (No Capital)
  Catatan: Site tidak mensyaratkan huruf kapital — password diterima,
           tidak ada warning password yang muncul.
==============================================
"""

from playwright.sync_api import sync_playwright
from Locator_Register import RegisterSGM
import os
HEADLESS = os.environ.get("CI", "").lower() == "true"


def test_register_password_tanpa_kapital():
    print("\n[SKENARIO] Register dengan password tanpa huruf kapital")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()

        sgm = RegisterSGM(page)
        print(f"✓ Membuka: {sgm.url}")
        page.wait_for_timeout(3000)

        sgm.inputNamaPertama("Sherwin")
        page.wait_for_timeout(1000)

        sgm.InputnoHP("082281116519")
        page.wait_for_timeout(1000)

        # Password tanpa huruf kapital (semua huruf kecil)
        sgm.Inputpassword("test1234!")
        page.wait_for_timeout(1000)

        sgm.ClickKondisi()
        page.wait_for_timeout(1000)

        sgm.ClickKondisiHamil()
        page.wait_for_timeout(1000)

        sgm.PilihMinggu("12")
        page.wait_for_timeout(1000)

        sgm.ClickSetuju()
        page.wait_for_timeout(1000)

        sgm.ClickDaftar()
        page.wait_for_timeout(3000)

        page.screenshot(path="Negative_PasswordTanpaKapital.png")

        # Site tidak mensyaratkan kapital, tidak ada warning password
        sgm.verifyNoPasswordWarning()

        browser.close()


if __name__ == "__main__":
    test_register_password_tanpa_kapital()