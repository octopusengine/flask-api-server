from flask_restplus import Namespace, Resource
from .utils import BASE_PARSER, SERVER_TIME_MODEL
import datetime

NAME = 'time'
URL = '/' + NAME

API = Namespace(NAME, description='Service to get server time', path='/')

@API.route(URL)
class ServerTimeResource(Resource):
    @API.doc('time', parser=BASE_PARSER)
    @API.marshal_with(SERVER_TIME_MODEL)
    def get(self):
        """Return server time"""
        return {'@time': datetime.datetime.now()}
    

