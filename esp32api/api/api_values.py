from flask_restplus import Namespace, Resource
from .utils import BASE_PARSER, SERVER_TIME_MODEL, VALUES_PARSER, VALUES_MODEL
import datetime

NAME = 'values'
URL = '/' + NAME

API = Namespace(NAME, description='Service to update values to server', path='/')

from .. import QUEUES

@API.route(URL)
class ValuesResource(Resource):
    # @API.doc('values', parser=BASE_PARSER)
    @API.expect(VALUES_MODEL)
    def post(self):
        """Update values to server"""
        data = self.api.payload
        print("data:"+str(data))
        name = data['name']
        value = data['value']
        for queue in QUEUES:
            queue.put({"name":name, "value":value})

        return {'status': 'OK'}