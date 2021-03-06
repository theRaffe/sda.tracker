import ConfigParser
import os, cherrypy
from mmredes.com.sda.web.server.DashBoardRoot import DashBoardRoot
from tools import SAEnginePlugin, SATool, schema_base

basedir = os.path.abspath(os.path.dirname(__file__))

config = {
    'DEFAULT': {
        basedir: basedir,
    },

    'global': {
        'server.socket_port': 8000,
        'server.socket_host': "127.0.0.1",

        'tools.encode.on': True,
        'tools.encode.encoding': 'utf-8',

        'request.show_tracebacks': True,
        'log.access_file': "C:/SdaTracker/webserver/access_sda_tracker_web.log",
        'log.error_file': "C:/SdaTracker/webserver/error_sda_tracker_web.log",
        'log.screen': False,
        'tools.sessions.on': True,
    },

    '/': {
        'tools.db.on': True,
    },
}


def start_cherrypy_server():
    config_parser = ConfigParser.RawConfigParser()
    config_parser.read('C:/SdaTracker/webserver/board.cfg')
    connection_file = config_parser.get('DatabaseSection', 'database.file')
    # print "sqlite file: %s" % connection_file
    SAEnginePlugin(cherrypy.engine, connection_file).subscribe()
    cherrypy.tools.db = SATool()
    cherrypy.config.update(config)
    cherrypy.engine.start()
    cherrypy.quickstart(DashBoardRoot(schema_base), config=config)
    # cherrypy.engine.block()


def shutdown_cherrypy_server():
    cherrypy.engine.exit()


if __name__ == "__main__":
    start_cherrypy_server()
