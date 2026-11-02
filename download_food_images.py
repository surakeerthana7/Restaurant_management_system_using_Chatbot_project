
import os
import re
import time
import requests
from pathlib import Path
from pymongo import MongoClient
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / "back_end" / ".env")

client = MongoClient(os.getenv("MONGO_URL", "mongodb://localhost:27017/"))
db = client["restaurant_management"]
menu_collection = db["menuitems"]

IMAGE_FOLDER = BASE_DIR / "front_end" / "public" / "food"
IMAGE_FOLDER.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "RestaurantManagementStudentProject/1.0 (educational use)"
}

# Alternative search terms for missing dishes
SEARCH_TERMS = {
    "Rasmalai": ["rasmalai indian dessert", "ras malai sweets"],
    "Oreo Milkshake": ["oreo milkshake glass", "cookies cream milkshake"],
    "Chicken Biryani": ["chicken biryani indian rice", "hyderabadi chicken biryani"],
    "Veg Fried Rice": ["vegetable fried rice", "indian veg fried rice"],
    "Chocolate Cake": ["chocolate cake slice", "chocolate layer cake"],
    "Chicken 65": ["chicken 65 indian food", "indian spicy fried chicken"],
    "Veg Manchurian": ["vegetable manchurian gravy", "veg manchurian dry"],
    "Mutton Biryani": ["mutton biryani indian", "lamb biryani rice"],
    "Gulab Jamun": ["gulab jamun indian dessert", "gulab jamun sweets"],
    "Vanilla Ice Cream": ["vanilla ice cream scoop", "vanilla ice cream bowl"],
    "Fresh Lime Soda": ["lime soda drink glass", "fresh lime soda india"],
    "Chicken Fried Rice": ["chicken fried rice", "fried rice with chicken"],
    "Paneer Fried Rice": ["paneer fried rice", "indian cottage cheese fried rice"],
    "Mango Lassi": ["mango lassi indian drink", "mango yogurt smoothie"],
    "Veg Pulao": ["vegetable pulao rice", "indian veg pulao"]
}


def make_filename(name):
    name = name.lower().replace("&", "and")
    name = re.sub(r"[^a-z0-9]+", "_", name)
    return name.strip("_") + ".jpg"


def search_image(search_term):
    url = "https://commons.wikimedia.org/w/api.php"

    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": search_term + " filetype:bitmap",
        "gsrnamespace": 6,
        "gsrlimit": 15,
        "prop": "imageinfo",
        "iiprop": "url|mime",
        "iiurlwidth": 700,
        "format": "json"
    }

    response = requests.get(
        url, params=params, headers=HEADERS, timeout=30
    )
    response.raise_for_status()

    pages = response.json().get("query", {}).get("pages", {})

    for page in pages.values():
        info = page.get("imageinfo", [{}])[0]
        image_url = info.get("thumburl") or info.get("url")
        mime = info.get("mime", "")

        if image_url and mime.startswith("image/"):
            return image_url

    return None


def download_food(food):
    name = food["name"]
    filename = make_filename(name)
    image_path = IMAGE_FOLDER / filename

    if image_path.exists() and image_path.stat().st_size > 1000:
        menu_collection.update_one(
            {"_id": food["_id"]},
            {"$set": {"image": f"/food/{filename}"}}
        )
        print("Already downloaded:", name)
        return True

    terms = SEARCH_TERMS.get(name, [name + " food photograph"])

    for term in terms:
        try:
            print(f"Searching {name}: {term}")

            image_url = search_image(term)

            if not image_url:
                time.sleep(1)
                continue

            response = requests.get(
                image_url, headers=HEADERS, timeout=30
            )
            response.raise_for_status()

            if not response.headers.get("Content-Type", "").startswith("image/"):
                continue

            if len(response.content) < 5000:
                continue

            image_path.write_bytes(response.content)

            menu_collection.update_one(
                {"_id": food["_id"]},
                {"$set": {"image": f"/food/{filename}"}}
            )

            print("Downloaded:", name)
            time.sleep(1)
            return True

        except requests.RequestException as error:
            print("Error:", error)

        time.sleep(1)

    print("FAILED:", name)
    return False


def main():
    foods = list(menu_collection.find({}))
    failed = []

    print("Total food items:", len(foods))

    for food in foods:
        if not download_food(food):
            failed.append(food["name"])

    print("\n========== FINAL RESULT ==========")
    print("Total food items:", len(foods))
    print("Downloaded or already present:", len(foods) - len(failed))
    print("Still missing:", len(failed))

    for name in failed:
        print("-", name)


if __name__ == "__main__":
    main()

def fix_last_two_images():
    foods_to_fix = {
        "Mango Lassi": [
            "mango lassi indian yogurt drink",
            "mango lassi in glass",
            "mango yogurt drink"
        ],
        "Veg Pulao": [
            "vegetable pulao indian rice",
            "vegetable pilaf rice",
            "indian vegetable rice pulao"
        ]
    }

    for name, search_terms in foods_to_fix.items():
        food = menu_collection.find_one({"name": name})

        if not food:
            print("Food not found:", name)
            continue

        filename = make_filename(name)
        image_path = IMAGE_FOLDER / filename
        downloaded = False

        for term in search_terms:
            try:
                print("Searching:", term)
                image_url = search_image(term)

                if not image_url:
                    continue

                response = requests.get(
                    image_url,
                    headers=HEADERS,
                    timeout=30
                )
                response.raise_for_status()

                if not response.headers.get("Content-Type", "").startswith("image/"):
                    continue

                if len(response.content) < 5000:
                    continue

                image_path.write_bytes(response.content)

                menu_collection.update_one(
                    {"_id": food["_id"]},
                    {"$set": {"image": f"/food/{filename}"}}
                )

                print("SUCCESS:", name)
                downloaded = True
                break

            except requests.RequestException as error:
                print("Error:", error)

        if not downloaded:
            print("Still missing:", name)


if __name__ == "__main__":
    fix_last_two_images()
