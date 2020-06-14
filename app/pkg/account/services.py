class AuthService:

    @classmethod
    def update_password(cls, user, password):
        user.set_password(password)
        user.save(update_fields=['password'])
