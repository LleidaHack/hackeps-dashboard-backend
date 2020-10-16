from app.models.user import User

class UserService():

    def __init__(self, db):
        self.firestore = db

    def get_all_users(self):
        users = self.firestore.collection('hackeps-2020').document('prod').collection('users').get()
        return list(map(lambda x: self._to_filtered_dict(x), users))

    def update_user_status(self, user_uid, status):
        user = self.firestore.collection('hackeps-2020').document('prod').collection('users').document(user_uid).update({"accepted": status})
        return user is not None

    def _to_filtered_dict(self, user):
        user = user.to_dict()
        return User.from_dict(user).to_dict()