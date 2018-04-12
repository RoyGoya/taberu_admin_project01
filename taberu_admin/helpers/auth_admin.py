from ..models.users_model import AdminUser


def is_admin(user):
    admin_user = AdminUser.query.filter_by(
        user_id=user.id, is_active=True, is_authenticated=True).first()
    if admin_user is None:
        return False
    elif user.id == admin_user.user_id:
        return True
