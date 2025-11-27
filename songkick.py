import requests
from bs4 import BeautifulSoup
import csv
import time
import json
from typing import List, Dict, Any

def scrape_gigography(base_url, filename = "songkick_gigography.csv"):
    gigs = []
    current_page = 1
    unique_gig_keys = set()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print(f"Starting scrape from {base_url}")

    while True:
        url = f"{base_url}?page={current_page}"
        print(f"Scraping page {current_page} at {url}")

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            json_ld_scripts = soup.find_all('script', {'type': 'application/ld+json'})
            
            events_on_page = []
            for script in json_ld_scripts:
                try:
                    data = json.loads(script.string)
                    if isinstance(data, list):
                        events_on_page.extend(data)
                except (json.JSONDecodeError, AttributeError):
                    continue
            
            new_gigs_added = 0
            
            for event in events_on_page:
                if event.get('@type') != 'MusicEvent':
                    continue

                try:
                    start_date = event.get('startDate', 'N/A')
                    date = start_date.split('T')[0] if 'T' in start_date else start_date
                    
                    event_name = event.get('name', 'N/A')
                    
                    venue = event.get('location', {}).get('name', 'N/A')
                    
                    address = event.get('location', {}).get('address', {})
                    locality = address.get('addressLocality', '')
                    country = address.get('addressCountry', '')
                    location = f"{locality}, {country}".strip(', ')
                    
                    gig_key = f"{date}|{event_name}|{venue}"
                    
                    if gig_key not in unique_gig_keys:
                        gigs.append({
                            'Date': date,
                            'Event Name': event_name,
                            'Venue': venue,
                            'Location': location
                        })
                        unique_gig_keys.add(gig_key)
                        new_gigs_added += 1
                    
                except Exception as e:
                    print(f"Error parsing event entry on page {current_page}: {e}")
                    continue

            if new_gigs_added == 0:
                print(f"Page {current_page} contained duplicate or no new gig data (0 unique gigs added). Ending scrape.")
                break

            current_page += 1
            
            time.sleep(1.5) 

        except requests.exceptions.HTTPError as errh:
            print (f"HTTP Error on page {current_page}: {errh.response.status_code}. Ending scrape.")
            break
        except requests.exceptions.RequestException as err:
            print (f"An unexpected error occurred during page fetch: {err}. Ending scrape.")
            break

    print(f"\nScraping complete. Found {len(gigs)} unique gigs. Writing to {filename}...")
    if gigs:
        keys = ['Date', 'Event Name', 'Venue', 'Location']
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as output_file:
                dict_writer = csv.DictWriter(output_file, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(gigs)
            print(f"✅ Successfully created and saved data to {filename}")
        except Exception as e:
            print(f"Error writing to CSV file: {e}")
    else:
        print("❌ No gig data was successfully scraped.")

GIGOGRAPHY_URL = "https://songkick.com/users/outspaced/gigography" 

if __name__ == '__main__':
    scrape_gigography(GIGOGRAPHY_URL)