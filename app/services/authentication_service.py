class AuthenticationService():
    def __init__(self, pb):
        self.auth = pb.auth()

    def login(self, email, password):
        user = self.auth.sign_in_with_email_and_password(email, password)
        return {'token': user['idToken'], 'refresh_token': user['refreshToken']}

    def reset_password(self, email):
        return self.auth.send_password_reset_email(email)

    def refresh_token(self, token):
        return self.auth.refresh(token)