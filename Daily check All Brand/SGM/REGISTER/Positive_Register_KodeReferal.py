"""
==============================================
  PLAYWRIGHT PYTHON - POSITIVE TEST REGISTER
  Skenario: Register dengan kode referral yang valid
  Catatan: Ganti KODE_REFERAL di bawah dengan kode referral yang valid
==============================================
"""

from playwright.sync_api import sync_playwright
from Locator_Register import RegisterSGM
import os
HEADLESS = os.environ.get("CI", "").lower() == "true"

KODE_REFERAL = "082281116519"  # Ganti dengan kode referral yang valid


def test_register_dengan_kode_referal():
    print("\n[SKENARIO] Register dengan kode referral valid")
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

        sgm.Inputpassword("Tes12345!")
        page.wait_for_timeout(1000)

        sgm.ClickKondisi()
        page.wait_for_timeout(1000)

        sgm.ClickKondisiHamil()
        page.wait_for_timeout(1000)

        sgm.PilihMinggu("12")
        page.wait_for_timeout(1000)

        # Pilih opsi Kode Referral dan masukkan kode
        sgm.ClickKodeReferalRadio()
        page.wait_for_timeout(1000)

        sgm.IsiKodeReferal(KODE_REFERAL)
        print(f"✓ Kode referral diisi: {KODE_REFERAL}")
        page.wait_for_timeout(1000)

        sgm.ClickSetuju()
        page.wait_for_timeout(1000)

        sgm.ClickDaftar()
        page.wait_for_timeout(5000)

        page.screenshot(path="Positive_KodeReferal.png")

        sgm.verifyElementPresent()

        browser.close()


if __name__ == "__main__":
    test_register_dengan_kode_referal()