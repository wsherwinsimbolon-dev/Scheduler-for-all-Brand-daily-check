
"""
==============================================
  PLAYWRIGHT PYTHON - ARTICLE HEADER MENU
  Skenario: Cek semua artikel pada setiap kategori dan topik
  URL     : https://www.generasimaju.co.id/artikel?category=bunda
  Catatan : Halaman tidak memiliki filter tahun. Pengecekan dilakukan
            per kategori (Bunda/Bayi/Anak) x topik x halaman paginasi.
==============================================
"""

from playwright.sync_api import sync_playwright
from Locator_Article import ArticlePage

CATEGORIES = [
    {"key": "bunda", "label": "Bunda"},
    {"key": "bop",   "label": "Bayi"},
    {"key": "gum",   "label": "Anak"},
]


def check_articles_on_page(locator, category_label, topik_name, page_num, summary):
    count = locator.getArticleCount()
    if count == 0:
        print(f"    ⚠ Tidak ada artikel ditemukan")
        return

    for i in range(count):
        result = locator.verifyArticleCard(i)
        summary["total"] += 1

        if result["errors"]:
            summary["errors"].append({
                "category": category_label,
                "topik":    topik_name,
                "page":     page_num,
                "title":    result["title"] or "(no title)",
                "issues":   result["errors"],
            })
            print(f"    ✗ [{i+1}] {result['title'] or '(no title)'} — {result['errors']}")
        else:
            print(f"    ✓ [{i+1}] {result['category']} | {result['title'][:60]}")


def check_all_articles():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        summary = {"total": 0, "errors": []}

        locator = ArticlePage(page)
        print(f"✓ Membuka: {locator.url}")
        page.wait_for_timeout(4000)

        for cat in CATEGORIES:
            print(f"\n{'='*60}")
            print(f"  KATEGORI: {cat['label']} ({cat['key']})")
            print(f"{'='*60}")

            # Navigate to category URL directly to reset state
            page.goto(f"https://www.generasimaju.co.id/artikel?category={cat['key']}")
            page.wait_for_timeout(4000)

            # Get topik count for this category
            topik_count = locator.getTopikCount()
            print(f"  Jumlah topik: {topik_count}")

            for t_idx in range(topik_count):
                topik_name = locator.getTopikName(t_idx)
                print(f"\n  -- Topik [{t_idx+1}/{topik_count}]: {topik_name} --")

                locator.clickTopikByIndex(t_idx)
                page.wait_for_timeout(3000)

                total_pages = locator.getTotalPages()
                print(f"     Total halaman: {total_pages}")

                for pg in range(1, total_pages + 1):
                    if pg > 1:
                        locator.clickPageNumber(pg)
                        page.wait_for_timeout(3000)

                    art_count = locator.getArticleCount()
                    print(f"     Halaman {pg}: {art_count} artikel")
                    check_articles_on_page(locator, cat['label'], topik_name, pg, summary)

                page.screenshot(path=f"Article_{cat['key']}_{topik_name.replace(' ','_')}.png")

        # ── Final Report ──
        print(f"\n{'='*60}")
        print(f"  HASIL PENGECEKAN")
        print(f"{'='*60}")
        print(f"  Total artikel dicek : {summary['total']}")
        print(f"  Total error         : {len(summary['errors'])}")

        if summary["errors"]:
            print(f"\n  DAFTAR ERROR:")
            for err in summary["errors"]:
                print(f"  - [{err['category']}] Topik: {err['topik']} | Hal: {err['page']}")
                print(f"    Judul : {err['title']}")
                print(f"    Masalah: {err['issues']}")
        else:
            print("  ✓ Semua artikel lolos pengecekan (judul, gambar, link tersedia)")

        browser.close()
        return summary


if __name__ == "__main__":
    check_all_articles()