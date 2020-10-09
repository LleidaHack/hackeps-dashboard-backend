import enum

class Status(enum.Enum):
    YES = 'YES'
    NO = 'NO'
    PERHAPS = 'PERHAPS'

    @staticmethod
    def get_status_from_string(string_type):
        if string_type == 'YES':
            return Status.YES.name
        elif string_type == 'NO':
            return Status.NO.name
        else:
            return Status.PERHAPS.name
