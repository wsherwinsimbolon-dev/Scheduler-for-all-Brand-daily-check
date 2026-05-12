from datetime import date, datetime, timedelta

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class KalkulatorKehamilanPage:
    URL = "https://www.generasimaju.co.id/tools/kalkulator-kehamilan"

    def __init__(self, page):
        self.page = page
        page.goto(self.URL, wait_until="domcontentloaded", timeout=20000)

        # ── Form Input ──
        self.inputHPHT      = page.locator("#due_date, input[name='due_date'], input[placeholder*='HPHT']")
        self.btnHitung      = page.locator("#btn-mulai, #submit-calc, button:has-text('Cek Hasil'), button:has-text('Hitung')")
        self.btnReset       = page.locator("//button[contains(translate(normalize-space(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'reset') or contains(translate(normalize-space(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'ulang')]")

        # ── Cookies & Overlay ──
        self.btnCookies     = page.locator("//button[@id='footer_tc_privacy_button']")

        # ── Result Section ──
        self.sectionHasil   = page.locator("text=Selamat Bunda!")
        self.hasilHPL       = page.locator("text=Hari Perkiraan Lahir")
        self.hasilUsia      = page.locator("text=Usia Kehamilan Bunda")
        self.hasilTrimester = page.locator("text=Trimester")
        self.hasilMinggu    = page.locator("text=/\\d+\\s+Minggu/")

        # ── Error / Validation Messages ──
        self.pesanError     = page.locator("//div[contains(@class,'error') or contains(@class,'warning') or contains(@class,'alert') or contains(@class,'invalid')]")
        self.pesanErrorHPHT = page.locator("//div[@id='hpht-error' or (contains(@class,'hpht') and contains(@class,'error'))] | //span[contains(@class,'error-hpht')]")

        # ── Page Structure ──
        self.pageTitle      = page.locator("//h1 | //h2[contains(normalize-space(),'Kalkulator') or contains(normalize-space(),'kalkulator')]")
        self.toolsContainer = page.locator("//div[contains(@class,'tools') or contains(@class,'kalkulator') or contains(@class,'calculator')]")
        self.infoTrimester1 = page.locator("//div[contains(normalize-space(),'Trimester 1') or contains(normalize-space(),'Trimester Pertama')]")
        self.infoTrimester2 = page.locator("//div[contains(normalize-space(),'Trimester 2') or contains(normalize-space(),'Trimester Kedua')]")
        self.infoTrimester3 = page.locator("//div[contains(normalize-space(),'Trimester 3') or contains(normalize-space(),'Trimester Ketiga')]")
        self.infoPerkembangan = page.locator("//div[contains(@class,'perkembangan') or contains(@class,'development') or contains(normalize-space(),'perkembangan')]")

    # ── Cookie handler ──
    def closeCookiesIfPresent(self):
        if self.btnCookies.count() > 0 and self.btnCookies.first.is_visible():
            self.btnCookies.first.click()
            self.page.wait_for_timeout(1000)

    def openHalaman(self):
        self.page.goto(self.URL, wait_until="domcontentloaded", timeout=20000)

    # ── Input HPHT ──
    def inputTanggalHPHT(self, tanggal: str):
        """Fill HPHT date. Format: YYYY-MM-DD or DD/MM/YYYY depending on the field."""
        input_el = self.inputHPHT.first
        parsed = self._parseTanggal(tanggal)

        if parsed and self._tanggalDalamRangeHPHT(parsed):
            input_el.evaluate(
                """(el, value) => {
                    const selectedDate = new Date(value.year, value.month - 1, value.day);
                    if (window.jQuery && window.jQuery.fn.datepicker) {
                        window.jQuery(el).datepicker("setDate", selectedDate);
                        window.jQuery(el).trigger({ type: "changeDate", date: selectedDate });
                        window.jQuery(el).trigger("change");
                    } else {
                        el.removeAttribute("readonly");
                        el.value = value.raw;
                        el.dispatchEvent(new Event("input", { bubbles: true }));
                        el.dispatchEvent(new Event("change", { bubbles: true }));
                    }
                }""",
                {
                    "day": parsed.day,
                    "month": parsed.month,
                    "year": parsed.year,
                    "raw": tanggal,
                },
            )
        else:
            input_el.evaluate(
                """(el, value) => {
                    el.removeAttribute("readonly");
                    el.value = value;
                    el.dispatchEvent(new Event("input", { bubbles: true }));
                    el.dispatchEvent(new Event("change", { bubbles: true }));
                }""",
                tanggal,
            )

    def clearHPHT(self):
        self.inputHPHT.first.evaluate(
            """el => {
                el.removeAttribute("readonly");
                el.value = "";
                el.dispatchEvent(new Event("input", { bubbles: true }));
                el.dispatchEvent(new Event("change", { bubbles: true }));
            }"""
        )

    # ── Actions ──
    def clickHitung(self):
        button = self.btnHitung.first
        if button.count() == 0:
            raise AssertionError("✗ Tombol Hitung tidak ditemukan")
        if button.get_attribute("disabled") is not None:
            print("  Tombol Hitung disabled, kalkulasi tidak dijalankan")
            return False
        button.click()
        try:
            self.page.wait_for_url("**/result", timeout=10000)
        except PlaywrightTimeoutError:
            pass
        return True

    def clickReset(self):
        if self.btnReset.count() > 0:
            self.btnReset.first.click()

    # ── Getters ──
    def getPageTitle(self):
        if self.pageTitle.count() > 0:
            return self.pageTitle.first.inner_text().strip()
        return ""

    def getHPL(self):
        el = self.hasilHPL.first
        return el.inner_text().strip() if self.hasilHPL.count() > 0 else ""

    def getUsiaKehamilan(self):
        el = self.hasilUsia.first
        return el.inner_text().strip() if self.hasilUsia.count() > 0 else ""

    def getTrimester(self):
        el = self.hasilTrimester.first
        return el.inner_text().strip() if self.hasilTrimester.count() > 0 else ""

    def getMinggu(self):
        el = self.hasilMinggu.first
        return el.inner_text().strip() if self.hasilMinggu.count() > 0 else ""

    def getPesanError(self):
        el = self.pesanError.first
        return el.inner_text().strip() if self.pesanError.count() > 0 else ""

    def isHasilVisible(self):
        return self.sectionHasil.count() > 0 and self.sectionHasil.first.is_visible()

    def isErrorVisible(self):
        return self.pesanError.count() > 0 and self.pesanError.first.is_visible()

    # ── Helper: calculate HPHT string from weeks ago ──
    @staticmethod
    def hphtDariMingguLalu(minggu: int) -> str:
        """Return HPHT date string (YYYY-MM-DD) from N weeks ago."""
        return (date.today() - timedelta(weeks=minggu)).strftime("%Y-%m-%d")

    @staticmethod
    def hphtDariMingguLaluSlash(minggu: int) -> str:
        """Return HPHT date string (DD/MM/YYYY) from N weeks ago."""
        return (date.today() - timedelta(weeks=minggu)).strftime("%d/%m/%Y")

    @staticmethod
    def _parseTanggal(tanggal: str):
        for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(tanggal, fmt).date()
            except ValueError:
                pass
        return None

    @staticmethod
    def _tanggalDalamRangeHPHT(tanggal: date):
        usia_kehamilan = date.today() - tanggal
        return timedelta(days=0) <= usia_kehamilan <= timedelta(weeks=42)

    # ── Verifications ──
    def verifyHalamanTerbuka(self):
        assert self.URL in self.page.url, f"✗ URL tidak sesuai. Sekarang: {self.page.url}"
        assert "403" not in self.page.title(), "✗ Halaman diblokir 403 Forbidden"
        print(f"✓ Halaman terbuka: {self.page.url}")

    def verifyJudulAda(self):
        assert self.pageTitle.count() > 0, "✗ Judul halaman tidak ditemukan"
        title = self.getPageTitle()
        assert title != "", "✗ Judul halaman kosong"
        print(f"✓ Judul halaman ditemukan: '{title}'")

    def verifyInputHPHTAda(self):
        self.inputHPHT.first.wait_for(state="visible", timeout=10000)
        assert self.inputHPHT.count() > 0, "✗ Input HPHT tidak ditemukan di halaman"
        print("✓ Input HPHT ditemukan")

    def verifyTombolHitungAda(self):
        self.btnHitung.first.wait_for(state="visible", timeout=10000)
        assert self.btnHitung.count() > 0, "✗ Tombol Hitung tidak ditemukan"
        print("✓ Tombol Hitung ditemukan")

    def verifyHasilMuncul(self):
        self.sectionHasil.first.wait_for(state="visible", timeout=10000)
        assert self.isHasilVisible(), "✗ Section hasil tidak tampil setelah klik Hitung"
        print("✓ Section hasil kalkulasi tampil")

    def verifyErrorMuncul(self, pesan_yang_diharapkan: str = ""):
        assert self.isErrorVisible(), "✗ Pesan error tidak muncul padahal input tidak valid"
        if pesan_yang_diharapkan:
            actual = self.getPesanError()
            assert pesan_yang_diharapkan.lower() in actual.lower(), \
                f"✗ Pesan error tidak sesuai. Diharapkan mengandung: '{pesan_yang_diharapkan}', Didapat: '{actual}'"
        print(f"✓ Pesan error muncul: '{self.getPesanError()}'")
