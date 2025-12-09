import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Load or initialize data
def load_data():
    try:
        df = pd.read_csv("grocery_shop_data.csv")
        if "Expiry_Date" in df.columns:
            df["Expiry_Date"] = pd.to_datetime(df["Expiry_Date"], errors='coerce').dt.date
        return df
    except FileNotFoundError:
        return pd.DataFrame({
            "Item_Name": [],
            "Quantity": [],
            "Unit": [],
            "Expiry_Date": []
        })

# Save updated data
def save_data(df):
    df.to_csv("grocery_shop_data.csv", index=False)

# STREAMLIT UI START
st.title("🛒 Grocery Shop Inventory Management System")
st.write("Manage your shop inventory, track expiry, update stock, and visualize items.")

# Load existing data
df = load_data()

menu = st.sidebar.selectbox("Menu", ["Add Item", "Update Stock", "Delete Item", "View Inventory", "Expiry Alerts", "Graphical Report"])

# ADD ITEM
if menu == "Add Item":
    st.header("➕ Add New Grocery Item")

    name = st.text_input("Item Name")
    qty = st.number_input("Quantity", min_value=0.0, step=0.1)
    unit = st.selectbox("Unit", ["kg", "g", "litre", "ml", "pcs"])
    expiry = st.date_input("Expiry Date", datetime.now().date())

    if st.button("Add Item"):
        new_row = pd.DataFrame({
            "Item_Name": [name],
            "Quantity": [qty],
            "Unit": [unit],
            "Expiry_Date": [expiry]
        })
        df = pd.concat([df, new_row], ignore_index=True)
        save_data(df)
        st.success(f"{name} added successfully!")

# UPDATE STOCK
if menu == "Update Stock":
    st.header("🔄 Update Stock")

    if df.empty:
        st.warning("No items available to update.")
    else:
        item_list = df["Item_Name"].unique()
        item = st.selectbox("Select Item", item_list)

        update_type = st.radio("Select Update Type", ["Add Stock", "Sell Stock"])
        amount = st.number_input("Enter Amount", min_value=0.0, step=0.1)

        if st.button("Update"):
            idx = df[df["Item_Name"] == item].index[0]

            if update_type == "Add Stock":
                df.at[idx, "Quantity"] += amount
            elif update_type == "Sell Stock":
                if df.at[idx, "Quantity"] >= amount:
                    df.at[idx, "Quantity"] -= amount
                else:
                    st.error("Not enough stock to sell!")
                    st.stop()

            save_data(df)
            st.success("Stock updated!")

# DELETE ITEM
if menu == "Delete Item":
    st.header("🗑️ Delete Item")

    if df.empty:
        st.warning("No items available to delete.")
    else:
        item_list = df["Item_Name"].unique()
        item = st.selectbox("Select Item to Delete", item_list)

        if st.button("Delete"):
            df = df[df["Item_Name"] != item]
            save_data(df)
            st.success(f"{item} deleted successfully!")

# VIEW INVENTORY
if menu == "View Inventory":
    st.header("📦 Current Inventory")
    st.dataframe(df)

# EXPIRY ALERTS
if menu == "Expiry Alerts":
    st.header("⚠️ Expiry Alerts")
    today = datetime.now().date()
    alert_period = timedelta(days=3)

    df_expired = df[df["Expiry_Date"] < today]
    df_alert = df[(df["Expiry_Date"] >= today) & (df["Expiry_Date"] <= today + alert_period)]

    st.subheader("❌ Expired Items")
    st.dataframe(df_expired)

    st.subheader("⚠️ Items Expiring Within 3 Days")
    st.dataframe(df_alert)

    st.subheader("✅ Valid / Not Expired Items")
    df_valid = df[df["Expiry_Date"] > today + alert_period]
    st.dataframe(df_valid)

# GRAPHICAL REPORT
if menu == "Graphical Report":
    st.header("📊 Inventory Graphical Report")

    if df.empty:
        st.warning("No data available to show graphs.")
    else:
        today = datetime.now().date()

        # Mark expired items
        df["Expired"] = df["Expiry_Date"] < today

        # Assign graph colors
        colors = ["red" if exp else "skyblue" for exp in df["Expired"]]

        fig, ax = plt.subplots()
        ax.bar(df["Item_Name"], df["Quantity"], color=colors)

        plt.xticks(rotation=45)
        plt.ylabel("Quantity")
        plt.title("Inventory Quantities (Red = Expired Items)")

        st.pyplot(fig)
        st.info("🔴 Red bars show expired items.  🔵 Blue bars show valid items.")
