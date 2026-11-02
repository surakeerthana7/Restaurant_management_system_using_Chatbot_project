
import { Link } from "react-router-dom";
import { Utensils, Clock, Truck } from "lucide-react";

import food1 from "../assets/food/food1.jpg";
import food2 from "../assets/food/food2.jpg";
import food3 from "../assets/food/food3.jpg";

function Home() {
    const popularFoods = [
        { name: "Special Dish 1", image: food1, price: "₹220" },
        { name: "Special Dish 2", image: food2, price: "₹180" },
        { name: "Special Dish 3", image: food3, price: "₹150" }

    ];

    return (
        <div className="home-page">
            <section className="hero">
                <div className="hero-content">
                    <h1>Welcome to Foodie Restaurant</h1>
                    <h2>Delicious Food, Delivered Fresh!</h2>
                    <p>
                        Explore our menu, order your favourite dishes
                        and enjoy delicious food at your doorstep.
                    </p>

                    <Link to="/menu" className="order-btn">
                        Explore Menu
                    </Link>
                </div>
            </section>

            <section className="features">
                <div className="feature-card">
                    <Utensils size={35} />
                    <h3>Fresh Food</h3>
                    <p>Fresh and delicious meals prepared every day.</p>
                </div>

                <div className="feature-card">
                    <Clock size={35} />
                    <h3>Quick Service</h3>
                    <p>Fast and easy online food ordering.</p>
                </div>

                <div className="feature-card">
                    <Truck size={35} />
                    <h3>Home Delivery</h3>
                    <p>Enjoy your favourite food at home.</p>
                </div>
            </section>

            <section className="popular-foods">
                <h2>Our Popular Dishes</h2>
                <p className="section-description">
                    Taste the delicious food prepared just for you!
                </p>

                <div className="popular-food-grid">
                    {popularFoods.map((food, index) => (
                        <div className="popular-food-card" key={index}>
                            <img src={food.image} alt={food.name} />
                            <h3>{food.name}</h3>
                            <p>{food.price}</p>
                        </div>
                    ))}
                </div>

                <Link to="/menu" className="order-btn">
                    View Full Menu
                </Link>
            </section>
        </div>
    );
}

export default Home;
