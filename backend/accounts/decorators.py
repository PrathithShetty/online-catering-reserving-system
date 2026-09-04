from django.contrib.auth.decorators import user_passes_test


def admin_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.is_catering_admin, login_url='accounts:login')(view_func)
