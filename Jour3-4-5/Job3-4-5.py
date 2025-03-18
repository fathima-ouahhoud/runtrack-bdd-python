import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox

def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root", 
            password=".env", 
            database="store"
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Erreur", f"Erreur de connexion à la base : {err}")
        return None

def show_products():
    for row in product_tree.get_children():
        product_tree.delete(row)

    db = connect_db()
    if db is None:
        return

    cursor = db.cursor()
    cursor.execute("""
        SELECT p.id, p.name, p.description, p.price, p.quantity, c.name 
        FROM product p 
        LEFT JOIN category c ON p.id_category = c.id
    """)
    products = cursor.fetchall()
    db.close()

    for product in products:
        product_tree.insert("", "end", values=product)

def add_product():
    name = name_entry.get().strip()
    description = desc_entry.get().strip()
    price = price_entry.get().strip()
    quantity = quantity_entry.get().strip()
    category = category_combo.get().strip()

    if not (name and description and price and quantity and category):
        messagebox.showwarning("Erreur", "Tous les champs doivent être remplis.")
        return

    try:
        price = int(price)
        quantity = int(quantity)
    except ValueError:
        messagebox.showwarning("Erreur", "Prix et Quantité doivent être des nombres.")
        return

    db = connect_db()
    if db is None:
        return

    cursor = db.cursor()
    cursor.execute("SELECT id FROM category WHERE name=%s", (category,))
    category_row = cursor.fetchone()

    if category_row is None:
        messagebox.showerror("Erreur", "Catégorie invalide. Veuillez choisir une catégorie existante.")
        db.close()
        return

    category_id = category_row[0]

    cursor.execute(
        "INSERT INTO product (name, description, price, quantity, id_category) VALUES (%s, %s, %s, %s, %s)",
        (name, description, price, quantity, category_id)
    )
    db.commit()
    db.close()

    show_products()
    messagebox.showinfo("Succès", "Produit ajouté avec succès !")

def delete_product():
    selected_item = product_tree.selection()
    if not selected_item:
        messagebox.showwarning("Erreur", "Veuillez sélectionner un produit.")
        return

    item = product_tree.item(selected_item)
    product_id = item["values"][0]

    db = connect_db()
    if db is None:
        return

    cursor = db.cursor()
    cursor.execute("DELETE FROM product WHERE id=%s", (product_id,))
    db.commit()
    db.close()

    show_products()
    messagebox.showinfo("Succès", "Produit supprimé !")

def update_product():
    selected_item = product_tree.selection()
    if not selected_item:
        messagebox.showwarning("Erreur", "Veuillez sélectionner un produit.")
        return

    item = product_tree.item(selected_item)
    product_id = item["values"][0]
    new_price = price_entry.get().strip()
    new_quantity = quantity_entry.get().strip()

    if not (new_price and new_quantity):
        messagebox.showwarning("Erreur", "Les champs Prix et Quantité doivent être remplis.")
        return

    try:
        new_price = int(new_price)
        new_quantity = int(new_quantity)
    except ValueError:
        messagebox.showwarning("Erreur", "Prix et Quantité doivent être des nombres.")
        return

    db = connect_db()
    if db is None:
        return

    cursor = db.cursor()
    cursor.execute(
        "UPDATE product SET price=%s, quantity=%s WHERE id=%s",
        (new_price, new_quantity, product_id)
    )
    db.commit()
    db.close()

    show_products()
    messagebox.showinfo("Succès", "Produit mis à jour !")

root = tk.Tk()
root.title("Gestion de Stock")

columns = ("ID", "Nom", "Description", "Prix", "Quantité", "Catégorie")
product_tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    product_tree.heading(col, text=col)
    product_tree.column(col, width=120)
product_tree.pack(pady=20)

form_frame = tk.Frame(root)
form_frame.pack()

tk.Label(form_frame, text="Nom:").grid(row=0, column=0)
name_entry = tk.Entry(form_frame)
name_entry.grid(row=0, column=1)

tk.Label(form_frame, text="Description:").grid(row=1, column=0)
desc_entry = tk.Entry(form_frame)
desc_entry.grid(row=1, column=1)

tk.Label(form_frame, text="Prix:").grid(row=2, column=0)
price_entry = tk.Entry(form_frame)
price_entry.grid(row=2, column=1)

tk.Label(form_frame, text="Quantité:").grid(row=3, column=0)
quantity_entry = tk.Entry(form_frame)
quantity_entry.grid(row=3, column=1)

tk.Label(form_frame, text="Catégorie:").grid(row=4, column=0)
category_combo = ttk.Combobox(form_frame)
category_combo.grid(row=4, column=1)

btn_frame = tk.Frame(root)
btn_frame.pack()

add_btn = tk.Button(btn_frame, text="Ajouter", command=add_product)
add_btn.grid(row=0, column=0, padx=10)

update_btn = tk.Button(btn_frame, text="Modifier", command=update_product)
update_btn.grid(row=0, column=1, padx=10)

delete_btn = tk.Button(btn_frame, text="Supprimer", command=delete_product)
delete_btn.grid(row=0, column=2, padx=10)

def load_categories():
    db = connect_db()
    if db is None:
        return

    cursor = db.cursor()
    cursor.execute("SELECT name FROM category")
    categories = [row[0] for row in cursor.fetchall()]
    db.close()

    category_combo["values"] = categories
    if categories:
        category_combo.current(0)

load_categories()
show_products()
root.mainloop()
