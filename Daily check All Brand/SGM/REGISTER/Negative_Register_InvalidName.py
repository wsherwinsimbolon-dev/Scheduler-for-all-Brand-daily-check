


"""
==============================================
  PLAYWRIGHT PYTHON - NEGATIVE TEST REGISTER
  Skenario:
    1. Register dengan nama kosong (tidak diisi)
    2. Register dengan nama kurang dari 3 karakter
==============================================
"""

from playwright.sync_api import sync_playwright
from Locator_Register import RegisterSGM
import os
HEADLESS = os.environ.get("CI", "").lower() == "true"

URL = "https://www.generasimaju.co.id/klub-generasi-maju/register?referral=https://www.generasimaju.co.id/klub-generasi-maju"


def _setup_browser(p):
    browser = p.chromium.launch(headless=HEADLESS)
    page = browser.new_page()
    return browser, page


def _fill_valid_fields(sgm, page):
    """Isi field wajib lain agar hanya validasi nama yang diuji."""
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


# ─────────────────────────────────────────
# SKENARIO 1: Nama Kosong
# ─────────────────────────────────────────
def test_register_nama_kosong():
    print("\n[SKENARIO 1] Register dengan nama kosong")
    with sync_playwright() as p:
        browser, page = _setup_browser(p)

        sgm = RegisterSGM(page)
        print(f"✓ Membuka: {sgm.url}")
        page.wait_for_timeout(3000)

        # Nama sengaja dikosongkan
        _fill_valid_fields(sgm, page)
        page.wait_for_timeout(1000)

        sgm.ClickDaftar()
        page.wait_for_timeout(3000)

        page.screenshot(path="Negative_NamaKosong.png")

        sgm.verifyWarningNama("Nama lengkap harus diisi")

        browser.close()


# ─────────────────────────────────────────
# SKENARIO 2: Nama Kurang dari 3 Karakter
# ─────────────────────────────────────────
def test_register_nama_kurang3():
    print("\n[SKENARIO 2] Register dengan nama kurang dari 3 karakter")
    with sync_playwright() as p:
        browser, page = _setup_browser(p)

        sgm = RegisterSGM(page)
        print(f"✓ Membuka: {sgm.url}")
        page.wait_for_timeout(3000)

        # Nama hanya 2 karakter
        sgm.inputNamaPertama("Ab")
        page.wait_for_timeout(1000)

        _fill_valid_fields(sgm, page)
        page.wait_for_timeout(1000)

        sgm.ClickDaftar()
        page.wait_for_timeout(3000)

        page.screenshot(path="Negative_NamaKurang3.png")

        sgm.verifyWarningNama("Nama lengkap minimal 3 Karakter")

        browser.close()


# ─────────────────────────────────────────
# JALANKAN SEMUA SKENARIO
# ─────────────────────────────────────────
if __name__ == "__main__":
    test_register_nama_kosong()
    test_register_nama_kurang3()
    print("\n✓ Semua skenario negative test selesai.")