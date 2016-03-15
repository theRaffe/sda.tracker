import os, cherrypy
from mmredes.com.sda.web.server.DashBoardRoot import DashBoardRoot
from tools import SAEnginePlugin, SATool, schema_base

basedir = os.path.abspath(os.path.dirname(__file__))

config = {
            'DEFAULT':  {
                            basedir : basedir,
            },

            'global':   {
                            'server.socket_port' : 8000,
                            'server.socket_host' : "127.0.0.1",

                            'tools.encode.on' : True,
                            'tools.encode.encoding' : 'utf-8',

                            'request.show_tracebacks' : True,
            },

            '/':        {
                            'tools.db.on' : True,
            },
}


if __name__ == "__main__":
    SAEnginePlugin(cherrypy.engine, '/Users/macbook/Documents/workspaces/python/sda_tracker_workspace/sda.tracker/db.sda.tracker/sda_tracking.db').subscribe()
    cherrypy.tools.db = SATool()
    cherrypy.config.update(config)
    cherrypy.engine.start()
    cherrypy.quickstart(DashBoardRoot(schema_base), config=config)
