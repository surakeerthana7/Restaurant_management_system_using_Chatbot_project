
import { useEffect, useState } from "react";
import { fetchAPI } from "../services/api";

function ManageMenu() {
    const [foods, setFoods] = useState([]);
    const [message, setMessage] = useState("");
    const [form, setForm] = useState({
        name: "",
        description: "",
        price: "",
        category: "",
        image: "",
        available: true
    });

    const loadFoods = async () => {
        try {
            const data = await fetchAPI("/api/menu/");
            setFoods(Array.isArray(data) ? data : []);
        } catch (error) {
            setMessage(error.message);
        }
    };

    useEffect(() => {
        loadFoods();
    }, []);

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const addFood = async (e) => {
        e.preventDefault();

        try {
            await fetchAPI("/api/menu/", {
                method: "POST",
                body: JSON.stringify({
                    ...form,
                    price: Number(form.price)
                })
            });

            setMessage("Food item added successfully!");
            setForm({
                name: "",
                description: "",
                price: "",
                category: "",
                image: "",
                available: true
            });
            loadFoods();
        } catch (error) {
            setMessage(error.message);
        }
    };

    const deleteFood = async (id) => {
        if (!window.confirm("Are you sure you want to delete this food item?")) {
            return;
        }

        try {
            await fetchAPI(`/api/menu/${id}`, {
                method: "DELETE"
            });
            setMessage("Food item deleted successfully!");
            loadFoods();
        } catch (error) {
            setMessage(error.message);
        }
    };

    return (
        <div className="page-container">
            <h1>Manage Food Menu</h1>
            <p>Add, view and delete restaurant food items.</p>

            {message && <p>{message}</p>}

            <form onSubmit={addFood}>
                <input name="name" placeholder="Food Name"
                    value={form.name} onChange={handleChange} required />

                <input name="description" placeholder="Description"
                    value={form.description} onChange={handleChange} />

                <input name="price" type="number" placeholder="Price"
                    value={form.price} onChange={handleChange} required />

                <input name="category" placeholder="Category"
                    value={form.category} onChange={handleChange} required />

                <input name="image" placeholder="Image URL"
                    value={form.image} onChange={handleChange} />

                <button type="submit">Add Food Item</button>
            </form>

            <h2>Food Items ({foods.length})</h2>

            <div className="food-list">
                {foods.map((food) => (
                    <div className="food-card" key={food.id}>
                        <h3>{food.name}</h3>
                        <p>{food.description}</p>
                        <p>Category: {food.category}</p>
                        <h4>₹{food.price}</h4>
                        <button onClick={() => deleteFood(food.id)}>
                            Delete
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default ManageMenu;
