from bottle import get, run, static_file


@get('/')
def index():
    return static_file('index.html', root=".")


@get('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./static')


run(host='localhost', port=5000)
