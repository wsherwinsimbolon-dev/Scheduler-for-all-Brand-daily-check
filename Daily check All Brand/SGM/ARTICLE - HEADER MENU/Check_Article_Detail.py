"""
==============================================
  PLAYWRIGHT PYTHON - ARTICLE DETAIL CHECK
  Skenario : Cek semua detail setiap artikel
  Cakupan  : Semua kategori (Bunda/Bayi/Anak) x Semua topik x Semua halaman
  Yang dicek per artikel:
    1. H1 Judul
    2. Penulis (author)
    3. Tanggal terbit
    4. Badge milestone (Menyusui, Trimester 1, dll)
    5. Badge kategori (Tips, Nutrisi, dll)
    6. Gambar hero (src & alt)
    7. Konten artikel (tidak kosong)
    8. Section Bagikan (share)
    9. Artikel Terkait (ada minimal 1)
==============================================
"""

from playwright.sync_api import sync_playwright
from Locator_Article import ArticlePage, ArticleDetailPage


def collect_links(browser):
    """Phase 1: collect all unique article URLs from listing pages."""
    print("=" * 60)
    print("  FASE 1: Mengumpulkan semua link artikel unik...")
    print("=" * 60)
    page = browser.new_page()
    listing = ArticlePage(page)
    links = listing.collectAllArticleLinks()
    page.close()
    print(f"  Total artikel unik ditemukan: {len(links)}\n")
    return links


def check_all_details(browser, links):
    """Phase 2: open each article and verify all detail elements."""
    print("=" * 60)
    print("  FASE 2: Mengecek detail setiap artikel...")
    print("=" * 60)

    page = browser.new_page()
    detail = ArticleDetailPage(page)

    summary = {"total": 0, "passed": 0, "failed": 0, "errors": []}

    for idx, url in enumerate(links, start=1):
        summary["total"] += 1
        result = detail.verifyDetail(url)

        slug = url.split("/artikel/")[-1] if "/artikel/" in url else url
        if result["errors"]:
            summary["failed"] += 1
            summary["errors"].append(result)
            print(f"  ✗ [{idx}/{len(links)}] {slug}")
            print(f"       Judul   : {result['title'][:70] or '(kosong)'}")
            for err in result["errors"]:
                print(f"       ⚠ {err}")
        else:
            summary["passed"] += 1
            print(f"  ✓ [{idx}/{len(links)}] {slug}")
            print(f"       Judul    : {result['title'][:70]}")
            print(f"       Penulis  : {result['author']}")
            print(f"       Terbit   : {result['date']}")
            print(f"       Milestone: {result['milestone']} | Kategori: {result['category']}")
            print(f"       Konten   : {result['content_len']} karakter | Terkait: {result['related_count']} artikel")

        # Screenshot for failed articles only
        if result["errors"]:
            safe_name = slug.replace("/", "_")[:60]
            page.screenshot(path=f"Error_Detail_{safe_name}.png")

    page.close()
    return summary


def print_report(summary):
    print(f"\n{'=' * 60}")
    print(f"  LAPORAN AKHIR")
    print(f"{'=' * 60}")
    print(f"  Total artikel dicek : {summary['total']}")
    print(f"  ✓ Lolos             : {summary['passed']}")
    print(f"  ✗ Ada masalah       : {summary['failed']}")

    if summary["errors"]:
        print(f"\n  DETAIL ERROR:")
        for r in summary["errors"]:
            print(f"\n  URL   : {r['url']}")
            print(f"  Judul : {r['title'] or '(kosong)'}")
            for err in r["errors"]:
                print(f"    ⚠ {err}")
    else:
        print("\n  ✓ Semua artikel lolos — judul, penulis, tanggal, gambar,")
        print("    konten, bagikan, dan artikel terkait semuanya tersedia.")


if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        links   = collect_links(browser)
        summary = check_all_details(browser, links)
        print_report(summary)

        browser.close()