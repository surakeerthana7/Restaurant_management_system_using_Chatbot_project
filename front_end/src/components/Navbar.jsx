import { Link } from "react-router-dom";
import { ShoppingCart, Utensils } from "lucide-react";

function Navbar() {
    return (
        <nav className="navbar">
            <div className="logo">
                <Utensils size={25} />
                <h2>Foodie Restaurant</h2>
            </div>

            <div className="nav-links">
                <Link to="/">Home</Link>
                <Link to="/menu">Menu</Link>
                <Link to="/login">Login</Link>
                <Link to="/register">Register</Link>
                <Link to="/cart">
                    <ShoppingCart size={20} />
                    Cart
                </Link>
            </div>
        </nav>
    );
}

export default Navbar;