from waitress import serve

from autoberth.wsgi import application

if __name__ == '__main__':
    serve(application, port='8003')