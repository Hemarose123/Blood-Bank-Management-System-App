import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta

# Database setup
def initialize_db():
    conn = sqlite3.connect("advanced_blood_bank.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS donors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            blood_group TEXT NOT NULL,
            contact TEXT NOT NULL,
            last_donation_date TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donor_id INTEGER,
            donation_date TEXT,
            FOREIGN KEY (donor_id) REFERENCES donors(id)
        )
    """)
    conn.commit()
    conn.close()

# Add new donor
def add_donor(name, age, blood_group, contact, last_donation_date):
    conn = sqlite3.connect("advanced_blood_bank.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO donors (name, age, blood_group, contact, last_donation_date) VALUES (?, ?, ?, ?, ?)",
                   (name, age, blood_group, contact, last_donation_date))
    conn.commit()
    conn.close()

# Add donation entry
def add_donation(donor_id, donation_date):
    conn = sqlite3.connect("advanced_blood_bank.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO donations (donor_id, donation_date) VALUES (?, ?)", (donor_id, donation_date))
    conn.commit()
    conn.close()

# Search donors
def search_donors(criteria, value):
    conn = sqlite3.connect("advanced_blood_bank.db")
    cursor = conn.cursor()
    if criteria == "blood_group":
        cursor.execute("SELECT * FROM donors WHERE blood_group = ?", (value,))
    elif criteria == "name":
        cursor.execute("SELECT * FROM donors WHERE name LIKE ?", ('%' + value + '%',))
    results = cursor.fetchall()
    conn.close()
    return results

# Fetch all donors
def fetch_all_donors():
    conn = sqlite3.connect("advanced_blood_bank.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donors")
    results = cursor.fetchall()
    conn.close()
    return results

# Check donor eligibility
def is_eligible(last_donation_date):
    if not last_donation_date:
        return True
    last_date = datetime.strptime(last_donation_date, "%Y-%m-%d")
    return datetime.now() >= last_date + timedelta(days=90)

# Main app class
class AdvancedBloodBankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Blood Bank Management System")
        self.root.geometry("800x600")

        # Variables
        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.blood_group_var = tk.StringVar()
        self.contact_var = tk.StringVar()
        self.last_donation_date_var = tk.StringVar()

        self.search_var = tk.StringVar()
        self.search_type = tk.StringVar(value="blood_group")

        self.create_widgets()

    def create_widgets(self):
        # Add Donor Section
        tk.Label(self.root, text="Donor Registration", font=("Arial", 16)).pack(pady=10)
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10)
        tk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(form_frame, textvariable=self.name_var).grid(row=0, column=1, padx=5, pady=5)
        tk.Label(form_frame, text="Age:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(form_frame, textvariable=self.age_var).grid(row=1, column=1, padx=5, pady=5)
        tk.Label(form_frame, text="Blood Group:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(form_frame, textvariable=self.blood_group_var).grid(row=2, column=1, padx=5, pady=5)
        tk.Label(form_frame, text="Contact:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(form_frame, textvariable=self.contact_var).grid(row=3, column=1, padx=5, pady=5)
        tk.Label(form_frame, text="Last Donation Date (YYYY-MM-DD):").grid(row=4, column=0, padx=5, pady=5)
        tk.Entry(form_frame, textvariable=self.last_donation_date_var).grid(row=4, column=1, padx=5, pady=5)
        tk.Button(form_frame, text="Add Donor", command=self.add_donor).grid(row=5, columnspan=2, pady=10)

        # Search Section
        tk.Label(self.root, text="Search Donors", font=("Arial", 16)).pack(pady=10)
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10)
        tk.Radiobutton(search_frame, text="Blood Group", variable=self.search_type, value="blood_group").grid(row=0, column=0)
        tk.Radiobutton(search_frame, text="Name", variable=self.search_type, value="name").grid(row=0, column=1)
        tk.Entry(search_frame, textvariable=self.search_var).grid(row=0, column=2, padx=10)
        tk.Button(search_frame, text="Search", command=self.search_donors).grid(row=0, column=3)

        # Donor List
        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Age", "Blood Group", "Contact", "Last Donation"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Age", text="Age")
        self.tree.heading("Blood Group", text="Blood Group")
        self.tree.heading("Contact", text="Contact")
        self.tree.heading("Last Donation", text="Last Donation")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.load_donors()

    def add_donor(self):
        name = self.name_var.get()
        age = self.age_var.get()
        blood_group = self.blood_group_var.get()
        contact = self.contact_var.get()
        last_donation_date = self.last_donation_date_var.get()

        if name and age and blood_group and contact:
            if last_donation_date:
                try:
                    datetime.strptime(last_donation_date, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
                    return
            add_donor(name, int(age), blood_group, contact, last_donation_date)
            messagebox.showinfo("Success", "Donor added successfully!")
            self.load_donors()
            self.clear_inputs()
        else:
            messagebox.showwarning("Error", "All fields are required!")

    def search_donors(self):
        criteria = self.search_type.get()
        value = self.search_var.get()
        if value:
            donors = search_donors(criteria, value)
            self.update_tree(donors)
        else:
            messagebox.showwarning("Error", "Please enter a search value!")

    def load_donors(self):
        donors = fetch_all_donors()
        self.update_tree(donors)

    def update_tree(self, donors):
        self.tree.delete(*self.tree.get_children())
        for donor in donors:
            self.tree.insert("", tk.END, values=donor)

    def clear_inputs(self):
        self.name_var.set("")
        self.age_var.set("")
        self.blood_group_var.set("")
        self.contact_var.set("")
        self.last_donation_date_var.set("")

# Run the app
if __name__ == "__main__":
    initialize_db()
    root = tk.Tk()
    app = AdvancedBloodBankApp(root)
    root.mainloop()
