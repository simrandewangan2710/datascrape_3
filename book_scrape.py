from playwright.sync_api import sync_playwright
import pandas as pd
from get_data import getBookData

if __name__ == "__main__":
    # collect data across pages
    all_dfs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Scrape the first page (homepage)
        page.goto('https://books.toscrape.com/')
        books = page.query_selector_all('article.product_pod')
        all_dfs.append(getBookData(books))

        # Scrape pages 2 to 50
        for each_page in range(2, 51):
            url = f'https://books.toscrape.com/catalogue/page-{each_page}.html'
            page.goto(url)
            books = page.query_selector_all('article.product_pod')
            if not books:
                break
            all_dfs.append(getBookData(books))

        browser.close()

    # combine and output
    if all_dfs:
        combined = pd.concat(all_dfs, ignore_index=True)
        out_file = 'books.csv'
        combined.to_csv(out_file, index=False)
        print(f"wrote {len(combined)} rows to {out_file}")
