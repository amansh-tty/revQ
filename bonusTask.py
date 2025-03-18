import json
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

json_file = "products.json"  
csv_filename = "ulta_products.csv"

with open(json_file, "r", encoding="utf-8") as file:
    products = json.load(file)

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in background
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

headers = [
    "ASIN", "BrandName", "ProductName", "Rating", "ReviewsCount", "Price", "Currency",
    "Amazon_URL", "Ulta_URL", "Ulta_Name", "Ulta_Price", "Ulta_Rating"
]

with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()

    for product in products:
        # 🟢 Search on Ulta
        search_query = product["ProductName"].replace(" ", "+")
        search_url = f"https://www.ulta.com/search?search={search_query}"
        driver.get(search_url)
        time.sleep(5)  # Wait for JavaScript to load products

        try:
            products_list = driver.find_elements(By.CLASS_NAME, "ProductCard")

            if not products_list:
                print(f"❌ No products found for {product['ProductName']}")
                ulta_url, ulta_name, ulta_price, ulta_rating = "", "", "", ""
            else:
                first_product = products_list[0]
                ulta_url = first_product.find_element(By.TAG_NAME, "a").get_attribute("href")

                driver.get(ulta_url)
                time.sleep(3)

                try:
                    ulta_name = driver.find_element(By.CLASS_NAME, "Text-ds--title-5").text
                except:
                    ulta_name = "N/A"

                try:
                    ulta_price = driver.find_element(By.CLASS_NAME, "Text-ds--title-5").text
                except:
                    ulta_price = "N/A"

                try:
                    ulta_rating = driver.find_element(By.CLASS_NAME, "Text-ds--body-3").text
                except:
                    ulta_rating = "N/A"

        except Exception as e:
            print(f"❌ Error fetching Ulta details: {e}")
            ulta_url, ulta_name, ulta_price, ulta_rating = "", "", "", ""

        row = {
            "ASIN": product.get("ASIN", ""),
            "BrandName": product.get("BrandName", ""),
            "ProductName": product.get("ProductName", ""),
            "Rating": product.get("ratingsDict", {}).get("average_rating", ""),
            "ReviewsCount": product.get("ReviewsCount", ""),
            "Price": product.get("Price", ""),
            "Currency": product.get("Currency", ""),
            "Amazon_URL": product.get("Url", ""),
           
            "Ulta_Name": ulta_name,
            "Ulta_Price": ulta_price,
            "Ulta_Rating": ulta_rating,
             "Ulta_URL": ulta_url,
        }
        writer.writerow(row)

driver.quit()

print(f"✅ CSV file '{csv_filename}' created successfully!")
