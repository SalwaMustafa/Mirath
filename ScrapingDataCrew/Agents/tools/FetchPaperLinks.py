import requests
import xml.etree.ElementTree as ET
from crewai.tools import tool

@tool("search_arxiv_by_category_code")
def search_arxiv_by_category_code(category_code: str, max_results: int = 1) -> list[dict]:
    """
    Searches the arXiv API for recent papers using a specific category code (e.g., 'cs.AI').
    Returns a list of dictionaries, where each dictionary contains the paper's 'title' and 'link'.
    
    Args:
        category_code: The arXiv category code (e.g., 'cs.AI', 'math.CO')
        max_results: Maximum number of results to return (default: 1)
    
    Returns:
        List of dictionaries with 'title' and 'link' keys
    """
    
    base_url = "http://export.arxiv.org/api/query?"
    query = f"search_query=cat:{category_code}&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
    
    print(f"[Tool] Searching API for: {category_code} (max: {max_results}) ...")
    
    papers_list = []
    
    try:
        response = requests.get(base_url + query, timeout=15)
        response.raise_for_status() 
        namespaces = {'atom': 'http://www.w3.org/2005/Atom'}
        root = ET.fromstring(response.content)

        for entry in root.findall('atom:entry', namespaces):
            title_elem = entry.find('atom:title', namespaces)
            link_elem = entry.find('atom:link[@rel="alternate"]', namespaces) 

            if title_elem is not None and title_elem.text and link_elem is not None:
                title = ' '.join(title_elem.text.strip().split())
                link = link_elem.get('href')
                papers_list.append({
                    'title': title,
                    'link': link,
                    'category': category_code
                })
        
        if not papers_list:
            print(f"[Tool] No papers found for: {category_code}")
            return []
            
        print(f"[Tool] Found {len(papers_list)} papers for: {category_code}")
        return papers_list

    except requests.RequestException as e:
        print(f"[Tool] Network error for {category_code}: {e}")
        return []
    except ET.ParseError as e:
        print(f"[Tool] XML parsing error for {category_code}: {e}")
        return []
    except Exception as e:
        print(f"[Tool] Unexpected error for {category_code}: {e}")
        return []