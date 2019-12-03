from threading import RLock
import queue
import datetime
import time
import logging
from flask import render_template, abort, Response
from . import app

subscriptions = []
lock = RLock()

def is_any_subscription():
	with lock:
		return (len(subscriptions)>0) 

def process_values_logs(queues, exit_handler):
	logs_queue = queue.Queue()
	queues.append(logs_queue)
	items = []
	try:
		while True:
			if exit_handler.is_going_down:
				break
			empty = False
			try:
				item = logs_queue.get(block=True, timeout=0.1)
				if (item != None):
					if is_any_subscription():
						items.append(item)
			except queue.Empty as e:
				# logging.debug('Empty result handling')
				empty = True
			if ((len(items)>9) or (empty and len(items) > 0)):
				if is_any_subscription():
					with app.app_context():
						internal_process_values(items)
						items = []
			if (empty):
				time.sleep(.1)
	finally:
		logging.debug("finalizing process_inventory_logs")

@app.route('/values', methods=['GET'])
def page_values():
	return render_template('page_values.html')

from flask import json

class ServerSentEvent(object):
	def __init__(self, data):
		self.data = json.dumps({'data':data})

	def encode(self):
		if not self.data:
			return ""
		return "data: "+self.data+"\n\n"

import copy

def internal_process_values(items):
	# Tady bude zaproceseni mnoziny logu do inventury
	# Struktura jenoho itemu je (tagId, antennaId, frequency, rssi, time, inventory_number)
	if (items):
		with lock:
			event_data = []
			for item in items:
				event_data.append(item)
			if (event_data):	
				ev = ServerSentEvent(event_data)
				for queue in subscriptions:
					queue.put(ev)

def register_subscription():
	q = queue.Queue()
	lock.acquire()
	try:
		subscriptions.append(q)
	finally:
		lock.release()
	return q

def unregister_subscription(queue):
	with lock:
		subscriptions.remove(queue)

@app.route("/values/subscribe")
def subscribe_page_chips_inventory():
	def gen():
		q = register_subscription()
		try:
			while True:
				ev = q.get()
				yield ev.encode()
		except GeneratorExit: # Or maybe use flask signals
			unregister_subscription(q)
	return Response(gen(), mimetype="text/event-stream")