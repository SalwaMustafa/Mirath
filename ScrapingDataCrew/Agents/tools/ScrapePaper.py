from bs4 import BeautifulSoup
import requests
import os
import json
import time
import random
from crewai.tools import tool

@tool("scrape_paper")
def scrape_paper(url_abs: str):
    """
    Scrapes the full content of a research paper from its arXiv abstract page link.
    Returns a dictionary containing the paper's 'title', 'authors', 'citation', 
    'publishedAt', 'category', 'abstract', and 'content'.
    """

    headers = {"User-Agent": f"Mozilla/5.0 (compatible; Bot/{random.randint(1000,9999)})"}
    url = url_abs.replace("/abs/", "/html/")

    response = requests.get(url, headers=headers, timeout=30)

    if response.status_code == 404:
        return {}     
    
    soup = BeautifulSoup(response.text, "html.parser")

    response_abs = requests.get(url_abs, headers=headers, timeout=30)
    soup_abs = BeautifulSoup(response_abs.text, "html.parser")

    dateline_div = soup_abs.find("div", class_="dateline")
    pub_date = dateline_div.get_text(strip=True) if dateline_div else None

    title_h1 = soup_abs.find("h1", class_="title mathjax")
    title_text = None
    if title_h1:
        title_text = title_h1.get_text(strip=True)

    abstract_block = soup_abs.find("blockquote", class_="abstract mathjax")
    abstract_text = abstract_block.get_text(strip=True)

    authors_div = soup_abs.find("div", class_="authors")

    authors_list = []
    if authors_div:
        authors_list = [a.get_text(strip=True) for a in authors_div.find_all("a")]

    metatable = soup_abs.find("div", class_="metatable")
    subjects = None
    cite_as = None

    if metatable:
        for row in metatable.find_all("tr"):
            label_td = row.find("td", class_="tablecell label")
            value_td = row.find("td", class_="tablecell subjects") or row.find("td", class_="tablecell arxivid")

            if label_td and value_td:
                label_text = label_td.get_text(strip=True).lower()

                if "subjects" in label_text:
                    subjects = [s.get_text(strip=True) for s in value_td.find_all("span", class_="primary-subject")]
                    secondary = value_td.get_text(strip=True).split(";")
                    secondary = [s.strip() for s in secondary if s.strip() not in subjects]
                    subjects.extend(secondary)

                if "cite as" in label_text:
                    cite_link = value_td.find("a")
                    cite_as = cite_link.get_text(strip=True) if cite_link else value_td.get_text(strip=True)


    target = soup.find("div", {"class": "ltx_page_main"})

    if not target:
        return {} 

    if target:
        for img in target.find_all("img"):
                src = img.get("src")
                if src:
                    img["src"] = f"{url}/{src}"

    try:
        html_content = f"""<html><head><link rel="stylesheet" href="https://arxiv.org/static/browse/0.3.4/css/arxiv-html-papers-20250916.css"></head>{target.decode()}</html>"""

    except:
        return {}


    content_lines = [line for line in html_content.splitlines() if line.strip()]
    for line in content_lines:
        line = line.replace("\n","")

    return {
        "title" : title_text,
        "authors" : authors_list,
        "citation" : cite_as,
        "publichedAt" : pub_date,
        "category": subjects,
        "abstract" : abstract_text,
        "content": content_lines
    }
