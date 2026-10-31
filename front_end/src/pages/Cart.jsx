import { useState } from "react";

function Cart() {
    const [cart, setCart] = useState([]);

    const removeItem = (id) => {
        setCart(cart.filter((item) => item.id !== id));
    };

    return (
        <div className="cart-page">
            <h1>My Cart</h1>

            {cart.length === 0 ? (
                <p>Your cart is empty.</p>
            ) : (
                cart.map((item) => (
                    <div key={item.id} className="cart-item">
                        <h3>{item.name}</h3>
                        <p>₹{item.price}</p>
                        <button onClick={() => removeItem(item.id)}>
                            Remove
                        </button>
                    </div>
                ))
            )}
        </div>
    );
}

export default Cart;