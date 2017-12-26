import os
from bottle import route, template, redirect, run, error, request, response, static_file, SimpleTemplate

@route('/')
def get_index():
	return template('index',title="yo")
	
@route('/static/css/<filename>')
def css(filename):
	return static_file(filename, root='static/css')

@route('/static/image/<filename>')
def image(filename):
	return static_file(filename, root='static/image')

@route('/static/js/<filename>')
def js(filename):
	return static_file(filename, root='static/js')

@route('/static/json/<filename>')
def json(filename):
	return static_file(filename, root='static/json')
	
if __name__ == '__main__':
	run(host='localhost', port=8080, debug=True)
