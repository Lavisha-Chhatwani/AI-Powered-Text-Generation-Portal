# importing the necessary libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd


URL = "https://www.scrapethissite.com/pages/simple/" #fetching the URL
OUTPUT_FILE = "countries_data.csv"


def clean_text(text):
    return text.strip() if text else ""


def scrape_countries(url): 
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    countries = []

    country_blocks = soup.select("div.country")
    
    for country in country_blocks: #Getting country div based on country tag
        name = clean_text(country.select_one("h3.country-name").get_text())
        capital = clean_text(country.select_one("span.country-capital").get_text())
        population = clean_text(country.select_one("span.country-population").get_text())
        area = clean_text(country.select_one("span.country-area").get_text())

        countries.append({
            "Name": name,
            "Capital": capital,
            "Population": population,
            "Area": area
        })

    return countries


def main():
    try:
        data = scrape_countries(URL)

        df = pd.DataFrame(data)
        # Saving Data Frame to CSV File
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"Saved {len(df)} countries to '{OUTPUT_FILE}'")

    except requests.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()