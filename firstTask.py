import requests
from bs4 import BeautifulSoup
from colorama import init, Fore, Style

init(autoreset=True)

url = "https://iliabeauty.com/products/balmy-tint-hydrating-tinted-lip-balm#d"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

h1_tag = soup.find('h1', class_="tw-font-serif-light tw-text-[1.563rem] tw-leading-[1.2] tw-col-span-full lg:tw-text-[1.953rem]")
product_name = h1_tag.get_text(strip=True) if h1_tag else "Product name not found"

shade_tag = soup.find('p', class_="tw-font-sans tw-font-medium tw-uppercase tw-text-quicksand tw-text-[.88rem] tw-leading-[1.4] tw-tracking-[.04em] tw-pt-4 lg:tw-pt-0")
shade = shade_tag.get_text(strip=True) if shade_tag else "Shade not found"

price_tag = soup.find('p', class_="tw-font-sans tw-font-medium tw-text-base")
price = "Price not found"
if price_tag:
    price_span = price_tag.find('span', attrs={"x-text": "activeVariant.price_str"})
    if price_span:
        price = price_span.get_text(strip=True)

rating_div = soup.find('div', class_="product-rating product-rating--with-label tw-text-right")
rating = "Rating not found"
review_count = "Reviews not found"

if rating_div:
    rating_value = rating_div.find('div', class_="oke-sr-rating")
    rating = rating_value.get_text(strip=True) if rating_value else rating

    review_count_value = rating_div.find('div', class_="oke-sr-count")
    review_count = review_count_value.get_text(strip=True) if review_count_value else review_count

desc_div = soup.find('div', class_="accordion__panel tw-px-4 tw-pb-4 tw-text-base tw-prose tw-prose-kabul prose-a:tw-font-normal prose-a:tw-transition-colors lg:hover:prose-a:tw-text-cocoa prose-li:tw-leading-[1.4] tw-tracking-[0.075rem]")
product_description = "Description not found"
if desc_div:
    descriptions = [p.get_text(strip=True) for p in desc_div.find_all('p')]
    product_description = " ".join(descriptions)

reviews = soup.find_all("li", class_="oke-w-reviews-list-item")

print(f"\n{Fore.CYAN}{'='*40}")
print(f"{Fore.YELLOW} PRODUCT DETAILS")
print(f"{Fore.CYAN}{'='*40}")
print(f"{Fore.GREEN} Product Name: {Fore.RESET}{product_name}")
print(f"{Fore.MAGENTA} Shade: {Fore.RESET}{shade}")
print(f"{Fore.RED} Price: {Fore.RESET}{price}")
print(f"{Fore.YELLOW} Rating: {Fore.RESET}{rating}")
print(f"{Fore.BLUE} Number of Reviews: {Fore.RESET}{review_count}")
print(f"{Fore.CYAN}{'='*40}")
print(f"{Fore.LIGHTGREEN_EX} Product Description: {Fore.RESET}{product_description[:500]}...")  # Truncate long descriptions
print(f"{Fore.CYAN}{'='*40}\n")


reviews = soup.find_all("li", class_="oke-w-reviews-list-item")

csv_filename = "reviews.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "Reviewer Name", "Rating", "Review Title", "Review Body",
        "Date of Review", "Verified Buyer", "Skin Type", "Concerns",
        "Skin Tone", "Undertone", "Eye Color", "Age Range"
    ])

    for index, review in enumerate(reviews):

            reviewer_name = review.find("strong", class_="oke-w-reviewer-name")
            reviewer_name = reviewer_name.text.strip() if reviewer_name else "Anonymous"

            rating_element = review.find("span", class_="oke-a11yText")
            rating = rating_element.text.strip() if rating_element else "No rating"

            review_title = review.find("div", class_="oke-reviewContent-title oke-title")
            review_title = review_title.text.strip() if review_title else "No title"

            review_body = review.find("div", class_="oke-reviewContent-body oke-bodyText")
            review_body = review_body.text.strip() if review_body else "No review text"

            date_of_review = review.find("div", class_="oke-reviewContent-date")
            date_of_review = date_of_review.text.strip() if date_of_review else "Unknown date"

            verified_buyer = "Yes" if review.find("div", class_="oke-w-reviewer-verified") else "No"

            attr_map = {
                "Skin Type": "Not specified",
                "Concerns": "Not specified",
                "Skin Tone": "Not specified",
                "Undertone": "Not specified",
                "Eye Color": "Not specified",
                "Age Range": "Not specified"
            }

            attributes = review.find_all("div", class_="oke-w-selectAttr-item")

            for attr in attributes:
                title_element = attr.find("strong", class_="oke-w-selectAttr-item-title")
                value_element = attr.find("span", class_="oke-w-selectAttr-item-value")

                if title_element and value_element:
                    title = title_element.text.strip()
                    value = value_element.text.strip()
                    if title in attr_map:
                        attr_map[title] = value

            skin_type = attr_map["Skin Type"]
            concerns = attr_map["Concerns"]
            skin_tone = attr_map["Skin Tone"]
            undertone = attr_map["Undertone"]
            eye_color = attr_map["Eye Color"]
            age_range = attr_map["Age Range"]

            writer.writerow([
                reviewer_name, rating, review_title, review_body, date_of_review,
                verified_buyer, skin_type, concerns, skin_tone, undertone, eye_color, age_range
            ])

print(f"Reviews successfully saved to {csv_filename}")

