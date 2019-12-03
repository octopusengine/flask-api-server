from flask import Blueprint, render_template
from flask_restplus import Api

API_URL_PREFIX = '/api'

API_BP = Blueprint('api', __name__, url_prefix=API_URL_PREFIX)

API = Api(API_BP, version='2.0', title='RaceMeter APIs',
          description='APIs for Racemeter application')

@API.errorhandler
def default_error_handler(error):
    '''Default error handler'''
    return {'message': str(error)}, getattr(error, 'code', 500)

def register_structure(name, structure):
    return API.model(name, structure)

def register_model(model):
    return register_structure(model.name, model)    

from .api_time import API as time_api
from .api_values import API as values_api

API.add_namespace(time_api)
API.add_namespace(values_api)