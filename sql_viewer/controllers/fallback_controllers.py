import traceback
from functools import wraps
from flask import render_template

def fallback(handler):
	def decorate(function):
		@wraps(function)
		def decorated(*args, **kwargs):
			try:
				return function(*args, **kwargs)
			except Exception as error:
				return handler(error)
		return decorated
	
	return decorate

def generic_handler(error):
	logs = traceback.format_exc()
	return render_template("_error.html", reason="An error has ocurred, check the logs for more info.", error=error, logs=logs), 500

def query_error_handler(error):
	logs = traceback.format_exc()
	return render_template("_error.html", reason="An error has ocurred, please check back on your query.", error=error, logs=logs), 500
