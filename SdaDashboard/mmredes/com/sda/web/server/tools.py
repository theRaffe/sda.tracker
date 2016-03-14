import os
import cherrypy

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import scoped_session, sessionmaker

__author__ = 'macbook'

schema_base = automap_base()

class SAEnginePlugin(cherrypy.process.plugins.SimplePlugin):
    def __init__(self, bus, db_uri):
        """
        The plugin is registered to the CherryPy engine and therefore
        is part of the bus (the engine *is* a bus) registery.

        We use this plugin to create the SA engine. At the same time,
        when the plugin starts we create the tables into the database
        using the mapped class of the global metadata.

        Finally we create a new 'bind' channel that the SA tool
        will use to map a session to the SA engine at request time.
        """
        cherrypy.process.plugins.SimplePlugin.__init__(self, bus)
        self.sa_engine = None
        self.bus.subscribe("bind", self.bind)
        self.db_uri = db_uri

    def start(self):
        db_path = self.db_uri
        #os.path.abspath(os.path.join(os.curdir, self.db_uri))
        self.sa_engine = create_engine('sqlite:///%s' % db_path, echo=True)
        schema_base.prepare(self.sa_engine, reflect=True)
        #Base.metadata.create_all(self.sa_engine)

    def stop(self):
        if self.sa_engine:
            self.sa_engine.dispose()
            self.sa_engine = None

    def bind(self, session):
        session.configure(bind=self.sa_engine)


class SATool(cherrypy.Tool):
    def __init__(self):
        """
        The SA tool is responsible for associating a SA session
        to the SA engine and attaching it to the current request.
        Since we are running in a multithreaded application,
        we use the scoped_session that will create a session
        on a per thread basis so that you don't worry about
        concurrency on the session object itself.

        This tools binds a session to the engine each time
        a requests starts and commits/rollbacks whenever
        the request terminates.
        """
        cherrypy.Tool.__init__(self, 'on_start_resource', self.bind_session, priority=20)

        self.session = scoped_session(sessionmaker(autoflush=True, autocommit=False))

    def _setup(self):
        cherrypy.Tool._setup(self)
        cherrypy.request.hooks.attach('on_end_resource', self.commit_transaction, priority=80)

    def bind_session(self):
        cherrypy.engine.publish('bind', self.session)
        cherrypy.request.db = self.session

    def commit_transaction(self):
        cherrypy.request.db = None
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.remove()