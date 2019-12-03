import signal
import logging

class SignalHandler():
	is_going_down = False

	def __init__(self):
		self.old_handler_int = signal.signal(signal.SIGINT, self.signal_int)
		# self.old_handler_quit = signal.signal(signal.SIGQUIT, self.signal_quit)
		self.old_handler_term = signal.signal(signal.SIGTERM, self.signal_term)
		# self.old_handler_hup = signal.signal(signal.SIGHUP, self.signal_hup)

	def signal_int(self, signal, frame):
		logging.debug("Signal handler has received SIGINT")
		self.is_going_down = True
		if (self.old_handler_int):
			self.old_handler_int(signal, frame)

	def signal_quit(self, signal, frame):
		logging.debug("Signal handler has received SIGQUIT")
		self.is_going_down = True
		if (self.old_handler_quit):
			self.old_handler_quit(signal, frame)

	def signal_term(self, signal, frame):
		logging.debug("Signal handler has received SIGTERM")
		self.is_going_down = True
		if (self.old_handler_term):
			self.old_handler_term(signal, frame)

	def signal_hup(self, signal, frame):
		logging.debug("Signal handler has received SIGHUP")
		self.is_going_down = True
		if (self.old_handler_hup):
			self.old_handler_hup(signal, frame)