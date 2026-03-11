import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
import random
import os

def scrape_otodom_page(page_number):
    url = f"https://www.otodom.pl/pl/wyniki/wynajem/mieszkanie/mazowieckie/warszawa/warszawa/warszawa?ownerTypeSingleSelect=ALL&page={page_number}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,pl;q=0.8"
    }
    
    print(f"Fetching page {page_number}...")
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Status code {response.status_code} on page {page_number}")
        return None
        
    soup = BeautifulSoup(response.text, 'html.parser')
    script_tag = soup.find("script", id="__NEXT_DATA__")
    
    if not script_tag:
        print(f"Error: __NEXT_DATA__ not found on page {page_number}.")
        return None
        
    try:
        data = json.loads(script_tag.string)
        items = data['props']['pageProps']['data']['searchAds']['items']
        
        # Stop condition: if items list is empty, we reached the end of the results
        if not items:
            return []
            
        flats_list = []
        for item in items:
            locations = item.get('location', {}).get('reverseGeocoding', {}).get('locations', [])
            district_name = locations[2].get('fullName') if len(locations) > 2 else (locations[0].get('fullName') if locations else None)

            flat = {
                'id': item.get('id'),
                'title': item.get('title'),
                'price': item.get('totalPrice', {}).get('value') if item.get('totalPrice') else None,
                'currency': item.get('totalPrice', {}).get('currency') if item.get('totalPrice') else None,
                'area': item.get('areaInSquareMeters'),
                'rooms': item.get('roomsNumber'),
                'district': district_name,
                'url': f"https://www.otodom.pl/pl/oferta/{item.get('slug')}" if item.get('slug') else None
            }
            flats_list.append(flat)
            
        return flats_list
        
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error parsing JSON on page {page_number}: {e}")
        return None

# --- Main Execution Block ---
if __name__ == "__main__":
    csv_filename = "warsaw_rentals_raw.csv"
    state_filename = "last_page.txt"
    
    # 1. Read the last processed page to know where to start
    start_page = 1
    if os.path.exists(state_filename):
        with open(state_filename, "r") as f:
            content = f.read().strip()
            if content.isdigit():
                start_page = int(content)
                
    pages_to_scrape = 55
    end_page = start_page + pages_to_scrape - 1
    
    print(f"Starting from page {start_page}. Target end page: {end_page}")
    
    # 2. Loop through the pages
    for page in range(start_page, end_page + 1):
        flats_on_page = scrape_otodom_page(page)
        
        # Hard stop if we get blocked or structure changes
        if flats_on_page is None:
            print("Stopping script due to an error (possible block or layout change).")
            break
            
        # Hard stop if we reached the last page of Otodom
        if len(flats_on_page) == 0:
            print(f"\nNo more listings found on page {page}. Reached the absolute end!")
            break
            
        # 3. Append directly to CSV
        df = pd.DataFrame(flats_on_page)
        
        # Check if CSV exists to decide whether to write headers
        file_exists = os.path.exists(csv_filename)
        df.to_csv(csv_filename, mode='a', index=False, header=not file_exists, encoding='utf-8')
        
        print(f"Saved {len(flats_on_page)} listings from page {page} to {csv_filename}.")
        
        # 4. Update the state file to next page AFTER successful save
        with open(state_filename, "w") as f:
            f.write(str(page + 1))
        
        # 5. Sleep between requests (skip sleep after the very last page in the loop)
        if page < end_page:
            sleep_time = random.uniform(2.5, 5.5)
            print(f"Sleeping for {sleep_time:.2f} seconds...\n")
            time.sleep(sleep_time)

    print("-" * 50)
    print("Batch finished. Run the script again to scrape the next batch.")