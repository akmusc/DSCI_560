#import necessary libraries
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

#Read the scrapped raw_file
RAW = Path("../data/raw_data/web_data.html")
OUT = Path("../data/processed_data")
BASE = "https://www.cnbc.com"

html = RAW.read_text(encoding="utf-8", errors="ignore")
soup = BeautifulSoup(html, "html.parser")


print("Reading the raw data file")
# For the latest News section
print("Filtering the news data")
news_rows = []
ul = soup.select_one("ul.LatestNews-list")
if ul:
    for li in ul.select("li.LatestNews-item"):
        a = li.select_one("a.LatestNews-headline")
        if not a: continue
        t = li.select_one("time.LatestNews-timestamp")
        ts = (t.get("datetime") or t.get_text(strip=True)) if t else ""
        title = a.get("title") or a.get_text(strip=True)
        link = urljoin(BASE, a.get("href",""))
        news_rows.append((ts, title, link))
with open(OUT/"news_data.csv","w",newline="",encoding="utf-8") as f:
    csv.writer(f).writerows([("LatestNews_timestamp","title","link"), *news_rows])
print("News data filtering complete")
# For Markets section
print("Filtering the market data")
mkt_rows = []
root = soup.select_one("div.MarketsBanner-marketData")
if root:
    for card in root.select("a.MarketCard-container"):
        sym_el = card.select_one(".MarketCard-symbol")
        pos_el = card.select_one(".MarketCard-stockPosition")
        pct_el = card.select_one(".MarketCard-changePct, .MarketCard-changesPts, .MarketCard-change")
        sym = sym_el.get_text(strip=True) if sym_el else ""
        pos = (pos_el.get_text(strip=True).replace(",","")) if pos_el else ""
        pct = pct_el.get_text(strip=True) if pct_el else ""
        mkt_rows.append((sym, pos, pct))
with open(OUT/"market_data.csv","w",newline="",encoding="utf-8") as f:
    csv.writer(f).writerows([("marketCard_symbol","marketCard_stockPosition","marketCard_changePct"), *mkt_rows])
print("Market data filtering complete")
print("Output saved and")
print("created:", OUT/"news_data.csv")
print("created:", OUT/"market_data.csv")

