
from database import menu_collection


# Recommend Food Items
def recommend_food(category_id: str = None):

    query = {
        "is_available": True
    }

    # Filter food by category
    if category_id:
        query["category_id"] = category_id

    food_items = list(
        menu_collection.find(query).limit(5)
    )

    recommendations = []

    for item in food_items:
        recommendations.append({
            "id": str(item["_id"]),
            "name": item["name"],
            "description": item.get("description"),
            "price": item["price"],
            "category_id": item["category_id"],
            "image": item.get("image")
        })

    return recommendations


# Recommend Popular Food Items
def recommend_popular_food():

    food_items = list(
        menu_collection.find({
            "is_available": True
        }).limit(5)
    )

    recommendations = []

    for item in food_items:
        recommendations.append({
            "id": str(item["_id"]),
            "name": item["name"],
            "price": item["price"],
            "image": item.get("image")
        })

    return recommendations
