#  Spotlight
Help UTRGV students discover campus events, register, and optionally get paired with a buddy to attend together.

<img width="1440" height="900" alt="Screenshot 2025-08-23 at 2 32 02 PM" src="https://github.com/user-attachments/assets/690792e7-02e7-422b-8989-357424d66679" />

Members: 
Luciana Flores
Michael Amaro

# Project overview
Desktop App - developed by Michael Amaro
-   programming languages: Python, Tkinter 
-   database: .db (sqlite3)      

WebApp - developed by Luciana Flores
-   programming languages: Python, Django, HTML, CSS
-   database: SQLite3 (db.sqlite3)
-   framework: Django 5.2.5
-   features: User authentication, event management, RSVP system, responsive design


# Running Code

Desktop App
- a virtual enviroment is recommended, one is provided in the repo
- Hitting run on main.py with the spotlight.db on device, it should work.

WebApp
- Python 3.8+ installed
- Virtual environment (recommended)


## WebApp Features
###  User Management
- **User Registration & Login**:  
- **User Profiles**:  
- **Password Management**: 
- **Create Events**:  
- **Event Details**:  
- **Event Editing**:  
- **Event Deletion**: 
- **RSVP to Events**:  
- **RSVP Tracking**:  
- **Duplicate Prevention**:  
- **RSVP Count**: 
- **Home Page**:  
- **Event Detail**:  
- **My Events**:  
- **User Posts**:  
- **Profile Pages**:  



## File Structure
```
WebApp/
├── blog/                    # Main app for events
│   ├── models.py           # Event and RSVP models
│   ├── views.py            # View logic
│   ├── forms.py            # Form definitions
│   ├── urls.py             # URL routing
│   ├── templates/          # HTML templates
│   └── static/             # CSS, JS, images
├── users/                   # User management app
│   ├── models.py           # User profile model
│   ├── views.py            # User views
│   └── templates/          # User templates
├── django_project/          # Project settings
│   ├── settings.py         # Django configuration
│   └── urls.py             # Main URL routing
├── manage.py               # Django management script
└── db.sqlite3             # Database file
```
