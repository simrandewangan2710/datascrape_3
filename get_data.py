from playwright.sync_api import ElementHandle
import pandas as pd


def getBookData(books: list[ElementHandle]) -> pd.DataFrame:
    """Extracts book title and price from a list of book element handles.
    Returns a DataFrame containing the data.
    """
    records = []
    for book in books:
        try:
            title = book.query_selector('h3 a').get_attribute('title')
        except Exception:
            title = None
        try:
            price = book.query_selector('.price_color').inner_text()
        except Exception:
            price = None
        records.append({"title": title, "price": price})

    df = pd.DataFrame(records)
    # you could save or return; printing for quick feedback
    print(df)
    return df
