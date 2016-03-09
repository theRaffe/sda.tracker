import cherrypy

from tools import *
__author__ = 'macbook'

class Root(object):

    _dict_database = {}

    def index(self):
        """
        List users from the DB & add new if no users
        """
        user = cherrypy.request.db.query(User).filter_by(firstname='John').first()
        if user is None:
            user = User('John', 'Doe')
            cherrypy.request.db.add(user)
            return 'Created user: %s %s' % (user.firstname, user.lastname)
        return 'Found user: %s %s' % (user.firstname, user.lastname)
    index.exposed = True


    def get_dict_database(self):
        Base.prepare(cherrypy.engine, reflect=True)
        self._dict_database["engine"] = cherrypy.engine
        self._dict_database["base"] = Base
        self._dict_database["session"] = cherrypy.request.db