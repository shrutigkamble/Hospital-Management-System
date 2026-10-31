from functools import wraps

from flask import abort
from flask_login import current_user, login_required


def role_required(*allowed_roles):

    def decorator(function):

        @wraps(function)
        @login_required
        def wrapper(*args, **kwargs):

            if current_user.role not in allowed_roles:

                abort(403)

            return function(*args, **kwargs)

        return wrapper

    return decorator