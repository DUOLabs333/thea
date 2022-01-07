from app import app
import cherrypy
import os

if __name__ == '__main__':
    cherrypy.tree.graft(app, '/')
    cherrypy.config.update({'server.socket_host': '127.0.0.1',
                            'server.socket_port': int(os.getenv('PORT',5000)),
                            'engine.autoreload.on': False,
                            })

if __name__ == '__main__':
    cherrypy.engine.start()