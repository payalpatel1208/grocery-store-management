from oprations import *
import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


st.set_page_config(page_title="Grocery store", layout="centered")
st.title("🛒 Grocery Store Management System")


menu = st.sidebar.radio(
    "Menu",
    ["Add Product", "View Inventory","Update Product" ,"Sell Product", "sell_product_Graph","Delete_product"]
)

# Add product

if menu == "Add Product":
    st.header("➕ Add New Product")

    name = st.text_input("Product Name")
    price = st.number_input("price",min_value=0.0)
    quantity = st.number_input("quantity",min_value=0)
    
    if st.button("Add Product"):
        if name.strip() == "":
            st.warning("Enter Product name")

        else:
            Add_Products(name,price,quantity)
            st.success("Product added successfully")

# Delete Product
if menu == "Delete_product":
    st.header("🧹 Delete Product")

    name = st.text_input("Product Name")

    if st.button("Delete Product"):
        if name.strip() == "":
             st.warning("Please enter product name")
        else:
             result = delete_product(name)
        if result == 0:
            st.error("Product not found")
        else:
            st.success(f"Product '{name}' deleted successfully")


if menu == "View Inventory":
    st.header("📦 Inventory")

    data = get_products()
    df = pd.DataFrame(data, columns=["ID", "Name", "Price", "Quantity"])

    if df.empty:
        st.info("No product available")
    else:
        st.dataframe(df)
# Update the product

if menu == "Update Product":
    st.header("✏️ Update Product")

    name = st.text_input("Product Name")

    option = st.radio(
        "What do you want to update?",
        ("Update Price", "Add Quantity", "Update Both")
    )

    if option == "Update Price":
        new_price = st.number_input("New Price", min_value=0.0)

    elif option == "Add Quantity":
        add_quantity = st.number_input("Quantity to Add", min_value=1)

    elif option == "Update Both":
        new_price = st.number_input("New Price", min_value=0.0)
        add_quantity = st.number_input("Quantity to Add", min_value=1)

    if st.button("Update Product"):
        if name.strip() == "":
            st.warning("Enter product name")
        else:
            if option == "Update Price":
                update_product(name, new_price=new_price)

            elif option == "Add Quantity":
                update_product(name, add_quantity=add_quantity)

            else:
                update_product(
                    name,
                    new_price=new_price,
                    add_quantity=add_quantity
                )

            st.success("Product updated successfully")


#  Sell Product
if menu == "Sell Product":
    st.header("💰 Sell Product")

    name = st.text_input("Product Name")
    quantity = st.number_input("Quantity", min_value=1)

    if st.button("Sell"):
        total = sell_product(name,quantity)
        if total is not None:
            st.success(f"Total Bill: ₹ {total}")
        else:
            st.error("Product not found or insufficient stock")

# sell Graph
if menu == "sell_product_Graph":
    st.header("📊 Sells Reports")

    conn = sqlite3.connect("grocery.db")
    sales_df = pd.read_sql(
    "SELECT product_name, SUM(quantity) as quantity FROM sales GROUP BY product_name",
    conn
    )
    conn.close()

    if sales_df.empty:
        st.info("No sales data available")
    else:
        fig, ax = plt.subplots()
        ax.bar(sales_df["product_name"], sales_df["quantity"], color="red")
        ax.set_xlabel("Product")
        ax.set_ylabel("Quantity Sold")
        ax.set_title("Product-wise Sales")
        st.pyplot(fig)
