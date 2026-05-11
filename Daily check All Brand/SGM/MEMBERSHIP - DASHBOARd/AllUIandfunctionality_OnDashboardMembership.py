"""
==============================================
  PLAYWRIGHT PYTHON - LOGIN BASIC
  Install dulu: pip install playwright
                playwright install chromium
==============================================
"""

from playwright.sync_api import sync_playwright
from Locator_Dasboard_Menu import MembershipDashboard

# ─────────────────────────────────────────
# FUNGSI UTAMA
# ─────────────────────────────────────────
def login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Buat objek dulu, url & goto sudah otomatis di dalam __init__
        sgm = MembershipDashboard(page)
        print(f"✓ Membuka: {sgm.url}")
        page.wait_for_timeout(5000)

        #Input Username
        sgm.noHP("082281116519")
        page.wait_for_timeout(5000)

        #Input Password
        sgm.pasWort("Tes12345!")
        page.wait_for_timeout(5000)

        #button Masuk
        sgm.tombolMasuk()
        page.wait_for_timeout(5000)

        # Click Profile
        sgm.clickXbuttonprofile()
        page.wait_for_timeout(5000)
        # screenshoot

        #Click Profile
        sgm.ClickProfileDashboardmember()
        page.wait_for_timeout(5000)


        page.screenshot(path="Uifunctional.png")

        browser.close()

if __name__ == "__main__":
    login()