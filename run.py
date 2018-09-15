from app import APP
from gevent.pywsgi import WSGIServer

if __name__ == '__main__':
    http_server = WSGIServer(('localhost', 8000), APP)
    http_server.serve_forever()
    app.run(host='localhost', port=8000, use_reloader=True)
