
import tkinter as tk
import tkinter.messagebox as messagebox
import sqlite3

class TruckManagementSystem(tk.Tk):
    def _init_(self):
        super()._init_()
        self.title("Truck Maintenance Management System")
        self.geometry("800x600")

        # Create and connect to the database
        self.create_database()

        # Create the login window
        self.login_window = LoginWindow(self)
        self.login_window.show()

    def create_database(self):
        # Create a new SQLite database or connect to an existing one
        self.conn = sqlite3.connect("truck_database.db")
        self.cursor = self.conn.cursor()

        # Create the "trucks" table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS trucks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plate_number TEXT NOT NULL,
                owner_name TEXT NOT NULL,
                driver_name TEXT NOT NULL,
                truck_type TEXT NOT NULL,
                phone_number TEXT NOT NULL
            )
        """)

        # Create the "maintenance_records" table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS maintenance_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                truck_id INTEGER NOT NULL,
                maintenance_date DATE NOT NULL,
                description TEXT NOT NULL,
                FOREIGN KEY (truck_id) REFERENCES trucks(id)
            )
        """)

        self.conn.commit()

    def add_truck(self, plate_number, owner_name, driver_name, truck_type, phone_number):
        # Insert a new truck into the "trucks" table
        self.cursor.execute("""
            INSERT INTO trucks (plate_number, owner_name, driver_name, truck_type, phone_number)
            VALUES (?, ?, ?, ?, ?)""",
            (plate_number, owner_name, driver_name, truck_type, phone_number))

        self.conn.commit()
        self.show_all_trucks()

    def update_truck(self, truck_id, plate_number, owner_name, driver_name, truck_type, phone_number):
        # Update the details of a truck in the "trucks" table based on its ID
        self.cursor.execute("""
            UPDATE trucks
            SET plate_number=?, owner_name=?, driver_name=?, truck_type=?, phone_number=?
            WHERE id=?""",
            (plate_number, owner_name, driver_name, truck_type, phone_number, truck_id))

        self.conn.commit()
        self.show_all_trucks()

    def delete_truck(self, truck_id):
        # Delete a truck from the "trucks" table based on its ID
        self.cursor.execute("""
            DELETE FROM trucks WHERE id=?""",
            (truck_id,))

        self.conn.commit()
        self.show_all_trucks()

    def add_maintenance_record(self, truck_id, maintenance_date, description):
        # Insert a new maintenance record into the "maintenance_records" table
        self.cursor.execute("""
            INSERT INTO maintenance_records (truck_id, maintenance_date, description)
            VALUES (?, ?, ?)""",
            (truck_id, maintenance_date, description))

        self.conn.commit()
        self.show_maintenance_records(truck_id)

    def update_maintenance_record(self, record_id, maintenance_date, description):
        # Update the details of a maintenance record in the "maintenance_records" table based on its ID
        self.cursor.execute("""
            UPDATE maintenance_records
            SET maintenance_date=?, description=?
            WHERE id=?""",
            (maintenance_date, description, record_id))

        self.conn.commit()
        self.show_maintenance_records(self.selected_truck_id)

    def delete_maintenance_record(self, record_id):
        # Delete a maintenance record from the "maintenance_records"
        
        self.cursor.execute("""
            DELETE FROM maintenance_records WHERE id=?""",
            (record_id,))

        self.conn.commit()
        self.show_maintenance_records(self.selected_truck_id)

    def get_all_trucks(self):
        # Fetch all trucks from the database
        self.cursor.execute("SELECT * FROM trucks")
        return self.cursor.fetchall()

    def get_maintenance_records(self, truck_id, date=None):
        # Fetch maintenance records for a specific truck and date (optional)
        if date:
            self.cursor.execute("SELECT * FROM maintenance_records WHERE truck_id=? AND maintenance_date=?", (truck_id, date))
        else:
            self.cursor.execute("SELECT * FROM maintenance_records WHERE truck_id=?", (truck_id,))

        return self.cursor.fetchall()

    def show_all_trucks(self):
        # Fetch all trucks from the database and display them in a listbox
        trucks = self.get_all_trucks()
        self.listbox_trucks.delete(0, tk.END)
        for truck in trucks:
            self.listbox_trucks.insert(tk.END, f"{truck[0]} - {truck[1]}")

    def show_maintenance_records(self, truck_id):
        # Fetch maintenance records for a specific truck and display them in a listbox
        records = self.get_maintenance_records(truck_id)
        self.listbox_records.delete(0, tk.END)
        for record in records:
            self.listbox_records.insert(tk.END, f"{record[0]} - {record[2]} - {record[3]}")

    def select_truck(self, event):
        # Get the selected truck's ID from the listbox and show its maintenance records
        selection = self.listbox_trucks.curselection()
        if selection:
            truck_id = self.listbox_trucks.get(selection[0]).split(" - ")[0]
            self.selected_truck_id = int(truck_id)
            self.show_maintenance_records(self.selected_truck_id)

    def backup_database(self):
        # Implement the backup function to backup the database
        # to a server or cloud storage
        messagebox.showinfo("Backup", "Database backup function to be implemented.")

class LoginWindow(tk.Toplevel):
    def _init_(self, master):
        super()._init_(master)
        self.title("Login")
        self.geometry("300x200")

        self.label_username = tk.Label(self, text="Username:")
        self.label_username.pack()
        self.entry_username = tk.Entry(self)
        self.entry_username.pack()

        self.label_password = tk.Label(self, text="Password:")
        self.label_password.pack()
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack()

        self.btn_login = tk.Button(self, text="Login", command=self.login)
        self.btn_login.pack()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username == "admin" and password == "password":
            self.destroy()
            self.master.create_components()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")

    def show(self):
        self.transient(self.master)
        self.grab_set()
        self.master.wait_window(self)

class AddTruckWindow(tk.Toplevel):
    def _init_(self, master):
        super()._init_(master)
        self.title("Add New Truck")
        self.geometry("400x300")

        self.label_plate_number = tk.Label