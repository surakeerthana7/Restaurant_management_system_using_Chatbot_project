import os
import requests
import time

# Folder to save food images
folder = "front_end/src/assets/food"
os.makedirs(folder, exist_ok=True)

# Food categories supported by the Foodish image API
categories = [
    "biryani",
    "burger",
    "butter-chicken",
    "dessert",
    "dosa",
    "idly",
    "pasta",
    "pizza",
    "rice",
    "samosa",
    "seafood"
]

count = 4

for category in categories:
    for number in range(1, 6):
        try:
            url = f"https://foodish-api.com/api/images/{category}"
            response = requests.get(url, timeout=20)
            response.raise_for_status()

            image_url = response.json()["image"]
            image = requests.get(image_url, timeout=20)
            image.raise_for_status()

            filename = f"food{count}.jpg"
            filepath = os.path.join(folder, filename)

            with open(filepath, "wb") as file:
                file.write(image.content)

            print(f"Downloaded: {filename}")
            count += 1
            time.sleep(1)

            if count > 50:
                break

        except Exception as error:
            print(f"Could not download {category}: {error}")

    if count > 50:
        break

print("Image download process completed.")