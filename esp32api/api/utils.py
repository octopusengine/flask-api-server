from flask import session
from flask_restplus import Model, fields, reqparse
from ..api import register_model

PUT_RESPONSES = {
    400: 'Validation Error / Bad request',
    401: 'Authentication failure',
    404: 'Entity not found'
}

POST_RESPONSES = {
    400: 'Validation error',
    401: 'Authentication failure',
    404: 'Entity does not exist'
}

DELETE_RESPONSES = {
    404: 'Entity not found'
}

# Base Api Model for a paginated response
PAGINATED_MODEL = Model('PaginatedModel', {
    '@nextpage': fields.Boolean,
    '@count': fields.Integer,
})

VALUES_MODEL = Model('ValuesModel', {
    'name': fields.String(required=True, example='temp', title="Name"),
    'value': fields.Float(required=True, example=1.22, title='Value')
})
register_model(VALUES_MODEL)

METADATA_MODEL = Model('MetadataModel', {
    'name': fields.String,
    'type': fields.String,
    'primary_key': fields.Boolean,
    'unique': fields.Boolean,
    'nullable': fields.Boolean,
    'default': fields.String,
    'caption': fields.String
})
register_model(METADATA_MODEL)

COUNT_MODEL = Model('CountModel', {
    '@count': fields.Integer,
})
register_model(COUNT_MODEL)

SERVER_TIME_MODEL = Model('ServerTimeModel', {
    '@server_time': fields.DateTime,
})
register_model(SERVER_TIME_MODEL)

TABLE_REQUEST_COLUMN_MODEL = Model('TableRequestColumnModel', {
    'data': fields.String(required=True),
    'name': fields.String(required=True),
    'orderable': fields.Boolean(required=True),
    'searchable': fields.Boolean(required=True),
    # 'search': fields.String(required=True)
})
register_model(TABLE_REQUEST_COLUMN_MODEL)

TABLE_REQUEST_ORDER_MODEL = Model('TableRequestOrderModel', {
    'column': fields.Integer(required=True),
    'dir': fields.String(required=True)
})
register_model(TABLE_REQUEST_ORDER_MODEL)

TABLE_REQUEST_SEARCH_MODEL = Model('TableRequestSearchModel', {
    # 'regex': fields.Boolean(required=True),
    'value': fields.String(required=True)
})
register_model(TABLE_REQUEST_SEARCH_MODEL)

TABLE_REQUEST_MODEL = Model('TableRequestModel', {
    'draw': fields.Integer(required=True, example=1, title='Internal number'),
    'start': fields.Integer(required=True, example=0, title='Start position for request'),
    'length': fields.Integer(required=True, example=10, title='How many rows are returned'),
    'columns': fields.List(fields.Nested(TABLE_REQUEST_COLUMN_MODEL), required=True, title='Required columns structure'),
    'search': fields.Nested(TABLE_REQUEST_SEARCH_MODEL, required=True),
    'order': fields.List(fields.Nested(TABLE_REQUEST_ORDER_MODEL),required=True, title='Required order')
})
register_model(TABLE_REQUEST_MODEL)

# MAILER_MODEL = Model('MailerModel', {
#     'subject': fields.String(required=True, example='Subjekt', title='Internal number'),
#     'start': fields.Integer(required=True, example=0, title='Start position for request'),
#     'length': fields.Integer(required=True, example=10, title='How many rows are returned'),
#     'columns': fields.List(fields.Nested(TABLE_REQUEST_COLUMN_MODEL), required=True, title='Required columns structure'),
#     'search': fields.Nested(TABLE_REQUEST_SEARCH_MODEL, required=True),
#     'order': fields.List(fields.Nested(TABLE_REQUEST_ORDER_MODEL),required=True, title='Required order')
# })
# EMAILER_PARSER.add_argument('subject', type=str, required=True, default='', help='Subject of email', location='args')
# EMAILER_PARSER.add_argument('to', type=str, required=True, default='', help='Addresses for email', location='args')
# EMAILER_PARSER.add_argument('cc', type=str, required=False, default='', help='Copy addresses for email', location='args')
# EMAILER_PARSER.add_argument('bcc', type=str, required=False, default='', help='BCC addresses for email', location='args')
# EMAILER_PARSER.add_argument('body', type=str, required=False, default='', help='Body of email', location='args')
# register_model(MAILER_MODEL)

IDS = Model('Ids', {
    'ids': fields.List(fields.String(required=True))
})
register_model(IDS)

TABLE_DATA_MODEL = Model('TableDataModel', {
    'draw': fields.Integer(required=True, example=1, title='Internal number'),
    'recordsTotal': fields.Integer(required=True, title='total count of records'),
    'recordsFiltered': fields.Integer(required=True, title='total count of filtered records'), 
    'data': fields.List(fields.Raw)
})
register_model(TABLE_DATA_MODEL)

ROLL_DATA_PAGINATION_MODEL = Model('RollDataPaginationModel', {
    'more': fields.Boolean(example=False, title='If there are more data')
})
register_model(ROLL_DATA_PAGINATION_MODEL)

ROLL_DATA_INNER_MODEL = Model('RollDataInnerModel', {
    'id': fields.Integer(required=True, example=1, title='Internal id of item'),
    'text': fields.String(required=True, example='race 1'),
    'subtitle': fields.String()
})
register_model(ROLL_DATA_INNER_MODEL)

ROLL_DATA_MODEL = Model('RollDataModel', {
    'results': fields.List(fields.Nested(ROLL_DATA_INNER_MODEL), title='Data'),
    'pagination': fields.Nested(ROLL_DATA_PAGINATION_MODEL, required=True)
})
register_model(ROLL_DATA_MODEL)

DEFAULT_PAGE_START = 0
DEFAULT_PAGE_COUNT = 10
DEFAULT_PAGE_ORDER = ''

BASE_PARSER = reqparse.RequestParser()
BASE_PARSER.add_argument('locale', type=str, required=False, default='', help='locale - if not set actual is used')

VALUES_PARSER = reqparse.RequestParser()
VALUES_PARSER.add_argument('name', type=str, required=True, location='json')
VALUES_PARSER.add_argument('value', type=float, required=True, location='json')


DEFAULT_SCANNED_TIME = 0.4

RFID_PARSER = BASE_PARSER.copy()
RFID_PARSER.add_argument('scan_time', type=float, required=False, default=DEFAULT_SCANNED_TIME, help='scanned time')

PAGINATED_PARSER = BASE_PARSER.copy()
PAGINATED_PARSER.add_argument('start', type=int, required=False, default=DEFAULT_PAGE_START, help='start')
PAGINATED_PARSER.add_argument('count', type=int, required=False, default=DEFAULT_PAGE_COUNT, help='max records returned')
PAGINATED_PARSER.add_argument('order', type=str, required=False, default=DEFAULT_PAGE_ORDER, help='order')

ROLL_PARSER = reqparse.RequestParser()
ROLL_PARSER.add_argument('page', type=int, required=False, default=1, help='The page - starting with 1', location='args')
ROLL_PARSER.add_argument('search', type=str, required=False, default='', help='The query for searching', location='args')

EMAILER_PARSER = reqparse.RequestParser()
EMAILER_PARSER.add_argument('subject', type=str, required=True, default='', help='Subject of email')
EMAILER_PARSER.add_argument('to', type=str, required=True, default='', help='Addresses for email')
EMAILER_PARSER.add_argument('cc', type=str, required=False, default='', help='Copy addresses for email')
EMAILER_PARSER.add_argument('bcc', type=str, required=False, default='', help='BCC addresses for email')
EMAILER_PARSER.add_argument('body', type=str, required=False, default='', help='Body of email')

# TABLEDATA_PARSER = BASE_PARSER.copy()
# TABLEDATA_PARSER.add_argument('args', type=dict, required=True, location='form', help='request from table')

TABLEDATA_PARSER = reqparse.RequestParser()
TABLEDATA_PARSER.add_argument('draw', type=int, required=True, location='json')
TABLEDATA_PARSER.add_argument('start', type=int, default=0, required=True, location='json')
TABLEDATA_PARSER.add_argument('length', type=int, default=10, required=True, location='json')
TABLEDATA_PARSER.add_argument('columns', type=str, required=True, location='json')
TABLEDATA_PARSER.add_argument('search', type=str, required=True, location='json')
TABLEDATA_PARSER.add_argument('order', type=str, required=True, location='json')



# {"draw":1,
# "columns":[
#     {"data":"name","name":"name","searchable":true,"orderable":true,"search":{"value":"","regex":false}},
#     {"data":"description","name":"description","searchable":true,"orderable":true,"search":{"value":"","regex":false}},
#     {"data":"start_time","name":"start_time","searchable":true,"orderable":true,"search":{"value":"","regex":false}},
#     {"data":"id","name":"id","searchable":true,"orderable":true,"search":{"value":"","regex":false}}
#     ],
# "order":[{"column":0,"dir":"asc"}],
# "start":0,
# "length":10,
# "search":{"value":"","regex":false}
# }

# Base class for Paginated Resource
class PaginatedResourceBase():
    """
    Paginated Resource Helper class
    This includes basic properties used in the class
    """
    parser = reqparse.RequestParser()
    parser.add_argument('start', type=int, required=False, default=DEFAULT_PAGE_START, help='start')
    parser.add_argument('count', type=int, required=False, default=DEFAULT_PAGE_COUNT, help='max records returned')
    parser.add_argument('order', type=str, required=False, default=DEFAULT_PAGE_ORDER, help='order')