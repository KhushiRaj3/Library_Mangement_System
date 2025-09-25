"""
Aesthetic Library Management System
Technologies: Python, SQLite, Tkinter
Features: Add, view books with a visually appealing interface
"""

import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# --- Database Setup ---
def initialize_database():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL
        )
    ''')
    conn.commit()
    return conn, cursor

# --- CRUD Functions ---
def add_book_gui():
    title = title_entry.get().strip()
    author = author_entry.get().strip()
    if title and author:
        cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
        conn.commit()
        messagebox.showinfo("Success", f'Book "{title}" by {author} added successfully.')
        title_entry.delete(0, tk.END)
        author_entry.delete(0, tk.END)
        view_books_gui()
    else:
        messagebox.showerror("Error", "Title and Author cannot be empty.")

def view_books_gui():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM books")
    for book in cursor.fetchall():
        tree.insert("", tk.END, values=book)

# --- Initialize DB ---
conn, cursor = initialize_database()

# --- GUI Setup ---
root = tk.Tk()
root.title("📚 Library Management System")
root.geometry("600x500")
root.configure(bg="#f0f4f8")  # Light background

# --- Header ---
header = tk.Label(root, text="Library Management System", font=("Helvetica", 20, "bold"), bg="#4a7abc", fg="white", pady=10)
header.pack(fill=tk.X)

# --- Input Frame ---
input_frame = tk.Frame(root, bg="#f0f4f8", pady=10)
input_frame.pack(fill=tk.X)

tk.Label(input_frame, text="Book Title:", font=("Helvetica", 12), bg="#f0f4f8").grid(row=0, column=0, padx=10, pady=5, sticky="w")
title_entry = tk.Entry(input_frame, width=40, font=("Helvetica", 12))
title_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(input_frame, text="Author Name:", font=("Helvetica", 12), bg="#f0f4f8").grid(row=1, column=0, padx=10, pady=5, sticky="w")
author_entry = tk.Entry(input_frame, width=40, font=("Helvetica", 12))
author_entry.grid(row=1, column=1, padx=10, pady=5)

# --- Buttons Frame ---
button_frame = tk.Frame(root, bg="#f0f4f8")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Book", command=add_book_gui, width=15, bg="#4caf50", fg="white", font=("Helvetica", 12, "bold")).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Refresh List", command=view_books_gui, width=15, bg="#2196f3", fg="white", font=("Helvetica", 12, "bold")).grid(row=0, column=1, padx=10)

# --- Treeview Frame ---
tree_frame = tk.Frame(root)
tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

# Scrollbar
tree_scroll = tk.Scrollbar(tree_frame)
tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

# Treeview
tree = ttk.Treeview(tree_frame, columns=("ID", "Title", "Author"), show='headings', yscrollcommand=tree_scroll.set)
tree.heading("ID", text="ID")
tree.heading("Title", text="Title")
tree.heading("Author", text="Author")
tree.column("ID", width=50, anchor="center")
tree.column("Title", width=250, anchor="w")
tree.column("Author", width=200, anchor="w")
tree.pack(fill=tk.BOTH, expand=True)
tree_scroll.config(command=tree.yview)

# --- Style Treeview ---
style = ttk.Style()
style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
style.configure("Treeview", font=("Helvetica", 11), rowheight=25)
style.map('Treeview', background=[('selected', '#ffcc00')], foreground=[('selected', 'black')])

# Initial load
view_books_gui()

# Run GUI
root.mainloop()

# Close DB connection on exit
conn.close()
