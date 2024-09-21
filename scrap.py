import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv, json
import os
from bs4 import BeautifulSoup


# Define file paths
json_file = "processed_links.json"
csv_file = "scraped_data.csv"

# Initialize JSON file if not present
if not os.path.exists(json_file):
    with open(json_file, 'w') as file:
        json.dump({}, file)

# Load the processed links
with open(json_file, 'r') as file:
    processed_links = json.load(file)

def save_to_json(data):
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)
    print("Processed links saved to JSON.")

def save_to_csv(data):
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Name', 'Phone', 'Address'])  # Write header if file is new
            print("CSV header written.")
        writer.writerow(data)
    print(f"Data saved to CSV: {data}")

def scrape_category(link):
    print(f"Starting to scrape link: {link}")
    
    driver.get(link)
    print(f"Page loaded: {link}")
    input("Press Enter when the page is fully loaded and ready for scraping")
    
    # Wait for the table to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "myTable"))
        )
        print("Table with ID 'myTable' found.")
        
        # Get page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        print("Page source parsed with BeautifulSoup.")
        
        table = soup.find('table', id='myTable')
        tbody = table.find('tbody')
        rows = tbody.find_all('tr')
        
        print(f"Number of rows found: {len(rows)}")
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 4:
                name = cols[1].get_text(strip=True)
                phone = cols[2].get_text(strip=True)
                address = cols[3].get_text(strip=True)
                save_to_csv([name, phone, address])
        
        processed_links[link] = True
        save_to_json(processed_links)
        
        print(f"Link {link} processed successfully.")
    except Exception as e:
        print(f"Error processing {link}: {str(e)}")

# Setup Chrome driver with JavaScript disabled
options = uc.ChromeOptions()
options.headless = False
# Disable JavaScript
prefs = {
    "profile.managed_default_content_settings.javascript": 2,
    "profile.managed_default_content_settings.images": 2  # 2 disables images
} # 2 disables JavaScript
options.add_experimental_option("prefs", prefs)

driver = uc.Chrome(options=options)
print("ChromeDriver initialized with JavaScript disabled.")
# The main link to scrape
main_link = "https://medicaldirectory.co.za/home/by_cat/2"

while True:
    choice = input("Do you want to process the current link? (y for yes, n for no): ").lower()
    if choice == "y":
        scrape_category(main_link)
        print("Ready for new link.")
    elif choice == "n":
        print("If you want to process a new link, click on it in the browser, then press Enter.")
        input("Press Enter to continue after selecting a new link...")
        print("Processing new link...")
        scrape_category(driver.current_url)
    else:
        
        break

# Cleanup
driver.quit()
print("ChromeDriver session ended.")
