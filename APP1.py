from inventory_module import *


st.title("🛒 Grocery Shop Inventory Management System")
st.write("Manage your shop inventory, track expiry, update stock, and visualize items.")

# Load data
df = load_data()

menu = st.sidebar.selectbox("Menu", ["Add Item", "Update Stock", "Delete Item", "View Inventory", "Expiry Alerts", "Graphical Report"])

if menu == "Add Item":
    df = add_item(df)
elif menu == "Update Stock":
    df = update_stock(df)
elif menu == "Delete Item":
    df = delete_item(df)
elif menu == "View Inventory":
    view_inventory(df)
elif menu == "Expiry Alerts":
    expiry_alerts(df)
elif menu == "Graphical Report":
    graphical_report(df)
