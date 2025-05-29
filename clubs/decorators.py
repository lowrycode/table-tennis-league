from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import redirect_to_login


def club_admin_required(view_func):
    """
    Decorator for views that checks whether the user is authenticated and has a
    related `club_admin` attribute. If the user is not authenticated, they are
    redirected to the login page. If they are authenticated but do not have
    club admin status, a PermissionDenied exception is raised.

    Intended for views restricted to club administrators only.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        if not hasattr(request.user, "club_admin"):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return _wrapped_view
