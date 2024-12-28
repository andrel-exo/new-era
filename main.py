import json
import requests
from bs4 import BeautifulSoup
import time

# File to store communicated houses
COMMUNICATED_HOUSES_FILE = "communicated_houses.json"

# Telegram bot credentials
BOT_TOKEN = "6286089541:AAFXN0DJsBEI_a5RnoyQxct6m8hfv5CjrBg"
BOT_CHAT_ID = "-4718672043"


def send_message(bot_token, bot_chat_id, bot_message):
    """Send a message via Telegram."""
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        "chat_id": bot_chat_id,
        "text": bot_message,
        "parse_mode": "Markdown",
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f"Failed to send message. Status code: {response.status_code}")
    else:
        print("Message sent successfully!")


def load_communicated_houses():
    """Load previously communicated houses from a JSON file."""
    try:
        with open(COMMUNICATED_HOUSES_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_communicated_houses(houses):
    """Save communicated houses to a JSON file."""
    with open(COMMUNICATED_HOUSES_FILE, "w") as file:
        json.dump(houses, file, indent=4)


def fetch_new_listings():
    """Fetch the newest listings from the website."""
    url = "https://www.idealista.pt/comprar-casas/maia/com-preco-max_280000,preco-min_180000,t2,t3"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    listings = soup.select("article.item")
    new_houses = []

    for listing in listings:
        try:
            house_id = listing.get("data-element-id")
            title = listing.select_one(".item-link").get_text(strip=True)
            price = listing.select_one(".item-price").get_text(strip=True)
            location = listing.select_one(".item-link")["title"]
            link = f"https://www.idealista.pt{listing.select_one('.item-link')['href']}"
            details = [d.get_text(strip=True) for d in listing.select(".item-detail")]
            typology = details[0] if len(details) > 0 else None
            area = details[1] if len(details) > 1 else None
            floor = details[2] if len(details) > 2 else None
            description = listing.select_one(".item-description p").get_text(strip=True) if listing.select_one(
                ".item-description p") else None
            garage = listing.select_one(".item-parking").get_text(strip=True) if listing.select_one(
                ".item-parking") else None

            new_houses.append({
                "id": house_id,
                "title": title,
                "price": price,
                "location": location,
                "link": link,
                "typology": typology,
                "area": area,
                "floor": floor,
                "description": description,
                "garage": garage,
            })
        except Exception as e:
            print(f"Error processing a listing: {e}")

    return new_houses


def detect_new_houses(new_listings, communicated_houses):
    """Detect new houses that haven't been communicated yet."""
    new_notifications = []
    for house in new_listings:
        if house["id"] not in communicated_houses:
            new_notifications.append(house)
    return new_notifications


def main():
    while True:
        # Load previously communicated houses
        communicated_houses = load_communicated_houses()

        # Fetch the newest listings
        new_listings = fetch_new_listings()

        # Detect new houses
        new_houses = detect_new_houses(new_listings, communicated_houses)

        if new_houses:
            print("New houses detected:")
            for house in new_houses:
                message = (
                    f"*Title:* {house['title']}\n"
                    f"*Price:* {house['price']}\n"
                    f"*Location:* {house['location']}\n"
                    f"*Link:* {house['link']}\n"
                    f"*Typology:* {house.get('typology', 'N/A')}\n"
                    f"*Area:* {house.get('area', 'N/A')}\n"
                    f"*Floor:* {house.get('floor', 'N/A')}\n"
                    f"*Description:* {house.get('description', 'N/A')}\n"
                    f"*Garage:* {house.get('garage', 'N/A')}\n"
                )
                send_message(BOT_TOKEN, BOT_CHAT_ID, message)

                # Add to communicated houses
                communicated_houses[house["id"]] = house
        else:
            print("No new houses detected.")

        # Save updated communicated houses
        save_communicated_houses(communicated_houses)

        # Wait for 5 minutes before checking again
        time.sleep(900)


if __name__ == "__main__":
    print("Starting the script. Press Ctrl+C to stop.")
    main()
