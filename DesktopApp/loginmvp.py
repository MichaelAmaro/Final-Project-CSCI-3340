import tkinter as tk
import customtkinter as ctk  

# Theme setup
ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue") 

class SpotlightLogin:
    def __init__(self, on_register=None):
        self.on_register = on_register  # Optional callback for register screen

        self.root = ctk.CTk()  # Create main window
        self.root.title("Spotlight Login")  # Window title
        self.root.geometry("400x350")  # Window size

        # App title label
        title = ctk.CTkLabel(
            self.root, 
            text="🌟 Spotlight Login",
            font=ctk.CTkFont(size=24, weight="bold")  # Big bold title
        )
        title.pack(pady=(30, 10))  # Padding above & below

        # Email input
        self.email_entry = ctk.CTkEntry(
            self.root, 
            placeholder_text="UTRGV Email",  # Hint text 
            width=250
        )
        self.email_entry.pack(pady=10)  # Space between widgets

        # Password input
        self.password_entry = ctk.CTkEntry(
            self.root, 
            placeholder_text="Password",  # Hint text
            show="*",  # Hide text for password
            width=250
        )
        self.password_entry.pack(pady=10)

        # Login button
        login_button = ctk.CTkButton(
            self.root, 
            text="Login", 
            width=250, 
            command=self.login_action  # Function when clicked
        )
        login_button.pack(pady=20)

        # Register button (link style)
        register_btn = ctk.CTkButton(
            self.root,
            text="Register",  # Registration text
            fg_color="transparent",  # No background
            text_color="gray",  # Blue text
            hover=False,  # No hover effect
            command=self.register_action  # Function when clicked
        )
        register_btn.pack()

        self.root.mainloop()  # Run the app

    def login_action(self):
        # Get typed values
        email = self.email_entry.get()
        password = self.password_entry.get()
        print(f"[Login] {email=} {password=}")  # Placeholder action

    def register_action(self):
        # Open register screen if provided
        if callable(self.on_register):
            self.on_register()
        else:
            print("[Register] Open registration screen here")

if __name__ == "__main__":
    SpotlightLogin()
