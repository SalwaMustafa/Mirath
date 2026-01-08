from crewai.tools import tool
import requests
from bs4 import BeautifulSoup

@tool("fetch_recent_papers")
def fetch_recent_papers():
    """
    Fetches all official research categories and subcategories from arXiv's taxonomy page.
    Returns a dictionary mapping main categories to their subcategories.
    """
    url = "https://arxiv.org/category_taxonomy"
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; bot/0.1; +https://example.com/bot)"
    }
    resp = requests.get(url, headers=headers, timeout=20)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    root = soup.find(id="category_taxonomy_list")
    if not root:
        root = soup

    data = {}

    for h2 in root.find_all("h2", class_="accordion-head"):
        main_cat = h2.get_text(separator=" ", strip=True)
        body = h2.find_next_sibling("div", class_="accordion-body")
        subcats = []
        if body:
            for h4 in body.find_all("h4"):
                code_node = h4.find(text=True, recursive=False)
                code = code_node.strip() if code_node else ""
               
                span = h4.find("span")
                if span:
                    name = span.get_text(strip=True)
                    name = name.strip("() ").strip()
                else:
                    full = h4.get_text(separator=" ", strip=True)
                    name = full.replace(code, "").strip(" -()")
                if code or name:
                    entry = f"{code} :{name}" if code and name else (code or name)
                    subcats.append(entry)
        if subcats:
            data[main_cat] = subcats

    return data


