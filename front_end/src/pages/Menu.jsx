
import { useEffect, useState } from "react";
import { fetchAPI } from "../services/api";

const categories = [
    "All",
    "Starters",
    "Veg Main Course",
    "Non-Veg Main Course",
    "Biryani",
    "Rice and Noodles",
    "South Indian",
    "Desserts",
    "Beverages"
];

function Menu() {
    const [foods, setFoods] = useState([]);
    const [message, setMessage] = useState("Loading menu...");
    const [selectedCategory, setSelectedCategory] = useState("All");

    useEffect(() => {
        const loadMenu = async () => {
            try {
                const data = await fetchAPI("/api/menu/");
                setFoods(Array.isArray(data) ? data : data.items || []);
                setMessage("");
            } catch (error) {
                setMessage(error.message);
            }
        };

        loadMenu();
    }, []);

    const filteredFoods =
        selectedCategory === "All"
            ? foods
            : foods.filter(
                (food) => food.category === selectedCategory
            );

    return (
        <div className="menu-page">
            <h1>Our Food Menu</h1>
            <p className="menu-subtitle">
                Explore our delicious food collection
            </p>

            <div className="category-buttons">
                {categories.map((category) => (
                    <button
                        key={category}
                        className={
                            selectedCategory === category
                                ? "active-category"
                                : ""
                        }
                        onClick={() => setSelectedCategory(category)}
                    >
                        {category}
                    </button>
                ))}
            </div>

            {message && <p>{message}</p>}

            <div className="food-list">
                {filteredFoods.map((food) => (
                    <div className="food-card" key={food.id || food._id}>
                        <img
                            src={
                                food.image ||
                                "https://placehold.co/500x350?text=Food+Image"
                            }
                            alt={food.name}
                            className="food-image"
                            loading="lazy"
                            onError={(e) => {
                                e.currentTarget.onerror = null;
                                e.currentTarget.src =
                                    "https://placehold.co/500x350?text=Image+Not+Available";
                            }}
                        />

                        <div className="food-card-content">
                            <h3>{food.name}</h3>

                            <p>{food.description}</p>

                            <h4>₹{food.price}</h4>

                            <span className="food-category">
                                {food.category}
                            </span>

                            {!food.available && (
                                <p className="unavailable">
                                    Currently unavailable
                                </p>
                            )}
                        </div>
                    </div>
                ))}
            </div>

            {!message && filteredFoods.length === 0 && (
                <p>No food items available in this category.</p>
            )}
        </div>
    );
}

export default Menu;
