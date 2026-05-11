"""
==============================================
  PLAYWRIGHT PYTHON - NEGATIVE TEST REGISTER
  Skenario: Register dengan nomor ponsel prefix tidak valid
  Prefix valid: 08xx (Telkomsel, XL, Indosat, dll)
  Prefix tidak valid contoh: 021 (nomor rumah/PSTN)
==============================================
"""

from playwright.sync_api import sync_playwright
from Locator_Register import RegisterSGM


def test_register_phone_prefix_tidak_valid():
    print("\n[SKENARIO] Register dengan nomor ponsel prefix tidak valid")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        sgm = RegisterSGM(page)
        print(f"✓ Membuka: {sgm.url}")
        page.wait_for_timeout(3000)

        sgm.inputNamaPertama("Sherwin")
        page.wait_for_timeout(1000)

        # Prefix 021 bukan prefix ponsel Indonesia yang valid
        sgm.InputnoHP("021123456789")
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

        page.screenshot(path="Negative_PhonePrefixTidakValid.png")

        sgm.verifyWarningPhone("Nomor Ponsel Bunda tidak terdaftar di Indonesia")

        browser.close()


if __name__ == "__main__":
    test_register_phone_prefix_tidak_valid()