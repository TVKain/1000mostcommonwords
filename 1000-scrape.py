import requests
from bs4 import BeautifulSoup
import json
import sys

def scrape_words(url, lang_code, output_file="words.json"):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Select all rows and skip the first header row
    rows = soup.select("tr")[1:]

    words_list = []
    for tr in rows:
        tds = tr.find_all("td")
        if len(tds) >= 3:
            foreign_word = tds[1].get_text(strip=True)
            english_word = tds[2].get_text(strip=True).lower()
            if foreign_word and english_word:
                words_list.append({lang_code: foreign_word, "eng": english_word})

    if words_list:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(words_list, f, ensure_ascii=False, indent=2)
        print(f"Scraped {len(words_list)} words. Saved to {output_file}")
    else:
        print("No words found. Check the URL format.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scrape_words.py <URL> <lang_code> [output_file.json]")
    else:
        url = sys.argv[1]
        lang_code = sys.argv[2]
        output_file = sys.argv[3] if len(sys.argv) > 3 else "words.json"
        scrape_words(url, lang_code, output_file)
