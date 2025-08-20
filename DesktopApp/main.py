import tkinter as tk
from tkinter import messagebox, font, simpledialog
import sqlite3
import calendar
from datetime import datetime
import random 

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# DATABASE SETUP
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

def setup_database():
    """Initializes the database and creates tables if they don't exist."""
    with sqlite3.connect('Spotlight.db') as conn:
        cursor = conn.cursor()

        # --- studentuser Table ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS studentuser(
                first_name TEXT,
                last_name TEXT,
                student_id TEXT,
                email TEXT PRIMARY KEY,
                major TEXT,
                password TEXT,
                role TEXT DEFAULT 'student',
                organization TEXT
            )
        """)

        # --- org_requests Table ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS org_requests(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                organization TEXT,
                status TEXT DEFAULT 'pending'
            )
        """)
        
        # --- events Table ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                location TEXT,
                description TEXT,
                organization_email TEXT 
            )
        """)

        # --- comments Table ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comments(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id INTEGER,
                user_email TEXT,
                comment_text TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (event_id) REFERENCES events(id)
            )
        """)
        
        # --- rsvps Table ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rsvps(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id INTEGER,
                user_email TEXT,
                find_vaquero BOOLEAN,
                FOREIGN KEY (event_id) REFERENCES events(id),
                UNIQUE(event_id, user_email)
            )
        """)

        # --- vaquero_matches Table ---
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vaquero_matches(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id INTEGER,
                user1_email TEXT,
                user2_email TEXT,
                FOREIGN KEY (event_id) REFERENCES events(id)
            )
        """)

        # --- Ensure dean user exists ---
        cursor.execute("SELECT * FROM studentuser WHERE email=?", ("dean@utrgv.edu",))
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO studentuser (first_name, last_name, student_id, email, major, password, role) VALUES (?, ?, ?, ?, ?, ?, ?)",
                ("dean", "pelton", "00000000", "dean@utrgv.edu", "Administration", "dalmatians", "dean")
            )
        
        conn.commit()

# Run database setup on start
setup_database()


# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# DATA LOADING FUNCTIONS
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

def load_users():
    """Loads user emails and passwords from the database into a dictionary."""
    users = {}
    with sqlite3.connect('Spotlight.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT email, password FROM studentuser")
        for email, password in cursor.fetchall():
            users[email] = password
    return users

def get_user_details(email):
    """Fetches all details for a specific user from the database."""
    if not email:
        return None
    with sqlite3.connect('Spotlight.db') as conn:
        conn.row_factory = sqlite3.Row # Allows accessing columns by name
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM studentuser WHERE email=?", (email,))
        user_data = cursor.fetchone()
        if user_data:
            return dict(user_data)
    return None


def load_events_from_db():
    """Loads all events from the database."""
    with sqlite3.connect('Spotlight.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, date, location, description FROM events ORDER BY date")
        events_data = []
        for row in cursor.fetchall():
            events_data.append({
                "id": row[0],
                "name": row[1],
                "date": row[2],
                "location": row[3],
                "description": row[4]
            })
    return events_data

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# MAIN APPLICATION CLASS
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

class VSpotlightApp(tk.Tk):
    """The main application window for V Spotlight."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("V Spotlight - UTRGV Event Hub")
        self.geometry("900x700")
        self.configure(bg="#f0f0f0")
        
        # --- User state ---
        self.current_user_email = None
        self.current_user_details = None

        # --- Font & Color Scheme ---
        self.title_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.header_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.body_font = font.Font(family="Helvetica", size=11)
        self.utrgv_orange = "#f05023"
        self.utrgv_background = "#9E9B9B"
        self.utrgv_gray = "#6C6C6C"

        container = tk.Frame(self, bg="#f0f0f0")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, MainPage, RegisterPage, CalendarPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        """Show a frame for the given page name."""
        frame = self.frames[page_name]
        if page_name in ['MainPage', 'CalendarPage']:
            frame.refresh_data() 
        frame.tkraise()
        
    def login_user(self, email):
        """Sets the current user's state after a successful login."""
        self.current_user_email = email
        self.current_user_details = get_user_details(email)
        self.show_frame("MainPage")

    def logout_user(self):
        """Logs out the current user and returns to the login page."""
        self.current_user_email = None
        self.current_user_details = None
        self.show_frame("LoginPage")

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# LOGIN PAGE
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

class LoginPage(tk.Frame):
    """Login screen for users."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.utrgv_background)
        self.controller = controller

        login_frame = tk.Frame(self, bg="white", padx=40, pady=40, relief="ridge", borderwidth=2)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        title_label = tk.Label(login_frame, text="V Spotlight", font=controller.title_font, bg="white", fg=controller.utrgv_orange)
        title_label.pack(pady=(0, 20))

        username_label = tk.Label(login_frame, text="Username (Email)", font=controller.body_font, bg="white")
        username_label.pack(anchor="w")
        self.username_entry = tk.Entry(login_frame, font=controller.body_font, width=30)
        self.username_entry.pack(pady=(5, 15))

        password_label = tk.Label(login_frame, text="Password", font=controller.body_font, bg="white")
        password_label.pack(anchor="w")
        self.password_entry = tk.Entry(login_frame, show="*", font=controller.body_font, width=30)
        self.password_entry.pack(pady=5)

        login_button = tk.Button(login_frame, text="Login", font=controller.header_font, bg=controller.utrgv_orange, fg="white", command=self.login)
        login_button.pack(pady=20, fill="x")

        register_button = tk.Button(login_frame, text="Register New User", font=controller.header_font, bg=controller.utrgv_gray, fg="white", command=lambda: controller.show_frame("RegisterPage"))
        register_button.pack(pady=(0, 10), fill="x")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

        with sqlite3.connect('Spotlight.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM studentuser WHERE email=?", (username,))
            row = cursor.fetchone()
            if row and row[0] == password:
                messagebox.showinfo("Login Success", f"Welcome, {username}!")
                self.controller.login_user(username)
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# REGISTRATION PAGE
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
class RegisterPage(tk.Frame):
    """Registration screen for new users."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.utrgv_background)
        self.controller = controller

        reg_frame = tk.Frame(self, bg="white", padx=40, pady=30, relief="ridge", borderwidth=2)
        reg_frame.place(relx=0.5, rely=0.5, anchor="center")

        title_label = tk.Label(reg_frame, text="Create New Account", font=controller.title_font, bg="white", fg=controller.utrgv_orange)
        title_label.pack(pady=(0, 20))

        fields = ["First Name", "Last Name", "Student ID", "Student Email", "Major", "Password", "Confirm Password"]
        self.entries = {}
        for field in fields:
            label = tk.Label(reg_frame, text=field, font=controller.body_font, bg="white")
            label.pack(anchor="w", padx=5, pady=(5,0))
            entry = tk.Entry(reg_frame, font=controller.body_font, width=40)
            if "Password" in field:
                entry.config(show="*")
            entry.pack(anchor="w", padx=5, pady=(0,5))
            self.entries[field] = entry

        button_frame = tk.Frame(reg_frame, bg="white")
        button_frame.pack(pady=20, fill="x")

        submit_button = tk.Button(button_frame, text="Submit", font=controller.header_font, bg=controller.utrgv_orange, fg="white", command=self.register_user)
        submit_button.pack(side="left", expand=True, padx=(0, 5))

        back_button = tk.Button(button_frame, text="Back to Login", font=controller.header_font, bg=controller.utrgv_gray, fg="white", command=lambda: controller.show_frame("LoginPage"))
        back_button.pack(side="right", expand=True, padx=(5, 0))

    def register_user(self):
        first_name = self.entries["First Name"].get()
        last_name = self.entries["Last Name"].get()
        student_id = self.entries["Student ID"].get()
        email = self.entries["Student Email"].get()
        major = self.entries["Major"].get()
        password = self.entries["Password"].get()
        confirm_password = self.entries["Confirm Password"].get()

        if not all([first_name, last_name, student_id, email, major, password, confirm_password]):
            messagebox.showerror("Error", "All fields must be filled out.")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return
            
        if not email.lower().strip().endswith("@utrgv.edu"):
            messagebox.showerror("Invalid Email", "Please use a valid @utrgv.edu university email to register.")
            return

        with sqlite3.connect('Spotlight.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM studentuser WHERE email=?", (email,))
            if cursor.fetchone():
                messagebox.showerror("Error", "An account with this email already exists.")
                return

            try:
                cursor.execute(
                    "INSERT INTO studentuser (first_name, last_name, student_id, email, major, password) VALUES (?, ?, ?, ?, ?, ?)",
                    (first_name, last_name, student_id, email, major, password)
                )
                conn.commit()
            except Exception as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
                return

        messagebox.showinfo("Success", "Account created successfully! Please log in.")
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.controller.show_frame("LoginPage")

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# MAIN APPLICATION PAGE
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

class MainPage(tk.Frame):
    """Main application interface showing events and details."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        self.selected_event_id = None
        self.events = []

        self.columnconfigure(0, weight=1, minsize=300)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(1, weight=1)

        # --- Header ---
        self.header_frame = tk.Frame(self, bg=controller.utrgv_background, pady=10)
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        header_label = tk.Label(self.header_frame, text="UTRGV Campus Events", font=controller.title_font, bg=controller.utrgv_background, fg="white")
        header_label.pack(side="left", padx=20)
        
        sign_out_button = tk.Button(self.header_frame, text="Sign Out", font=controller.header_font, bg=controller.utrgv_gray, fg="white", command=self.controller.logout_user)
        sign_out_button.pack(side="right", padx=10)

        calendar_button = tk.Button(self.header_frame, text="View Calendar", font=controller.header_font, bg=controller.utrgv_orange, fg="white", command=lambda: controller.show_frame("CalendarPage"))
        calendar_button.pack(side="right", padx=20)

        # --- Left Panel: Events List ---
        left_panel = tk.Frame(self, bg="white", padx=10, pady=10)
        left_panel.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=10)
        left_panel.rowconfigure(1, weight=1)
        
        events_label = tk.Label(left_panel, text="Upcoming Events", font=controller.header_font, bg="white", fg=controller.utrgv_gray)
        events_label.grid(row=0, column=0, sticky="w", pady=(0, 10))

        self.events_listbox = tk.Listbox(left_panel, font=controller.body_font, selectbackground=controller.utrgv_orange, relief="flat")
        self.events_listbox.grid(row=1, column=0, sticky="nsew")
        self.events_listbox.bind("<<ListboxSelect>>", self.on_event_select)

        # --- Right Panel: Event Details ---
        right_panel = tk.Frame(self, bg="white", padx=20, pady=20)
        right_panel.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=10)
        right_panel.rowconfigure(3, weight=1) # Make comment section expand

        self.event_title = tk.Label(right_panel, text="Select an Event", font=controller.title_font, bg="white", wraplength=500, justify="left")
        self.event_title.pack(anchor="w", pady=(0, 10))

        self.event_info = tk.Label(right_panel, text="Details will be shown here.", font=controller.body_font, bg="white", wraplength=500, justify="left")
        self.event_info.pack(anchor="w", pady=(0, 20))
        
        self.event_description = tk.Message(right_panel, text="", font=controller.body_font, bg="white", width=500)
        self.event_description.pack(anchor="w", pady=(0, 20))

        self.rsvp_button = tk.Button(right_panel, text="RSVP for this Event", font=controller.header_font, bg="#228B22", fg="white", state=tk.DISABLED, command=self.open_rsvp_window)
        self.rsvp_button.pack(anchor="w", pady=(10, 20))
        
        # --- Comments Section ---
        comments_frame = tk.Frame(right_panel, bg="white")
        comments_frame.pack(fill="both", expand=True, pady=(10,0))
        comments_frame.columnconfigure(0, weight=1)
        comments_frame.rowconfigure(1, weight=1)

        comments_label = tk.Label(comments_frame, text="Comments", font=controller.header_font, bg="white", fg=controller.utrgv_gray)
        comments_label.grid(row=0, column=0, sticky="w")
        
        self.comments_text = tk.Text(comments_frame, height=6, font=controller.body_font, relief="solid", bg="#fafafa", wrap="word", borderwidth=1)
        self.comments_text.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=5)
        self.comments_text.config(state=tk.NORMAL)

        self.comment_entry = tk.Entry(comments_frame, font=controller.body_font, width=50)
        self.comment_entry.grid(row=2, column=0, sticky="ew", pady=5)
        
        self.post_comment_button = tk.Button(comments_frame, text="Post", font=controller.body_font, bg=controller.utrgv_orange, fg="white", command=self.post_comment)
        self.post_comment_button.grid(row=2, column=1, sticky="e", padx=(5,0))

    def setup_header_buttons(self):
        """Dynamically adds buttons to the header based on user role."""
        # --- MODIFIED: Clear existing dynamic buttons ---
        for widget in self.header_frame.winfo_children():
            # Keep the main title and static buttons
            if widget.cget("text") not in ["UTRGV Campus Events", "View Calendar", "Sign Out"]:
                widget.destroy()

        details = self.controller.current_user_details
        if not details: return

        role = details.get('role')

        # --- MODIFIED: Conditional button creation based on role ---
        if role == 'dean':
            approve_button = tk.Button(self.header_frame, text="Approve Org Requests", font=self.controller.header_font, bg="#228B22", fg="white", command=self.open_approval_window)
            approve_button.pack(side="right", padx=10)
        
        elif role == 'organization':
            create_event_button = tk.Button(self.header_frame, text="Create Event", font=self.controller.header_font, bg="#007bff", fg="white", command=self.open_create_event_window)
            create_event_button.pack(side="right", padx=10)
        
        elif role == 'student':
            # Only show "Apply" button to users with the default 'student' role
            apply_org_button = tk.Button(self.header_frame, text="Apply as Organization", font=self.controller.header_font, bg=self.controller.utrgv_gray, fg="white", command=self.open_org_application)
            apply_org_button.pack(side="right", padx=10)


    def refresh_data(self):
        """Populates the event listbox with event names from the database."""
        self.setup_header_buttons()
        self.events = load_events_from_db()
        self.events_listbox.delete(0, tk.END)
        for event in self.events:
            self.events_listbox.insert(tk.END, event["name"])
        self.clear_details()

    def on_event_select(self, event):
        selection_indices = self.events_listbox.curselection()
        if not selection_indices: return
        
        selected_index = selection_indices[0]
        event_data = self.events[selected_index]
        self.selected_event_id = event_data["id"]
        
        self.event_title.config(text=event_data["name"])
        self.event_info.config(text=f"Date: {event_data['date']} | Location: {event_data['location']}")
        self.event_description.config(text=event_data["description"])
        
        self.rsvp_button.config(state=tk.NORMAL)
        self.load_comments()

    def load_comments(self):
        """Loads and displays comments for the selected event."""
        if self.selected_event_id is None: return
        
        self.comments_text.config(state=tk.NORMAL)
        self.comments_text.delete("1.0", tk.END)

        with sqlite3.connect('Spotlight.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT user_email, comment_text, strftime('%Y-%m-%d %H:%M', timestamp) 
                FROM comments WHERE event_id=? ORDER BY timestamp DESC
            """, (self.selected_event_id,))
            comments = cursor.fetchall()
        
        if comments:
            for email, comment, ts in comments:
                self.comments_text.insert(tk.END, f"{email.split('@')[0]} ({ts}):\n", ("user_email",))
                self.comments_text.insert(tk.END, f"{comment}\n\n")
        else:
            self.comments_text.insert(tk.END, "No comments yet. Be the first to comment!")
        
        self.comments_text.tag_config("user_email", font=font.Font(family="Helvetica", size=10, weight="bold"))
        self.comments_text.config(state=tk.NORMAL)

    def post_comment(self):
        """Saves a new comment to the database."""
        comment_text = self.comment_entry.get().strip()
        if not comment_text:
            messagebox.showwarning("Empty Comment", "Cannot post an empty comment.")
            return
        if self.selected_event_id is None:
            messagebox.showwarning("No Event", "Please select an event to comment on.")
            return

        with sqlite3.connect('Spotlight.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO comments (event_id, user_email, comment_text) VALUES (?, ?, ?)",
                (self.selected_event_id, self.controller.current_user_email, comment_text)
            )
            conn.commit()
        
        self.comment_entry.delete(0, tk.END)
        self.load_comments()

    def clear_details(self):
        self.selected_event_id = None
        self.event_title.config(text="Select an Event")
        self.event_info.config(text="Details will be shown here.")
        self.event_description.config(text="")
        self.rsvp_button.config(state=tk.DISABLED)
        self.comments_text.config(state=tk.NORMAL)
        self.comments_text.delete("1.0", tk.END)
        self.comments_text.config(state=tk.DISABLED)

    def open_rsvp_window(self):
        """Opens a window to RSVP and opt-in to Find a Vaquero."""
        if self.selected_event_id is None:
            return

        rsvp_win = tk.Toplevel(self)
        rsvp_win.title("RSVP")
        rsvp_win.geometry("350x200")
        
        tk.Label(rsvp_win, text="Confirm your RSVP for this event.", font=self.controller.body_font).pack(pady=10)
        
        find_vaquero_var = tk.BooleanVar()
        tk.Checkbutton(rsvp_win, text="Find a Vaquero: Match with another student!", variable=find_vaquero_var, font=self.controller.body_font).pack(pady=10)

        def submit_rsvp():
            find_vaquero = find_vaquero_var.get()
            user_email = self.controller.current_user_email
            
            with sqlite3.connect('Spotlight.db') as conn:
                cursor = conn.cursor()
                try:
                    cursor.execute(
                        "INSERT INTO rsvps (event_id, user_email, find_vaquero) VALUES (?, ?, ?)",
                        (self.selected_event_id, user_email, find_vaquero)
                    )
                    conn.commit()
                    messagebox.showinfo("RSVP Confirmed", "Your RSVP has been recorded.", parent=rsvp_win)
                    
                    if find_vaquero:
                        self.find_vaquero_match(self.selected_event_id, user_email)

                except sqlite3.IntegrityError:
                    messagebox.showwarning("Already RSVP'd", "You have already RSVP'd for this event.", parent=rsvp_win)
            
            rsvp_win.destroy()

        tk.Button(rsvp_win, text="Confirm RSVP", command=submit_rsvp, bg=self.controller.utrgv_orange, fg="white", font=self.controller.header_font).pack(pady=20)

    def find_vaquero_match(self, event_id, current_user_email):
        """Logic to find a match for the 'Find a Vaquero' feature."""
        current_user_details = self.controller.current_user_details
        
        with sqlite3.connect('Spotlight.db') as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("""
                SELECT r.user_email, u.major 
                FROM rsvps r
                JOIN studentuser u ON r.user_email = u.email
                WHERE r.event_id = ? 
                  AND r.find_vaquero = 1 
                  AND r.user_email != ?
                  AND r.user_email NOT IN (SELECT user1_email FROM vaquero_matches WHERE event_id = ?)
                  AND r.user_email NOT IN (SELECT user2_email FROM vaquero_matches WHERE event_id = ?)
            """, (event_id, current_user_email, event_id, event_id))
            
            potential_matches = [dict(row) for row in cursor.fetchall()]

            if not potential_matches:
                return

            same_major_matches = [p for p in potential_matches if p['major'] == current_user_details['major']]
            
            match_found = None
            if same_major_matches:
                match_found = random.choice(same_major_matches)
            else:
                match_found = random.choice(potential_matches)

            if match_found:
                matched_user_email = match_found['user_email']
                
                cursor.execute(
                    "INSERT INTO vaquero_matches (event_id, user1_email, user2_email) VALUES (?, ?, ?)",
                    (event_id, current_user_email, matched_user_email)
                )
                conn.commit()
                
                matched_user_details = get_user_details(matched_user_email)
                
                messagebox.showinfo("Vaquero Found!", 
                                    f"You've been matched with another Vaquero!\n\n"
                                    f"Name: {matched_user_details['first_name']} {matched_user_details['last_name']}\n"
                                    f"Email: {matched_user_details['email']}\n\n"
                                    f"Feel free to connect before the event!")


    def open_org_application(self):
        app_win = tk.Toplevel(self)
        app_win.title("Organization Application")
        app_win.geometry("350x250")
        
        tk.Label(app_win, text="Full Name:").pack(anchor="w", padx=10, pady=(10,0))
        name_entry = tk.Entry(app_win, width=30)
        name_entry.pack(padx=10)
        
        tk.Label(app_win, text="Your UTRGV Email:").pack(anchor="w", padx=10, pady=(10,0))
        email_entry = tk.Entry(app_win, width=30)
        email_entry.pack(padx=10)

        if self.controller.current_user_email:
            email_entry.insert(0, self.controller.current_user_email)
            email_entry.config(state='readonly')

        tk.Label(app_win, text="Organization Name:").pack(anchor="w", padx=10, pady=(10,0))
        org_entry = tk.Entry(app_win, width=30)
        org_entry.pack(padx=10)

        def submit():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            org = org_entry.get().strip()
            if not all([name, email, org]):
                messagebox.showerror("Error", "All fields are required.", parent=app_win)
                return
            with sqlite3.connect('Spotlight.db') as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO org_requests (name, email, organization) VALUES (?, ?, ?)", (name, email, org))
                conn.commit()
            messagebox.showinfo("Submitted", "Your application has been submitted for approval.", parent=app_win)
            app_win.destroy()
        tk.Button(app_win, text="Submit", command=submit, bg="#f05023", fg="white").pack(pady=20)

    def open_approval_window(self):
        win = tk.Toplevel(self)
        win.title("Approve Organization Requests")
        win.geometry("500x400")
        
        with sqlite3.connect('Spotlight.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email, organization FROM org_requests WHERE status='pending'")
            requests = cursor.fetchall()

        if not requests:
            tk.Label(win, text="No pending requests.").pack(pady=20)
            return

        for req_id, name, email, org in requests:
            frame = tk.Frame(win, pady=5)
            frame.pack(fill="x", padx=10)
            tk.Label(frame, text=f"{name} ({email}) - Org: {org}", anchor="w").pack(side="left", expand=True, fill='x')
            
            def approve_action(req_id=req_id, email=email, org=org):
                with sqlite3.connect('Spotlight.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE org_requests SET status='approved' WHERE id=?", (req_id,))
                    cursor.execute("UPDATE studentuser SET role='organization', organization=? WHERE email=?", (org, email))
                    conn.commit()
                messagebox.showinfo("Approved", f"{email} is now an Organization user for {org}.", parent=win)
                win.destroy()
                self.open_approval_window()
            
            tk.Button(frame, text="Approve", bg="#228B22", fg="white", command=approve_action).pack(side="right")

    def open_create_event_window(self):
        """Opens a dialog for organization users to create a new event."""
        win = tk.Toplevel(self)
        win.title("Create New Event")
        win.geometry("400x400")

        fields = ["Event Name", "Date (YYYY-MM-DD)", "Location", "Description"]
        entries = {}
        for field in fields:
            tk.Label(win, text=field).pack(anchor="w", padx=20, pady=(10,0))
            if field == "Description":
                entry = tk.Text(win, height=5, width=40)
            else:
                entry = tk.Entry(win, width=40)
            entry.pack(padx=20)
            entries[field] = entry
        
        def submit_event():
            name = entries["Event Name"].get().strip()
            date = entries["Date (YYYY-MM-DD)"].get().strip()
            location = entries["Location"].get().strip()
            # --- FIXED: Corrected typo from '..' to '.' ---
            description = entries["Description"].get("1.0", tk.END).strip()

            if not all([name, date, location, description]):
                messagebox.showerror("Error", "All fields must be filled out.", parent=win)
                return
            
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid Date", "Please use YYYY-MM-DD format for the date.", parent=win)
                return

            with sqlite3.connect('Spotlight.db') as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO events (name, date, location, description, organization_email) VALUES (?, ?, ?, ?, ?)",
                    (name, date, location, description, self.controller.current_user_email)
                )
                conn.commit()
            
            messagebox.showinfo("Success", "Event created successfully!", parent=win)
            win.destroy()
            self.refresh_data()

        tk.Button(win, text="Create Event", command=submit_event, bg=self.controller.utrgv_orange, fg="white").pack(pady=20)

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# CALENDAR PAGE
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
class CalendarPage(tk.Frame):
    """Displays a monthly event calendar."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        self.year = datetime.now().year
        self.month = datetime.now().month
        self.events = []
        self.event_dates = set()

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        header_frame = tk.Frame(self, bg=controller.utrgv_background, pady=10)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        header_label = tk.Label(header_frame, text="Event Calendar", font=controller.title_font, bg=controller.utrgv_background, fg="white")
        header_label.pack(side="left", padx=20)
        back_button = tk.Button(header_frame, text="Back to List", font=controller.header_font, bg=controller.utrgv_orange, fg="white", command=lambda: controller.show_frame("MainPage"))
        back_button.pack(side="right", padx=20)

        calendar_panel = tk.Frame(self, bg="white", padx=10, pady=10)
        calendar_panel.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=10)

        nav_frame = tk.Frame(calendar_panel, bg="white")
        nav_frame.pack(pady=10)
        prev_button = tk.Button(nav_frame, text="<", command=self.prev_month, font=controller.header_font)
        prev_button.pack(side="left")
        self.month_label = tk.Label(nav_frame, text="", font=controller.title_font, bg="white", width=20)
        self.month_label.pack(side="left", padx=10)
        next_button = tk.Button(nav_frame, text=">", command=self.next_month, font=controller.header_font)
        next_button.pack(side="left")

        self.calendar_frame = tk.Frame(calendar_panel, bg="white")
        self.calendar_frame.pack()

        details_panel = tk.Frame(self, bg="white", padx=20, pady=20)
        details_panel.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=10)
        self.details_label = tk.Label(details_panel, text="Select a date to see events", font=controller.header_font, bg="white")
        self.details_label.pack(anchor="w")
        self.details_text = tk.Text(details_panel, font=controller.body_font, bg="#fafafa", relief="flat", wrap="word")
        self.details_text.pack(fill="both", expand=True, pady=10)
        self.details_text.config(state=tk.DISABLED)

    def draw_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        self.month_label.config(text=f"{calendar.month_name[self.month]} {self.year}")

        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for i, day in enumerate(days):
            lbl = tk.Label(self.calendar_frame, text=day, font=self.controller.header_font, bg="white")
            lbl.grid(row=0, column=i, padx=5, pady=5)

        month_days = calendar.monthcalendar(self.year, self.month)
        for row_idx, week in enumerate(month_days, 1):
            for col_idx, day_num in enumerate(week):
                if day_num == 0: continue
                
                day_date = datetime(self.year, self.month, day_num).date()
                btn_bg = "white"
                btn_fg = "black"
                btn_font = self.controller.body_font
                
                if day_date in self.event_dates:
                    btn_bg = self.controller.utrgv_orange
                    btn_fg = "white"
                    btn_font = font.Font(family="Helvetica", size=11, weight="bold")

                btn = tk.Button(self.calendar_frame, text=str(day_num), width=4, height=2,
                                bg=btn_bg, fg=btn_fg, font=btn_font,
                                command=lambda d=day_num: self.show_day_events(d))
                btn.grid(row=row_idx, column=col_idx, padx=2, pady=2)

    def prev_month(self):
        self.month -= 1
        if self.month == 0:
            self.month = 12
            self.year -= 1
        self.draw_calendar()
        self.clear_details()

    def next_month(self):
        self.month += 1
        if self.month == 13:
            self.month = 1
            self.year += 1
        self.draw_calendar()
        self.clear_details()

    def show_day_events(self, day):
        selected_date_str = f"{self.year}-{self.month:02d}-{day:02d}"
        self.details_label.config(text=f"Events for {selected_date_str}")
        
        day_events = [e for e in self.events if e["date"] == selected_date_str]
        
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete("1.0", tk.END)
        if day_events:
            for event in day_events:
                self.details_text.insert(tk.END, f"Event: {event['name']}\n")
                self.details_text.insert(tk.END, f"Location: {event['location']}\n")
                self.details_text.insert(tk.END, f"Description: {event['description']}\n\n")
        else:
            self.details_text.insert(tk.END, "No events scheduled for this day.")
        self.details_text.config(state=tk.DISABLED)

    def clear_details(self):
        self.details_label.config(text="Select a date to see events")
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete("1.0", tk.END)
        self.details_text.config(state=tk.DISABLED)

    def refresh_data(self):
        """Called when the frame is shown."""
        self.events = load_events_from_db()
        self.event_dates = {datetime.strptime(e["date"], "%Y-%m-%d").date() for e in self.events}
        self.draw_calendar()
        self.clear_details()

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# APPLICATION STARTUP
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

if __name__ == "__main__":
    app = VSpotlightApp()
    app.mainloop()
