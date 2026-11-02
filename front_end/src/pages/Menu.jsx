
import { useEffect, useState } from "react";
import { fetchAPI } from "../services/api";

function Menu() {
    const [foods, setFoods] = useState([]);
    const [message, setMessage] = useState("Loading menu...");
    const [success, setSuccess] = useState("");

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

    const addToCart = (food) => {
        const cart = JSON.parse(localStorage.getItem("cart") || "[]");

        const foodId = food.id || food._id;
        const existingItem = cart.find(
            (item) => String(item.id) === String(foodId)
        );

        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            cart.push({
                id: foodId,
                name: food.name,
                price: Number(food.price),
                image: food.image || "",
                quantity: 1
            });
        }

        localStorage.setItem("cart", JSON.stringify(cart));

        setSuccess(`${food.name} added to cart!`);

        setTimeout(() => {
            setSuccess("");
        }, 2000);
    };

    return (
        <div className="menu-page">
            <h1>Our Food Menu</h1>

            {message && <p>{message}</p>}

            {success && (
                <p style={{ color: "green", fontWeight: "bold" }}>
                    {success}
                </p>
            )}

            <div className="food-list">
                {foods.map((food) => (
                    <div className="food-card" key={food.id || food._id}>
                        <img
                            src={food.image || "https://placehold.co/500x350?text=Food+Image"}
                            alt={food.name}
                            onError={(e) => {
                                e.currentTarget.src =
                                    "https://placehold.co/500x350?text=Image+Not+Available";
                            }}
                        />

                        <h3>{food.name}</h3>
                        <p>{food.description}</p>
                        <h4>₹{food.price}</h4>

                        <button onClick={() => addToCart(food)}>
                            Add to Cart
                        </button>
                    </div>
                ))}
            </div>

            {!message && foods.length === 0 && (
                <p>No food items available yet.</p>
            )}
        </div>
    );
}

export default Menu;
