"""
==============================================
  PLAYWRIGHT PYTHON - NEGATIVE TEST REGISTER
  Skenario: Register dengan nomor ponsel lebih dari 13 karakter
==============================================
"""

from playwright.sync_api import sync_playwright
from Locator_Register import RegisterSGM


def test_register_phone_lebih13():
    print("\n[SKENARIO] Register dengan nomor ponsel lebih dari 13 karakter")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        sgm = RegisterSGM(page)
        print(f"✓ Membuka: {sgm.url}")
        page.wait_for_timeout(3000)

        sgm.inputNamaPertama("Sherwin")
        page.wait_for_timeout(1000)

        # Nomor ponsel 16 digit (lebih dari 13)
        sgm.InputnoHP("0822811169123456")
        page.wait_for_timeout(1000)

        sgm.Inputpassword("Tes12345!")
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

        page.screenshot(path="Negative_PhoneLebih13.png")

        sgm.verifyWarningPhone("Nomor Ponsel maksimal 13 karakter")

        browser.close()


if __name__ == "__main__":
    test_register_phone_lebih13()