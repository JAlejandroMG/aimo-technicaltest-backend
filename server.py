from bottle import run, route

@route('/hello')
def hello():
    return "<h1>HelloWorld!</h1>"

run(host='localhost', port=8000)