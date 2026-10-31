import { useEffect, useState } from "react";
import { fetchAPI } from "../services/api";

function Menu() {
    const [foods, setFoods] = useState([]);
    const [message, setMessage] = useState("Loading menu...");

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

    return (
        <div className="menu-page">
            <h1>Our Food Menu</h1>

            {message && <p>{message}</p>}

            <div className="food-list">
                {foods.map((food) => (
                    <div className="food-card" key={food._id}>
                        <h3>{food.name}</h3>
                        <p>{food.description}</p>
                        <h4>₹{food.price}</h4>
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