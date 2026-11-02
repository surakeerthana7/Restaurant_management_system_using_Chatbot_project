
import { useEffect, useState } from "react";
import { fetchAPI } from "../services/api";

function Reports() {
    const [report, setReport] = useState({
        users: 0,
        foodItems: 0,
        orders: 0,
        reservations: 0,
        tables: 0
    });

    const [message, setMessage] = useState("");

    useEffect(() => {
        const loadReports = async () => {
            try {
                const [users, foods, orders, reservations, tables] =
                    await Promise.all([
                        fetchAPI("/api/users/"),
                        fetchAPI("/api/menu/"),
                        fetchAPI("/api/orders/"),
                        fetchAPI("/api/reservations/"),
                        fetchAPI("/api/tables/")
                    ]);

                setReport({
                    users: Array.isArray(users) ? users.length : 0,
                    foodItems: Array.isArray(foods) ? foods.length : 0,
                    orders: Array.isArray(orders) ? orders.length : 0,
                    reservations: Array.isArray(reservations)
                        ? reservations.length : 0,
                    tables: Array.isArray(tables) ? tables.length : 0
                });
            } catch (error) {
                setMessage(error.message);
            }
        };

        loadReports();
    }, []);

    const cards = [
        { title: "Total Users", value: report.users, icon: "👥" },
        { title: "Food Items", value: report.foodItems, icon: "🍽️" },
        { title: "Total Orders", value: report.orders, icon: "🛒" },
        { title: "Reservations", value: report.reservations, icon: "📅" },
        { title: "Restaurant Tables", value: report.tables, icon: "🪑" }
    ];

    return (
        <div className="page-container">
            <h1>Restaurant Reports</h1>
            <p>Overview of restaurant activities and statistics.</p>

            {message && <p>{message}</p>}

            <div className="report-grid">
                {cards.map((card) => (
                    <div className="report-card" key={card.title}>
                        <h2>{card.icon}</h2>
                        <h3>{card.title}</h3>
                        <h1>{card.value}</h1>
                    </div>
                ))}
            </div>

            <button onClick={() => window.location.reload()}>
                Refresh Reports
            </button>
        </div>
    );
}

export default Reports;
