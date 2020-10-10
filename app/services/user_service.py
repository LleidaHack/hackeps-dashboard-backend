from app.models.user import User

class UserService():
    def get_all_users(self, db):
        users = db.collection(u'hackeps-2019').document(u'prod').collection(u'users').get()
        return list(map(lambda x: self._to_filtered_dict(x), users))

    def _to_filtered_dict(self, user):
        user = user.to_dict()
        return User.from_dict(user).to_dict()