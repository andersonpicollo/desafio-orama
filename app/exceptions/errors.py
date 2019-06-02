import falcon
import json
from collections import OrderedDict

ERR_INVALID_PARAMETER = {
    'status': falcon.HTTP_400,
    'code': 88,
    'title': 'Invalid Parameter'
}

ERR_USER_NOT_EXISTS = {
    'status': falcon.HTTP_404,
    'code': 21,
    'title': 'User Not Exists'
}

ERR_UNKNOWN = {
    'status': falcon.HTTP_500,
    'code': 500,
    'title': 'Unknown Error'
}

ERR_INVALID_MOV = {
    'status': falcon.HTTP_400,
    'code': 88,
    'title': 'Invalid Mov'
}

ERR_INVALID_DATE = {
    'status': falcon.HTTP_400,
    'code': 88,
    'title': 'Invalid Date'
}


class AppError(Exception):

    def __init__(self, error=ERR_UNKNOWN, description=None):
        self.error = error
        self.error['description'] = description

    @property
    def code(self):
        return self.error['code']

    @property
    def title(self):
        return self.error['title']

    @property
    def status(self):
        return self.error['status']

    @property
    def description(self):
        return self.error['description']

    @staticmethod
    def handle(exception, req, resp, error=None):
        resp.status = exception.status
        meta = OrderedDict()
        meta['code'] = exception.code
        meta['message'] = exception.title

        if exception.description:
            meta['description'] = exception.description
        resp.body = json.dumps({'meta': meta})


class InvalidParameterError(AppError):
    def __init__(self, description=None):
        super().__init__(ERR_INVALID_PARAMETER)
        self.error['description'] = description


class DatabaseError(AppError):
    def __init__(self, error, args=None, params=None):
        super().__init__(error)
        obj = OrderedDict()
        obj['details'] = ', '.join(args)
        obj['params'] = str(params)
        self.error['description'] = obj


class ClienteNotExistsError(AppError):
    def __init__(self, description=None):
        super().__init__(ERR_USER_NOT_EXISTS)
        self.error['description'] = description


class InvalidMovError(AppError):
    def __init__(self, description=None):
        super().__init__(ERR_INVALID_MOV)
        self.error['description'] = description


class InvalidDateError(AppError):
    def __init__(self, description=None):
        super().__init__(ERR_INVALID_DATE)
        self.error['description'] = description

