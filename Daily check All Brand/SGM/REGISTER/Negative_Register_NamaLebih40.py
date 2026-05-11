"""
==============================================
  PLAYWRIGHT PYTHON - NEGATIVE TEST REGISTER
  Skenario: Register dengan nama lebih dari 40 karakter
==============================================
"""

from playwright.sync_api import sync_playwright
from Locator_Register import RegisterSGM


def test_register_nama_lebih40():
    print("\n[SKENARIO] Register dengan nama lebih dari 40 karakter")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        sgm = RegisterSGM(page)
        print(f"✓ Membuka: {sgm.url}")
        page.wait_for_timeout(3000)

        # Nama lebih dari 40 karakter (41 karakter)
        sgm.inputNamaPertama("A" * 41)
        page.wait_for_timeout(1000)

        sgm.InputnoHP("082281116519")
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

        page.screenshot(path="Negative_NamaLebih40.png")

        sgm.verifyWarningNama("Nama lengkap maksimal 40 Karakter")

        browser.close()


if __name__ == "__main__":
    test_register_nama_lebih40()