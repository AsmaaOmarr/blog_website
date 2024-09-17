# Flask Starter Project | Flask-Login, Flask-SQLAlchemy, FLASK-WTF, Flask-Injector, and Flask-Bootstrap

A Flask starter project with server-side setup, including:
- **Flask-Login**: For user authentication management.
- **Flask-SQLAlchemy**: For database ORM integration.
- **Flask-WTF**: For form validation on both client and server sides, with CSRF protection.
- **Flask-Injector**: For dependency injection
- **Flask-Bootstrap**: For serving bootstrap features

## Features
- **Role-Based Access Control**:

Admin: Full control over blog posts and user management.
Author: Can manage only their own blog posts.
Reader: Can view all published blog posts and like/dislike them.
- **Authentication**:

Session-based authentication for login and registration.
Role assignment on registration, with Admin-only role modification.
- **Database**:

SQL Database: Managed using SQLAlchemy.

- **Blog Management**:

Create, view, edit, and delete posts based on user roles.
Like/dislike functionality for blog posts.


## Establish the app

- Create a virtual environment with all required dependencies by running those commands

```bash
python -m venv venv
./venv/Scripts/activate
pip install -r requirements.txt
```

- Set the environment variables based on your configuration in the `.env` file
```env
FLASK_DEBUG=True    # Enable hot reload and debug messages
CREATE_DATABASE_IF_NOT_FOUND=True    # Create new database file in case of there is no a database file already
SQLALCHEMY_DATABASE_URI=sqlite:///DATABASE_FILE.db    # The database connection string
SECRET_KEY=    # The secret key used to encrypt the session content
LOGIN_MANAGER_LOGIN_VIEW=auth.login    # The login view based on the defined routes
```

- Run the flask app

```bash
python main.py
```
