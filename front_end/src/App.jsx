import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import ChatbotWidget from "./components/ChatbotWidget";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Menu from "./pages/Menu";
import Cart from "./pages/Cart";
import MyOrders from "./pages/MyOrders";
import OrderTracking from "./pages/OrderTracking";
import Reservations from "./pages/Reservations";
import Profile from "./pages/Profile";
import Feedback from "./pages/Feedback";

import "./App.css";

function App() {
    return (
        <BrowserRouter>
            <Navbar />

            <main>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/menu" element={<Menu />} />
                    <Route path="/cart" element={<Cart />} />
                    <Route path="/orders" element={<MyOrders />} />
                    <Route path="/track-order" element={<OrderTracking />} />
                    <Route path="/reservations" element={<Reservations />} />
                    <Route path="/profile" element={<Profile />} />
                    <Route path="/feedback" element={<Feedback />} />
                </Routes>
            </main>

            <ChatbotWidget />
            <Footer />
        </BrowserRouter>
    );
}

export default App;