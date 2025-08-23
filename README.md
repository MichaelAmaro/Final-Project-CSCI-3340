#  Spotlight
Help UTRGV students discover campus events, register, and optionally get paired with a buddy to attend together.



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

### Event Management
- **Create Events**:  
- **Event Details**:  
- **Event Editing**:  
- **Event Deletion**: 

### RSVP System
- **RSVP to Events**:  
- **RSVP Tracking**:  
- **Duplicate Prevention**:  
- **RSVP Count**: 

### Pages & Templates
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
