import { Link } from "react-router-dom";
import { Utensils, Clock, Truck } from "lucide-react";

function Home() {
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
        </div>
    );
}

export default Home;