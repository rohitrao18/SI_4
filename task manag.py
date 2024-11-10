import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# Connect to the SQLite database
conn = sqlite3.connect('task_tracking.db')
cursor = conn.cursor()

# Database setup
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    deadline TEXT,
    status TEXT DEFAULT 'Pending',
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
''')
conn.commit()

# GUI setup
root = tk.Tk()
root.title("Task Assignment and Tracking System")
root.geometry("600x400")

def add_user():
    username = user_entry.get()
    if username:
        cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
        conn.commit()
        user_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "User added successfully!")
    else:
        messagebox.showerror("Error", "Please enter a username.")

def assign_task():
    title = task_title_entry.get()
    description = task_desc_entry.get()
    deadline = task_deadline_entry.get()
    user_id = user_id_entry.get()
    
    if title and user_id and deadline:
        cursor.execute("INSERT INTO tasks (title, description, deadline, user_id) VALUES (?, ?, ?, ?)",
                       (title, description, deadline, user_id))
        conn.commit()
        task_title_entry.delete(0, tk.END)
        task_desc_entry.delete(0, tk.END)
        task_deadline_entry.delete(0, tk.END)
        user_id_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Task assigned successfully!")
    else:
        messagebox.showerror("Error", "Please fill in all required fields.")

def view_tasks():
    task_list.delete(0, tk.END)
    cursor.execute("SELECT tasks.id, title, description, deadline, status, username FROM tasks "
                   "JOIN users ON tasks.user_id = users.id")
    tasks = cursor.fetchall()
    
    for task in tasks:
        task_info = f"ID: {task[0]}, Title: {task[1]}, Description: {task[2]}, Deadline: {task[3]}, Status: {task[4]}, Assigned to: {task[5]}"
        task_list.insert(tk.END, task_info)

def update_task_status():
    task_id = task_id_entry.get()
    new_status = task_status_entry.get()
    
    if task_id and new_status:
        cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
        conn.commit()
        task_id_entry.delete(0, tk.END)
        task_status_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Task status updated successfully!")
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

# User Interface Elements
# User Management
tk.Label(root, text="Add User:").grid(row=0, column=0)
user_entry = tk.Entry(root)
user_entry.grid(row=0, column=1)
tk.Button(root, text="Add User", command=add_user).grid(row=0, column=2)

# Task Assignment
tk.Label(root, text="Task Title:").grid(row=1, column=0)
task_title_entry = tk.Entry(root)
task_title_entry.grid(row=1, column=1)

tk.Label(root, text="Task Description:").grid(row=2, column=0)
task_desc_entry = tk.Entry(root)
task_desc_entry.grid(row=2, column=1)

tk.Label(root, text="Deadline (YYYY-MM-DD):").grid(row=3, column=0)
task_deadline_entry = tk.Entry(root)
task_deadline_entry.grid(row=3, column=1)

tk.Label(root, text="Assign to User ID:").grid(row=4, column=0)
user_id_entry = tk.Entry(root)
user_id_entry.grid(row=4, column=1)

tk.Button(root, text="Assign Task", command=assign_task).grid(row=5, column=1)

# Task Viewing and Updating
tk.Button(root, text="View All Tasks", command=view_tasks).grid(row=6, column=1)

tk.Label(root, text="Update Task ID:").grid(row=7, column=0)
task_id_entry = tk.Entry(root)
task_id_entry.grid(row=7, column=1)

tk.Label(root, text="New Status (Pending/Complete):").grid(row=8, column=0)
task_status_entry = tk.Entry(root)
task_status_entry.grid(row=8, column=1)

tk.Button(root, text="Update Task Status", command=update_task_status).grid(row=9, column=1)

# Task List Display
task_list = tk.Listbox(root, width=80, height=10)
task_list.grid(row=10, column=0, columnspan=3)

# Run the application
root.mainloop()

# Close the database connection when done
conn.close()
