import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [products, setProducts] = useState([]);
  const [status, setStatus] = useState('Connecting to backend...');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In production, Nginx reverse-proxies /api/ to backend:8000/
    fetch('/api/products')
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        setProducts(data.products || []);
        setStatus(data.db_status || 'Connected');
        setLoading(false);
      })
      .catch((err) => {
        console.error('API Fetch error:', err);
        setStatus('Backend API offline or unreachable');
        setLoading(false);
      });
  }, []);

  return (
    <div className="app-container">
      <header className="navbar">
        <div className="logo">🛒 CloudShop E-Commerce</div>
        <div className="network-badge">
          Status: <span className="status-indicator">{status}</span>
        </div>
      </header>

      <main className="content">
        <section className="architecture-banner">
          <h2>Production Docker Architecture</h2>
          <p>
            Frontend (Port 80 Public) &rarr; Internal Nginx Proxy &rarr; FastAPI Backend (Port 8000 Private) &rarr; PostgreSQL (Port 5432 Private)
          </p>
        </section>

        <h3>Featured Products</h3>
        {loading ? (
          <p>Loading catalog from FastAPI & PostgreSQL...</p>
        ) : (
          <div className="product-grid">
            {products.length > 0 ? (
              products.map((item) => (
                <div key={item.id} className="product-card">
                  <h4>{item.name}</h4>
                  <p className="description">{item.description}</p>
                  <p className="price">${item.price.toFixed(2)}</p>
                  <button className="buy-btn">Add to Cart</button>
                </div>
              ))
            ) : (
              <p>No products available yet.</p>
            )}
          </div>
        )}
      </main>

      <footer className="footer">
        <p>Running on Ubuntu EC2 | Network: Isolated Bridge (app-network)</p>
      </footer>
    </div>
  );
}

export default App;
