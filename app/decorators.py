from functools import wraps
from flask_login import current_user

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return 'You need to be logged in to access this page'
            if current_user.role not in required_role:
                return'You do not have permission to access this page'
            return f(*args, **kwargs)
        return decorated_function
    return decorator
