"""
==============================================
  PLAYWRIGHT PYTHON - KALKULATOR KEHAMILAN
  Skenario: Cek semua fungsi Kalkulator Kehamilan
  URL     : https://www.generasimaju.co.id/tools/kalkulator-kehamilan
  Catatan : Menggunakan HPHT (Hari Pertama Haid Terakhir) sebagai input
            untuk menghitung HPL dan usia kehamilan.
==============================================
"""

import os

from playwright.sync_api import sync_playwright
from Locator_KalkulatorKehamilan import KalkulatorKehamilanPage

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)


# ─────────────────────────────────────────────────────────────
#  SKENARIO POSITIF
# ─────────────────────────────────────────────────────────────

def test_ui_halaman_terbuka(kalk, page):
    """TC-POS-01: Halaman Kalkulator Kehamilan berhasil dibuka"""
    print("\n[TC-POS-01] Verifikasi halaman terbuka")
    kalk.verifyHalamanTerbuka()
    kalk.verifyJudulAda()
    kalk.verifyInputHPHTAda()
    kalk.verifyTombolHitungAda()
    page.screenshot(path="Positive_KalkulatorKehamilan_Halaman.png")
    print("✓ TC-POS-01 PASSED\n")


def test_hitung_trimester1(kalk, page):
    """TC-POS-02: Hitung usia kehamilan Trimester 1 (8 minggu)"""
    print("\n[TC-POS-02] HPHT 8 minggu lalu → Trimester 1")
    hpht = KalkulatorKehamilanPage.hphtDariMingguLaluSlash(8)
    print(f"  HPHT: {hpht}")

    kalk.closeCookiesIfPresent()
    kalk.inputTanggalHPHT(hpht)
    page.wait_for_timeout(1000)
    kalk.clickHitung()
    page.wait_for_timeout(3000)

    kalk.verifyHasilMuncul()
    hpl     = kalk.getHPL()
    usia    = kalk.getUsiaKehamilan()
    trimest = kalk.getTrimester()
    minggu  = kalk.getMinggu()

    print(f"  HPL             : {hpl}")
    print(f"  Usia Kehamilan  : {usia}")
    print(f"  Trimester       : {trimest}")
    print(f"  Minggu          : {minggu}")

    assert hpl != "",  "✗ HPL tidak tampil"
    assert usia != "" or minggu != "", "✗ Usia kehamilan tidak tampil"
    print("✓ TC-POS-02 PASSED\n")
    page.screenshot(path="Positive_KalkulatorKehamilan_Trimester1.png")


def test_hitung_trimester2(kalk, page):
    """TC-POS-03: Hitung usia kehamilan Trimester 2 (16 minggu)"""
    print("\n[TC-POS-03] HPHT 16 minggu lalu → Trimester 2")
    hpht = KalkulatorKehamilanPage.hphtDariMingguLaluSlash(16)
    print(f"  HPHT: {hpht}")

    kalk.openHalaman()
    page.wait_for_timeout(3000)
    kalk.closeCookiesIfPresent()
    kalk.inputTanggalHPHT(hpht)
    page.wait_for_timeout(1000)
    kalk.clickHitung()
    page.wait_for_timeout(3000)

    kalk.verifyHasilMuncul()
    hpl     = kalk.getHPL()
    usia    = kalk.getUsiaKehamilan()
    trimest = kalk.getTrimester()

    print(f"  HPL             : {hpl}")
    print(f"  Usia Kehamilan  : {usia}")
    print(f"  Trimester       : {trimest}")

    assert hpl != "", "✗ HPL tidak tampil"
    print("✓ TC-POS-03 PASSED\n")
    page.screenshot(path="Positive_KalkulatorKehamilan_Trimester2.png")


def test_hitung_trimester3(kalk, page):
    """TC-POS-04: Hitung usia kehamilan Trimester 3 (30 minggu)"""
    print("\n[TC-POS-04] HPHT 30 minggu lalu → Trimester 3")
    hpht = KalkulatorKehamilanPage.hphtDariMingguLaluSlash(30)
    print(f"  HPHT: {hpht}")

    kalk.openHalaman()
    page.wait_for_timeout(3000)
    kalk.closeCookiesIfPresent()
    kalk.inputTanggalHPHT(hpht)
    page.wait_for_timeout(1000)
    kalk.clickHitung()
    page.wait_for_timeout(3000)

    kalk.verifyHasilMuncul()
    hpl     = kalk.getHPL()
    usia    = kalk.getUsiaKehamilan()
    trimest = kalk.getTrimester()

    print(f"  HPL             : {hpl}")
    print(f"  Usia Kehamilan  : {usia}")
    print(f"  Trimester       : {trimest}")

    assert hpl != "", "✗ HPL tidak tampil"
    print("✓ TC-POS-04 PASSED\n")
    page.screenshot(path="Positive_KalkulatorKehamilan_Trimester3.png")


def test_hitung_kehamilan_muda(kalk, page):
    """TC-POS-05: Hitung kehamilan sangat muda (4 minggu = 1 bulan)"""
    print("\n[TC-POS-05] HPHT 4 minggu lalu → Kehamilan muda")
    hpht = KalkulatorKehamilanPage.hphtDariMingguLaluSlash(4)
    print(f"  HPHT: {hpht}")

    kalk.openHalaman()
    page.wait_for_timeout(3000)
    kalk.closeCookiesIfPresent()
    kalk.inputTanggalHPHT(hpht)
    page.wait_for_timeout(1000)
    kalk.clickHitung()
    page.wait_for_timeout(3000)

    kalk.verifyHasilMuncul()
    hpl  = kalk.getHPL()
    usia = kalk.getUsiaKehamilan()
    print(f"  HPL            : {hpl}")
    print(f"  Usia Kehamilan : {usia}")

    assert hpl != "", "✗ HPL tidak tampil"
    print("✓ TC-POS-05 PASSED\n")
    page.screenshot(path="Positive_KalkulatorKehamilan_4Minggu.png")


def test_hitung_mendekati_hpl(kalk, page):
    """TC-POS-06: Hitung kehamilan mendekati HPL (38 minggu)"""
    print("\n[TC-POS-06] HPHT 38 minggu lalu → Mendekati HPL")
    hpht = KalkulatorKehamilanPage.hphtDariMingguLaluSlash(38)
    print(f"  HPHT: {hpht}")

    kalk.openHalaman()
    page.wait_for_timeout(3000)
    kalk.closeCookiesIfPresent()
    kalk.inputTanggalHPHT(hpht)
    page.wait_for_timeout(1000)
    kalk.clickHitung()
    page.wait_for_timeout(3000)

    kalk.verifyHasilMuncul()
    hpl  = kalk.getHPL()
    usia = kalk.getUsiaKehamilan()
    print(f"  HPL            : {hpl}")
    print(f"  Usia Kehamilan : {usia}")

    assert hpl != "", "✗ HPL tidak tampil"
    print("✓ TC-POS-06 PASSED\n")
    page.screenshot(path="Positive_KalkulatorKehamilan_38Minggu.png")


def test_hitung_tepat_hpl(kalk, page):
    """TC-POS-07: Hitung kehamilan tepat 40 minggu (HPL hari ini)"""
    print("\n[TC-POS-07] HPHT 40 minggu lalu → HPL hari ini")
    hpht = KalkulatorKehamilanPage.hphtDariMingguLaluSlash(40)
    print(f"  HPHT: {hpht}")

    kalk.openHalaman()
    page.wait_for_timeout(3000)
    kalk.closeCookiesIfPresent()
    kalk.inputTanggalHPHT(hpht)
    page.wait_for_timeout(1000)
    kalk.clickHitung()
    page.wait_for_timeout(3000)

    kalk.verifyHasilMuncul()
    hpl  = kalk.getHPL()
    print(f"  HPL: {hpl}")
    assert hpl != "", "✗ HPL tidak tampil"
    print("✓ TC-POS-07 PASSED\n")
    page.screenshot(path="Positive_KalkulatorKehamilan_40Minggu.png")


def test_verifikasi_informasi_trimester_muncul(kalk, page):
    """TC-POS-08: Verifikasi informasi / edukasi trimester tampil setelah hitung"""
    print("\n[TC-POS-08] Verifikasi informasi trimester tampil")
    hpht = KalkulatorKehamilanPage.hphtDariMingguLaluSlash(20)

    kalk.openHalaman()
    page.wait_for_timeout(3000)
    kalk.closeCookiesIfPresent()
    kalk.inputTanggalHPHT(hpht)
    page.wait_for_timeout(1000)
    kalk.clickHitung()
    page.wait_for_timeout(3000)

    kalk.verifyHasilMuncul()

    has_info = (
        kalk.infoTrimester1.count() > 0
        or kalk.infoTrimester2.count() > 0
        or kalk.infoTrimester3.count() > 0
        or kalk.infoPerkembangan.count() > 0
    )
    assert has_info, "✗ Informasi trimester / perkembangan janin tidak tampil"
    print("✓ Informasi trimester / perkembangan janin tampil")
    print("✓ TC-POS-08 PASSED\n")
    page.screenshot(path="Positive_KalkulatorKehamilan_InfoTrimester.png")


# ─────────────────────────────────────────────────────────────
#  SKENARIO NEGATIF
# ─────────────────────────────────────────────────────────────

def test_hpht_kosong(kalk, page):
    """TC-NEG-01: Klik Hitung tanpa mengisi HPHT → Harus muncul error"""
    print("\n[TC-NEG-01] Input HPHT kosong → error wajib muncul")

    kalk.openHalaman()
    page.wait_for_timeout(3000)
    kalk.closeCookiesIfPresent()
    kalk.clearHPHT()
    page.wait_for_timeout(500)
    kalk.clickHitung()
    page.wait_for_timeout(2000)

    has_error = kalk.isErrorVisible()
    hasil_tidak_muncul = not kalk.isHasilVisible()

    assert has_error or hasil_tidak_muncul, \
        "✗ Sistem seharusnya mencegah kalkulasi saat HPHT kosong"
    print(f"  Pesan error: '{kalk.getPesanError()}'")
    print("✓ TC-NEG-01 PASSED\n")
    page.screenshot(path="Negative_KalkulatorKehamilan_HPHTKosong.png")


def test_hpht_masa_depan(kalk, page):
    """TC-NEG-02: HPHT tanggal di masa depan → Harus muncul error"""
    print("\n[TC-NEG-02] HPHT tanggal depan → error wajib muncul")
    from datetime import date, timedelta
    hpht_depan = (date.today() + timedelta(days=7)).strftime("%d/%m/%Y")
    print(f"  HPHT (depan): {hpht_depan}")

    kalk.openHalaman()
    page.wait_for_timeout(3000)
    kalk.closeCookiesIfPresent()
    kalk.inputTanggalHPHT(hpht_depan)
    page.wait_for_timeout(500)
    kalk.clickHitung()
    page.wait_for_timeout(2000)

    has_error = kalk.isErrorVisible()
    hasil_tidak_muncul = not kalk.isHasilVisible()

    assert has_error or hasil_tidak_muncul, \
        "✗ Sistem seharusnya menolak HPHT yang ada di masa depan"
    print(f"  Pesan error: '{kalk.getPesanError()}'")
    print("✓ TC-NEG-02 PASSED\n")
    page.screenshot(path="Negative_KalkulatorKehamilan_HPHTMasaDepan.png")


def test_hpht_lebih_dari_42_minggu(kalk, page):
    """TC-NEG-03: HPHT lebih dari 42 minggu lalu → Seharusnya tidak valid"""
    print("\n[TC-NEG-03] HPHT > 42 minggu lalu → error atau peringatan wajib muncul")
    hpht = KalkulatorKehamilanPage.hphtDariMingguLaluSlash(50)
    print(f"  HPHT (50 minggu lalu): {hpht}")

    kalk.openHalaman()
    page.wait_for_timeout(3000)
    kalk.closeCookiesIfPresent()
    kalk.inputTanggalHPHT(hpht)
    page.wait_for_timeout(500)
    kalk.clickHitung()
    page.wait_for_timeout(2000)

    has_error = kalk.isErrorVisible()
    hasil_tidak_muncul = not kalk.isHasilVisible()

    assert has_error or hasil_tidak_muncul, \
        "✗ Sistem seharusnya menolak HPHT yang sudah melewati 42 minggu"
    print(f"  Pesan error / hasil: '{kalk.getPesanError()}'")
    print("✓ TC-NEG-03 PASSED\n")
    page.screenshot(path="Negative_KalkulatorKehamilan_HPHT50Minggu.png")


def test_hpht_format_tidak_valid(kalk, page):
    """TC-NEG-04: Input HPHT dengan karakter bukan tanggal → error"""
    print("\n[TC-NEG-04] Input HPHT karakter acak → error wajib muncul")

    kalk.openHalaman()
    page.wait_for_timeout(3000)
    kalk.closeCookiesIfPresent()
    kalk.inputTanggalHPHT("abcdefgh")
    page.wait_for_timeout(500)
    kalk.clickHitung()
    page.wait_for_timeout(2000)

    has_error = kalk.isErrorVisible()
    hasil_tidak_muncul = not kalk.isHasilVisible()

    assert has_error or hasil_tidak_muncul, \
        "✗ Sistem seharusnya menolak input bukan tanggal"
    print(f"  Pesan error: '{kalk.getPesanError()}'")
    print("✓ TC-NEG-04 PASSED\n")
    page.screenshot(path="Negative_KalkulatorKehamilan_FormatTidakValid.png")


def test_hpht_angka_acak(kalk, page):
    """TC-NEG-05: Input HPHT dengan angka tidak berformat tanggal → error"""
    print("\n[TC-NEG-05] Input HPHT angka acak → error wajib muncul")

    kalk.openHalaman()
    page.wait_for_timeout(3000)
    kalk.closeCookiesIfPresent()
    kalk.inputTanggalHPHT("99/99/9999")
    page.wait_for_timeout(500)
    kalk.clickHitung()
    page.wait_for_timeout(2000)

    has_error = kalk.isErrorVisible()
    hasil_tidak_muncul = not kalk.isHasilVisible()

    assert has_error or hasil_tidak_muncul, \
        "✗ Sistem seharusnya menolak tanggal tidak valid (99/99/9999)"
    print(f"  Pesan error: '{kalk.getPesanError()}'")
    print("✓ TC-NEG-05 PASSED\n")
    page.screenshot(path="Negative_KalkulatorKehamilan_TanggalTidakValid.png")


def test_hpht_spesial_karakter(kalk, page):
    """TC-NEG-06: Input HPHT dengan karakter spesial → error"""
    print("\n[TC-NEG-06] Input HPHT karakter spesial → error wajib muncul")

    kalk.openHalaman()
    page.wait_for_timeout(3000)
    kalk.closeCookiesIfPresent()
    kalk.inputTanggalHPHT("!@#$%^&*()")
    page.wait_for_timeout(500)
    kalk.clickHitung()
    page.wait_for_timeout(2000)

    has_error = kalk.isErrorVisible()
    hasil_tidak_muncul = not kalk.isHasilVisible()

    assert has_error or hasil_tidak_muncul, \
        "✗ Sistem seharusnya menolak karakter spesial"
    print(f"  Pesan error: '{kalk.getPesanError()}'")
    print("✓ TC-NEG-06 PASSED\n")
    page.screenshot(path="Negative_KalkulatorKehamilan_KarakterSpesial.png")


# ─────────────────────────────────────────────────────────────
#  SKENARIO UI / REGRESSION
# ─────────────────────────────────────────────────────────────

def test_ui_elemen_halaman(kalk, page):
    """TC-UI-01: Verifikasi elemen-elemen penting di halaman ada semua"""
    print("\n[TC-UI-01] Verifikasi elemen halaman")
    errors = []

    if kalk.inputHPHT.count() == 0:
        errors.append("Input HPHT tidak ditemukan")
    if kalk.btnHitung.count() == 0:
        errors.append("Tombol Hitung tidak ditemukan")
    if kalk.pageTitle.count() == 0:
        errors.append("Judul halaman tidak ditemukan")

    if errors:
        for e in errors:
            print(f"  ✗ {e}")
        raise AssertionError(f"Elemen halaman tidak lengkap: {errors}")

    print(f"  ✓ Input HPHT   : ada")
    print(f"  ✓ Tombol Hitung: ada")
    print(f"  ✓ Judul halaman: '{kalk.getPageTitle()}'")
    print("✓ TC-UI-01 PASSED\n")
    page.screenshot(path="UI_KalkulatorKehamilan_Elemen.png")


def test_ui_reset_form(kalk, page):
    """TC-UI-02: Tombol Reset / Ulang membersihkan form dan hasil"""
    print("\n[TC-UI-02] Tombol Reset membersihkan form")
    hpht = KalkulatorKehamilanPage.hphtDariMingguLaluSlash(20)

    kalk.openHalaman()
    page.wait_for_timeout(3000)
    kalk.closeCookiesIfPresent()
    kalk.inputTanggalHPHT(hpht)
    kalk.clickHitung()
    page.wait_for_timeout(2000)

    if kalk.btnReset.count() > 0:
        kalk.clickReset()
        page.wait_for_timeout(1500)
        nilai_input = kalk.inputHPHT.input_value()
        assert nilai_input == "", f"✗ Input HPHT tidak kosong setelah reset: '{nilai_input}'"
        print("  ✓ Input HPHT kosong setelah reset")
        print("✓ TC-UI-02 PASSED\n")
    else:
        print("  ⚠ Tombol Reset tidak ditemukan di halaman — skenario dilewati")
    page.screenshot(path="UI_KalkulatorKehamilan_Reset.png")


def test_ui_scroll_dan_layout(kalk, page):
    """TC-UI-03: Halaman dapat di-scroll, layout tidak rusak"""
    print("\n[TC-UI-03] Scroll dan layout halaman")

    kalk.openHalaman()
    page.wait_for_timeout(3000)

    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(1500)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(1000)

    assert kalk.inputHPHT.count() > 0, "✗ Input HPHT hilang setelah scroll"
    assert kalk.btnHitung.count() > 0,  "✗ Tombol Hitung hilang setelah scroll"
    print("  ✓ Layout tidak rusak setelah scroll")
    print("✓ TC-UI-03 PASSED\n")
    page.screenshot(path="UI_KalkulatorKehamilan_Layout.png")


def test_ui_page_title_dan_meta(kalk, page):
    """TC-UI-04: Verifikasi page title dan URL sesuai"""
    print("\n[TC-UI-04] Verifikasi page title browser dan URL")

    browser_title = page.title()
    current_url   = page.url

    assert "generasimaju" in current_url.lower(), \
        f"✗ URL tidak mengandung 'generasimaju': {current_url}"
    assert browser_title != "", "✗ Browser title kosong"

    print(f"  ✓ URL          : {current_url}")
    print(f"  ✓ Browser Title: {browser_title}")
    print("✓ TC-UI-04 PASSED\n")


def test_ui_mobile_viewport(kalk, page):
    """TC-UI-05: Tampilan halaman pada ukuran layar mobile (375x812)"""
    print("\n[TC-UI-05] Tampilan mobile viewport (375x812)")

    page.set_viewport_size({"width": 375, "height": 812})
    kalk.openHalaman()
    page.wait_for_timeout(3000)
    kalk.closeCookiesIfPresent()

    assert kalk.inputHPHT.count() > 0, "✗ Input HPHT tidak tampil di mobile"
    assert kalk.btnHitung.count() > 0,  "✗ Tombol Hitung tidak tampil di mobile"
    print("  ✓ Input HPHT dan Tombol Hitung tampil di mobile")

    page.screenshot(path="UI_KalkulatorKehamilan_Mobile.png")

    # Kembalikan ukuran ke desktop
    page.set_viewport_size({"width": 1280, "height": 800})
    print("✓ TC-UI-05 PASSED\n")


# ─────────────────────────────────────────────────────────────
#  RUNNER UTAMA
# ─────────────────────────────────────────────────────────────

def run_all():
    summary = {"passed": 0, "failed": 0, "errors": []}

    TESTS_POSITIF = [
        ("TC-POS-01", test_ui_halaman_terbuka),
        ("TC-POS-02", test_hitung_trimester1),
        ("TC-POS-03", test_hitung_trimester2),
        ("TC-POS-04", test_hitung_trimester3),
        ("TC-POS-05", test_hitung_kehamilan_muda),
        ("TC-POS-06", test_hitung_mendekati_hpl),
        ("TC-POS-07", test_hitung_tepat_hpl),
        ("TC-POS-08", test_verifikasi_informasi_trimester_muncul),
    ]

    TESTS_NEGATIF = [
        ("TC-NEG-01", test_hpht_kosong),
        ("TC-NEG-02", test_hpht_masa_depan),
        ("TC-NEG-03", test_hpht_lebih_dari_42_minggu),
        ("TC-NEG-04", test_hpht_format_tidak_valid),
        ("TC-NEG-05", test_hpht_angka_acak),
        ("TC-NEG-06", test_hpht_spesial_karakter),
    ]

    TESTS_UI = [
        ("TC-UI-01", test_ui_elemen_halaman),
        ("TC-UI-02", test_ui_reset_form),
        ("TC-UI-03", test_ui_scroll_dan_layout),
        ("TC-UI-04", test_ui_page_title_dan_meta),
        ("TC-UI-05", test_ui_mobile_viewport),
    ]

    ALL_TESTS = TESTS_POSITIF + TESTS_NEGATIF + TESTS_UI

    with sync_playwright() as p:
        headless = os.getenv("HEADLESS", "true").lower() not in ("0", "false", "no")
        browser = p.chromium.launch(headless=headless)
        page    = browser.new_page(user_agent=os.getenv("USER_AGENT", DEFAULT_USER_AGENT))
        page.set_default_timeout(10000)
        page.set_default_navigation_timeout(20000)
        page.set_viewport_size({"width": 1280, "height": 800})

        kalk = KalkulatorKehamilanPage(page)
        print(f"✓ Membuka: {kalk.URL}")
        page.wait_for_timeout(4000)
        kalk.closeCookiesIfPresent()

        print(f"\n{'='*60}")
        print(f"  KALKULATOR KEHAMILAN — TOTAL {len(ALL_TESTS)} TEST CASE")
        print(f"{'='*60}")

        for tc_id, test_fn in ALL_TESTS:
            try:
                test_fn(kalk, page)
                summary["passed"] += 1
            except AssertionError as e:
                summary["failed"] += 1
                summary["errors"].append({"id": tc_id, "msg": str(e)})
                print(f"✗ {tc_id} FAILED: {e}\n")
                page.screenshot(path=f"Error_{tc_id}.png")
            except Exception as e:
                summary["failed"] += 1
                summary["errors"].append({"id": tc_id, "msg": f"[EXCEPTION] {e}"})
                print(f"✗ {tc_id} ERROR: {e}\n")
                page.screenshot(path=f"Error_{tc_id}.png")

        browser.close()

    # ── Laporan Akhir ──
    total = summary["passed"] + summary["failed"]
    print(f"\n{'='*60}")
    print(f"  HASIL AKHIR PENGUJIAN KALKULATOR KEHAMILAN")
    print(f"{'='*60}")
    print(f"  Total Test Case : {total}")
    print(f"  Passed          : {summary['passed']}")
    print(f"  Failed          : {summary['failed']}")

    if summary["errors"]:
        print(f"\n  DAFTAR KEGAGALAN:")
        for err in summary["errors"]:
            print(f"  - [{err['id']}] {err['msg']}")
    else:
        print("  ✓ Semua test case PASSED")

    return summary


if __name__ == "__main__":
    run_all()
