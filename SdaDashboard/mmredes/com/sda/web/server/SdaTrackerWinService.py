import ConfigParser
import os
import win32service

import cherrypy
import win32serviceutil

from mmredes.com.sda.web.server.DashBoardRoot import DashBoardRoot
from mmredes.com.sda.web.server.tools import SAEnginePlugin, SATool, schema_base

basedir = os.path.abspath(os.path.dirname(__file__))

config = {
    'DEFAULT': {
        basedir: basedir,
    },

    'global': {
        'server.socket_port': 9091,
        'server.socket_host': "tristana.mmredes.com",

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
    cherrypy.engine.block()


def shutdown_cherrypy_server():
    cherrypy.engine.exit()


class SdaTrackerService(win32serviceutil.ServiceFramework):
    """NT Service."""

    _svc_name_ = "SdaTrackerService"
    _svc_display_name_ = "Windows Service of SdaTracker Web Server"

    def SvcDoRun(self):
        start_cherrypy_server()
        # self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        # win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        shutdown_cherrypy_server()

        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        # very important for use with py2exe
        # otherwise the Service Controller never knows that it is stopped !


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(SdaTrackerService)
