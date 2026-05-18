import streamlit as st
import requests
import pandas as pd

# API_URL = "http://127.0.0.1:8000"
API_URL = 'http://localhost:8501'
st.set_page_config(
    page_title="E-Commerce System",
    layout="wide"
)

st.title("🛒 E-Commerce System")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Register",
        "Products",
        "Add Product",
        "Create Order",
        "User Orders",
        "Top Products",
        "Sales Report"
    ]
)

# ---------------------------------
# Register
# ---------------------------------

if menu == "Register":

    st.header("Register User")

    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password")

    if st.button("Register"):

        response = requests.post(
            f"{API_URL}/register",
            json={
                "name": name,
                "email": email,
                "password": password
            }
        )

        st.success(response.json()["message"])

# ---------------------------------
# Products
# ---------------------------------

elif menu == "Products":

    st.header("Products")

    try:
        response = requests.get(f"{API_URL}/products")
        data = response.json()

        # If API returns error, show demo products
        if isinstance(data, dict) and 'detail' in data:
            st.warning("Using demo data (database not connected). To see your database products, please set up SQL Server connection properly.")
            data = []
        
        # Demo products to show layout
        demo_products = [
            {"id": 1, "name": "iPhone 15", "description": "Apple smartphone 128GB", "price": 55000, "stock": 10, "category": "Electronics"},
            {"id": 2, "name": "Gaming Laptop", "description": "RTX gaming laptop", "price": 42000, "stock": 5, "category": "Electronics"},
            {"id": 3, "name": "Running Shoes", "description": "Comfortable sport shoes", "price": 1500, "stock": 20, "category": "Fashion"},
            {"id": 4, "name": "Clean Code Book", "description": "Programming best practices", "price": 850, "stock": 15, "category": "Books"},
            {"id": 5, "name": "Air Fryer", "description": "Digital air fryer 5L", "price": 3200, "stock": 8, "category": "Home Appliances"},
            {"id": 6, "name": "Football", "description": "Professional football", "price": 700, "stock": 25, "category": "Sports"}
        ]
        
        # Use database data if available, otherwise use demo
        display_data = data if (isinstance(data, list) and len(data) > 0) else demo_products

        if display_data:
            # Display products in a grid layout (3 columns)
            cols = st.columns(3)
            
            for idx, product in enumerate(display_data):
                col = cols[idx % 3]
                
                with col:
                    st.markdown(f"""
                    <div style="border: 1px solid #ddd; padding: 15px; border-radius: 8px; height: 100%; background-color: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); height: 200px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-bottom: 10px;">
                            <p style="text-align: center; color: white; font-size: 3em;">🛍️</p>
                        </div>
                        <h4 style="margin: 10px 0; color: #333;">{product.get('name', 'N/A')}</h4>
                        <p style="color: #666; font-size: 0.9em; margin: 5px 0; min-height: 40px;">{product.get('description', '')[:60]}...</p>
                        <p style="color: #27ae60; font-weight: bold; font-size: 1.3em; margin: 10px 0;">₹{product.get('price', 0)}</p>
                        <p style="color: #7f8c8d; font-size: 0.85em; margin: 5px 0;">Category: {product.get('category', 'N/A')}</p>
                        <p style="color: #e74c3c; font-size: 0.9em; margin: 5px 0;">Stock: {product.get('stock', 0)}</p>
                        <button style="width: 100%; padding: 10px; background-color: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; margin-top: 10px; transition: background-color 0.3s;">
                            🛒 Add to Cart
                        </button>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No products found")
    
    except Exception as e:
        st.error(f"Error fetching products: {str(e)}")

# ---------------------------------
# Add Product
# ---------------------------------

elif menu == "Add Product":

    st.header("Add Product")

    name = st.text_input("Product Name")
    description = st.text_area("Description")
    price = st.number_input("Price")
    stock = st.number_input("Stock")
    category_id = st.number_input("Category ID")

    if st.button("Add Product"):

        response = requests.post(
            f"{API_URL}/add-product",
            json={
                "name": name,
                "description": description,
                "price": price,
                "stock": stock,
                "category_id": category_id
            }
        )

        st.success(response.json()["message"])

# ---------------------------------
# Create Order
# ---------------------------------

elif menu == "Create Order":

    st.header("Create Order")

    user_id = st.number_input("User ID")
    total_price = st.number_input("Total Price")
    status = st.selectbox(
        "Status",
        ["pending", "shipped"]
    )

    if st.button("Create"):

        response = requests.post(
            f"{API_URL}/create-order",
            json={
                "user_id": user_id,
                "total_price": total_price,
                "status": status
            }
        )

        st.success(response.json()["message"])

# ---------------------------------
# User Orders
# ---------------------------------

elif menu == "User Orders":

    st.header("User Orders")

    user_id = st.number_input("Enter User ID")

    if st.button("Show Orders"):
        try:
            response = requests.get(
                f"{API_URL}/user-orders/{user_id}"
            )
            data = response.json()
            
            if isinstance(data, list) and len(data) > 0:
                df = pd.DataFrame(data)
                st.dataframe(df)
            else:
                st.info("No orders found for this user")
        except Exception as e:
            st.error(f"Error fetching orders: {str(e)}")

# ---------------------------------
# Top Products
# ---------------------------------

elif menu == "Top Products":

    st.header("Top Selling Products")

    try:
        response = requests.get(
            f"{API_URL}/top-products"
        )
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0:
            df = pd.DataFrame(data)
            st.dataframe(df)
        else:
            st.info("No top products found")
    except Exception as e:
        st.error(f"Error fetching top products: {str(e)}")

# ---------------------------------
# Sales Report
# ---------------------------------

elif menu == "Sales Report":

    st.header("Monthly Sales Report")

    try:
        response = requests.get(
            f"{API_URL}/sales-report"
        )
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0:
            df = pd.DataFrame(data)
            st.dataframe(df)
        else:
            st.info("No sales report data available")
    except Exception as e:
        st.error(f"Error fetching sales report: {str(e)}")
