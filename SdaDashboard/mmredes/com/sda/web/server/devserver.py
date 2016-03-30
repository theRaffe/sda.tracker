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
        'log.access_file': "access.log",
        'log.error_file': "error.log",
        'log.screen': False,
        'tools.sessions.on': True,
    },

    '/': {
        'tools.db.on': True,
    },
}

if __name__ == "__main__":
    config = ConfigParser.RawConfigParser()
    config.read('board.cfg')
    connection_file = config.get('DatabaseSection', 'database.file')
    SAEnginePlugin(cherrypy.engine, connection_file).subscribe()
    cherrypy.tools.db = SATool()
    cherrypy.config.update(config)
    cherrypy.engine.start()
    cherrypy.quickstart(DashBoardRoot(schema_base), config=config)
