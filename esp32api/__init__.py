from flask import Flask
from flask_restplus import Resource, Api
import threading

# api = Api()

app = Flask(__name__)
# api.init_app(app)

QUEUES = []


with app.app_context():
	from .api import API_BP
	app.register_blueprint(API_BP)

from .values_views import process_values_logs
from .signal_handler import SignalHandler

EXIT_HANDLER = SignalHandler()

rfid_inventory = threading.Thread(name="rfid_inventory", target=process_values_logs, args=(QUEUES, EXIT_HANDLER, ))
rfid_inventory.start()	


# @api.route('/hello')
# class HelloWorld(Resource):
#     def get(self):
#         return {'hello': 'world'}

# if __name__ == '__main__':
#     app.run(debug=True, port= 81)