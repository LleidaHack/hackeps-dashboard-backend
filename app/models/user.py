from app.models.status import Status

class User():
    def __init__(self):
        uid = ''
        full_name = ''
        birthday = ''
        allergies = []
        gdpr = True
        terms = True
        status = Status.PERHAPS
        shirt_size = ''
        photo_url = ''

    def to_dict(self):
        user_dict = {
            'uid': self.uid,
            'full_name': self.full_name,
            'birthday': self.birthday,
            'allergies': self.allergies,
            'gdpr': self.gdpr,
            'terms': self.terms,
            'status': self.status,
            'shirt_size': self.shirt_size,
            'photo_url': self.photo_url
        }
        return user_dict

    @staticmethod
    def from_dict(user_dict):
        user = User()
        user.uid = user_dict['uid']
        user.full_name = user_dict['fullName']
        user.birthday = user_dict['birthDate']
        user.allergies = user_dict['food']
        user.gdpr = user_dict['gdpr']
        user.terms = user_dict['terms']
        user.status = Status.get_status_from_string(user_dict['accepted'])
        user.shirt_size = user_dict['shirtSize']
        user.photo_url = user_dict['photoURL']
        return user