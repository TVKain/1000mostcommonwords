import requests
from bs4 import BeautifulSoup
import json
import sys
from nltk.corpus import words
import nltk
import os

# Ensure the words corpus is available
nltk.download('words', quiet=True)

def scrape_words(url, lang_code, output_file="words.json"):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    rows = soup.select("tr")[1:]  # Skip header row
    if not rows:
        print("No rows found in the table. Check the page structure.")
        return

    english_words = set(words.words())
    seen = set()
    words_list = []

    skip_dupe = 0
    skip_english = 0

    for tr in rows:
        tds = tr.find_all("td")
        if len(tds) >= 3:
            foreign_word = tds[1].get_text(strip=True).lower()
            english_word = tds[2].get_text(strip=True).lower()
            if foreign_word and english_word:
                # Skip if foreign word looks like English
                if foreign_word in english_words:
                    skip_english += 1
                    continue

                # Skip duplicates
                if foreign_word in seen:
                    skip_dupe += 1
                    continue

                words_list.append({lang_code: foreign_word, "eng_Latn": english_word})
                seen.add(foreign_word)

    print(f"Skip dupe: {skip_dupe}")
    print(f"Skip in english: {skip_english}")
    if words_list:
        final_data = words_list
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(final_data, f, ensure_ascii=False, indent=2)
        print(f"Scraped {len(words_list)} new words. Total now: {len(final_data)}. Saved to {output_file}")
    else:
        print("No new words found.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python 1000-scrape.py <URL> <lang_code> [output_file.json]")
    else:
        url = sys.argv[1]
        lang_code = sys.argv[2]
        output_file = sys.argv[3] if len(sys.argv) > 3 else "words.json"
        scrape_words(url, lang_code, output_file)
