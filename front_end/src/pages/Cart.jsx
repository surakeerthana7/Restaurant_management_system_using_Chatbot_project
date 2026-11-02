
import { useEffect, useState } from "react";

function Cart() {
    const [cart, setCart] = useState([]);

    useEffect(() => {
        const savedCart = JSON.parse(localStorage.getItem("cart") || "[]");
        setCart(savedCart);
    }, []);

    const saveCart = (updatedCart) => {
        setCart(updatedCart);
        localStorage.setItem("cart", JSON.stringify(updatedCart));
    };

    const increaseQuantity = (id) => {
        const updatedCart = cart.map((item) =>
            String(item.id) === String(id)
                ? { ...item, quantity: item.quantity + 1 }
                : item
        );

        saveCart(updatedCart);
    };

    const decreaseQuantity = (id) => {
        const updatedCart = cart
            .map((item) =>
                String(item.id) === String(id)
                    ? { ...item, quantity: item.quantity - 1 }
                    : item
            )
            .filter((item) => item.quantity > 0);

        saveCart(updatedCart);
    };

    const removeItem = (id) => {
        const updatedCart = cart.filter(
            (item) => String(item.id) !== String(id)
        );

        saveCart(updatedCart);
    };

    const clearCart = () => {
        saveCart([]);
    };

    const totalAmount = cart.reduce(
        (total, item) => total + item.price * item.quantity,
        0
    );

    return (
        <div className="page-container">
            <h1>My Cart</h1>

            {cart.length === 0 ? (
                <div>
                    <h2>Your cart is empty!</h2>
                    <p>Please visit our Menu page and add some delicious food.</p>
                </div>
            ) : (
                <>
                    <div className="food-list">
                        {cart.map((item) => (
                            <div className="food-card" key={item.id}>
                                {item.image && (
                                    <img
                                        src={item.image}
                                        alt={item.name}
                                        onError={(e) => {
                                            e.currentTarget.style.display = "none";
                                        }}
                                    />
                                )}

                                <h3>{item.name}</h3>
                                <p>Price: ₹{item.price}</p>

                                <div>
                                    <button onClick={() => decreaseQuantity(item.id)}>
                                        −
                                    </button>

                                    <span style={{ margin: "0 15px" }}>
                                        {item.quantity}
                                    </span>

                                    <button onClick={() => increaseQuantity(item.id)}>
                                        +
                                    </button>
                                </div>

                                <h4>
                                    Subtotal: ₹{item.price * item.quantity}
                                </h4>

                                <button onClick={() => removeItem(item.id)}>
                                    Remove
                                </button>
                            </div>
                        ))}
                    </div>

                    <div style={{ textAlign: "center", margin: "30px" }}>
                        <h2>Total Amount: ₹{totalAmount}</h2>

                        <button onClick={clearCart}>
                            Clear Cart
                        </button>
                    </div>
                </>
            )}
        </div>
    );
}

export default Cart;
