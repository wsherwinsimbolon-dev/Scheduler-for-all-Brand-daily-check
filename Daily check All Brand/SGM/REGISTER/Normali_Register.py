"""
==============================================
  PLAYWRIGHT PYTHON - LOGIN BASIC
  Install dulu: pip install playwright
                playwright install chromium
==============================================
"""

from playwright.sync_api import sync_playwright
from Locator_Register import RegisterSGM

# ─────────────────────────────────────────
# FUNGSI UTAMA
# ─────────────────────────────────────────
def login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Buat objek dulu, url & goto sudah otomatis di dalam __init__
        sgm = RegisterSGM(page)
        print(f"✓ Membuka: {sgm.url}")
        page.wait_for_timeout(5000)

        #Input Nama Depan
        sgm.inputNamaPertama("Sherwin")
        page.wait_for_timeout(5000)




        #Input no Hp
        sgm.InputnoHP("082281116519")
        page.wait_for_timeout(5000)

        #input Password
        sgm.Inputpassword("Tes12345!")
        page.wait_for_timeout(5000)

        #Pilih Kondisi Bunda
        sgm.ClickKondisi()
        page.wait_for_timeout(2000)

        #Pilih opsi Hamil
        sgm.ClickKondisiHamil()
        page.wait_for_timeout(2000)

        #Pilih minggu kehamilan (1-42)
        sgm.PilihMinggu("12")
        page.wait_for_timeout(2000)

        #Centang persetujuan syarat & ketentuan
        sgm.ClickSetuju()
        page.wait_for_timeout(2000)

        page.screenshot(path="RegisterBerhasil.png")

        #Klik tombol Daftar
        sgm.ClickDaftar()
        page.wait_for_timeout(5000)

        #Verifikasi elemen hasil registrasi
        sgm.verifyElementPresent()

        browser.close()

if __name__ == "__main__":
    login()