from rest_framework.response import Response

class ResponseCodes:
    SUCCESS = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
    
class RFResponse(Response):
    def __init__(self, code=200, message='Success', data=None, errors=None, status=None, **kwargs):
        response_data = {
            'code': code,
            'message': message,
            'data': data,
            'errors': errors,
        }
        super().__init__(response_data, status=status, **kwargs)
