
class Response:
    def __init__(self, status: int, description: str, body: list):
        self.status = status
        self.description = description
        self.body = body

    def to_dict(self):
        return {
            'status': self.status,
            'description': self.description,
            'body': self.body,
        }

    def __repr__(self):
        return '\n'.join((
            'status: %s' % self.status,
            'description: %s' % self.description,
            'body: %s' % self.body,
        ))
