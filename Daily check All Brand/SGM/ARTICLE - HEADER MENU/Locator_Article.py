class ArticlePage:
    def __init__(self, page):
        self.page = page
        self.url = "https://www.generasimaju.co.id/artikel?category=bunda"
        page.goto(self.url)

        # ── Main category (Tahapan) ──
        self.categoryBunda = page.locator("//div[contains(@class,'tahapan-list-item') and contains(@class,'bunda')]")
        self.categoryBayi  = page.locator("//div[contains(@class,'tahapan-list-item') and contains(@class,'bop')]")
        self.categoryAnak  = page.locator("//div[contains(@class,'tahapan-list-item') and contains(@class,'gum')]")

        # ── Topik (sub-category) ──
        self.topikImages   = page.locator("//div[contains(@class,'topik-list-image')]")
        self.topikTitles   = page.locator("//div[contains(@class,'topik-list-title')]")

        # ── Article cards ──
        self.articleCards  = page.locator("//div[contains(@class,'card__articles') and contains(@class,'col-12')]")

        # ── Pagination ──
        self.paginationList   = page.locator("//ul[@id='paginationListArticle']")
        self.pageNumberLinks  = page.locator("//ul[@id='paginationListArticle']//a[contains(@aria-label,'Page')]")
        self.btnNext          = page.locator("//a[@aria-label='Next' and not(contains(@class,'disabled'))]")

    # ── Category actions ──
    def clickCategoryBunda(self):
        self.categoryBunda.click()

    def clickCategoryBayi(self):
        self.categoryBayi.click()

    def clickCategoryAnak(self):
        self.categoryAnak.click()

    def clickCategoryByKey(self, key):
        self.page.locator(f"//div[contains(@class,'tahapan-list-item') and contains(@class,'{key}')]").click()

    # ── Topik actions ──
    def getTopikCount(self):
        return self.topikImages.count()

    def getTopikName(self, index):
        return self.topikTitles.nth(index).inner_text().strip()

    def clickTopikByIndex(self, index):
        self.topikImages.nth(index).click()

    # ── Pagination ──
    def getTotalPages(self):
        return self.pageNumberLinks.count()

    def clickPageNumber(self, page_num):
        self.page.locator(f"//ul[@id='paginationListArticle']//a[@aria-label='Page {page_num}']").click()

    def hasNextPage(self):
        return self.btnNext.count() > 0

    # ── Article cards ──
    def getArticleCount(self):
        return self.articleCards.count()

    def verifyArticleCard(self, index):
        card = self.articleCards.nth(index)

        link_href = card.locator("a").first.get_attribute("href") or ""
        title_el  = card.locator("//p[contains(@class,'card__articles-title')]")
        img_el    = card.locator("img")
        cat_el    = card.locator("//div[contains(@class,'card__articles-category')]")

        title    = title_el.inner_text().strip()  if title_el.count() > 0 else ""
        img_src  = img_el.first.get_attribute("src") if img_el.count() > 0 else ""
        category = cat_el.first.inner_text().strip() if cat_el.count() > 0 else ""

        errors = []
        if not title:     errors.append("judul kosong")
        if not img_src:   errors.append("gambar tidak ada")
        if not link_href: errors.append("link tidak ada")

        return {
            "title":    title,
            "category": category,
            "link":     link_href,
            "img":      img_src,
            "errors":   errors,
        }

    def collectAllArticleLinks(self):
        """Collect every unique article href across all categories, topik, and pages."""
        links = set()
        for cat_key in ["bunda", "bop", "gum"]:
            self.page.goto(f"https://www.generasimaju.co.id/artikel?category={cat_key}")
            self.page.wait_for_timeout(3000)
            topik_count = self.getTopikCount()
            for t_idx in range(topik_count):
                self.clickTopikByIndex(t_idx)
                self.page.wait_for_timeout(2000)
                total_pages = self.getTotalPages()
                for pg in range(1, total_pages + 1):
                    if pg > 1:
                        self.clickPageNumber(pg)
                        self.page.wait_for_timeout(2000)
                    count = self.getArticleCount()
                    for i in range(count):
                        href = self.articleCards.nth(i).locator("a").first.get_attribute("href") or ""
                        if href:
                            full = "https://www.generasimaju.co.id" + href if href.startswith("/") else href
                            links.add(full)
        return sorted(links)


class ArticleDetailPage:
    BASE = "https://www.generasimaju.co.id"

    def __init__(self, page):
        self.page = page

    def open(self, url):
        self.page.goto(url)
        self.page.wait_for_timeout(3000)

    # ── Detail element locators (resolved at call-time, not __init__) ──
    def _loc(self, xpath):
        return self.page.locator(xpath)

    def verifyDetail(self, url):
        """Navigate to article URL and verify all detail elements. Returns a result dict."""
        self.open(url)
        p = self.page
        errors = []

        # 1. H1 Title
        h1 = p.locator("//section[@id='section_content']//h1[@class='title']")
        title = h1.inner_text().strip() if h1.count() > 0 else ""
        if not title:
            errors.append("H1 judul kosong")

        # 2. Author
        author_el = p.locator("//p[@class='label-author']").first
        author = author_el.inner_text().strip() if author_el.count() > 0 else ""
        if not author:
            errors.append("Penulis tidak ada")

        # 3. Published date
        date_els = p.locator("//p[@class='label-publishing']//span[@class='date']")
        date_pub = date_els.nth(0).inner_text().strip() if date_els.count() > 0 else ""
        if not date_pub:
            errors.append("Tanggal terbit tidak ada")

        # 4. Milestone badge (e.g. Menyusui, Trimester 1)
        milestone_el = p.locator("//div[@class='badge badge-milestone']").first
        milestone = milestone_el.inner_text().strip() if milestone_el.count() > 0 else ""
        if not milestone:
            errors.append("Badge milestone tidak ada")

        # 5. Category badge (e.g. Tips, Nutrisi)
        cat_badge_el = p.locator("//div[@class='badge badge-category']").first
        cat_badge = cat_badge_el.inner_text().strip() if cat_badge_el.count() > 0 else ""
        if not cat_badge:
            errors.append("Badge kategori tidak ada")

        # 6. Hero image
        img_el = p.locator("//picture[@class='img-article-wrapper']//img").first
        img_src = img_el.get_attribute("src") if img_el.count() > 0 else ""
        img_alt = img_el.get_attribute("alt") if img_el.count() > 0 else ""
        if not img_src:
            errors.append("Gambar hero tidak ada")
        if not img_alt:
            errors.append("Alt gambar hero kosong")

        # 7. Article body content
        content_el = p.locator("//div[@class='article-content-wrapper']").first
        content_text = content_el.inner_text().strip() if content_el.count() > 0 else ""
        if not content_text:
            errors.append("Konten artikel kosong")

        # 8. Share section
        share_el = p.locator("//section[@id='section_sharing']")
        if share_el.count() == 0:
            errors.append("Bagikan section tidak ada")

        # 9. Related articles section
        related_el = p.locator("//section[@id='section_related_article']")
        related_cards = p.locator("//section[@id='section_related_article']//div[@class='card-article']")
        if related_el.count() == 0:
            errors.append("Artikel terkait section tidak ada")
        elif related_cards.count() == 0:
            errors.append("Artikel terkait tidak ada item")

        return {
            "url":       url,
            "title":     title,
            "author":    author,
            "date":      date_pub,
            "milestone": milestone,
            "category":  cat_badge,
            "img_src":   img_src,
            "img_alt":   img_alt,
            "content_len": len(content_text),
            "related_count": related_cards.count() if related_el.count() > 0 else 0,
            "errors":    errors,
        }