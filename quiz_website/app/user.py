from flask_login import UserMixin, AnonymousUserMixin


class UserClass(UserMixin):
    def __init__(self, user_data) -> None:
        self.user_id = user_data['user_id']
        self.username = user_data['username']
        self.password = user_data['password_hash']
        self.admin = user_data['admin']
        self.confirmed = user_data['confirmed']
    
    def get_id(self):
        return self.user_id

    def is_admin(self):
        return self.admin
    

class AnonymousUser(AnonymousUserMixin):
    def __init__(self) -> None:
        self.username = 'Anonymous'
