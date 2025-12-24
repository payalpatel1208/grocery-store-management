import sqlite3

def connect():
    return sqlite3.connect("grocery.db")

# add a new product
def Add_Products(name,price,quantity):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute(" INSERT OR IGNORE INTO products(name,price,quantity) VALUES (:name,:price,:quantity)",
                    {"name" : name, "price" : price, "quantity": quantity}
        )

# to get a product

def get_products():
    with connect() as conn:
        cur = conn.cursor()

        cur.execute("SELECT * FROM products")
        conn.commit()
        return cur.fetchall() # It retrieves all the rows stored in the cursor and returns them as a Python list 

# to delete products

def delete_product(name):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM products WHERE name = ?", (name,))
        deleted_rows = cur.rowcount
        conn.commit()
        return deleted_rows

# to update products
def update_product(name, new_price=None, add_quantity=None):
    with connect() as conn:
        cur = conn.cursor()

        if new_price is not None:
            cur.execute(
                "UPDATE products SET price = ? WHERE name = ?",
                (new_price, name)
            )

        if add_quantity is not None:
            cur.execute(
                "UPDATE products SET quantity = quantity + ? WHERE name = ?",
                (add_quantity, name)
            )

        conn.commit()

def sell_product(product_name,quantity):
    with connect() as conn:
        cur = conn.cursor()

        # Fetch product details
        cur.execute("SELECT quantity , price FROM products WHERE name=?",(product_name,))
        product = cur.fetchone() # It retrieves one the rows stored in the cursor and returns them as a Python list

        if product is None:
            return "Product is not found"
        
        available_quntity , price = product

        # Check stock
        if available_quntity < quantity:
            return "insufficent product"
        # total_bill
        total = quantity * price

        # update_product

        cur.execute("UPDATE products SET quantity = quantity - ? WHERE name = ?", (quantity, product_name))

        # INSERT sales

        cur.execute("INSERT INTO sales(product_name, quantity, total) VALUES (?, ?, ?)",
                    (product_name, quantity, total))
        
        conn.commit()
        return f"seles sucessful {total}"