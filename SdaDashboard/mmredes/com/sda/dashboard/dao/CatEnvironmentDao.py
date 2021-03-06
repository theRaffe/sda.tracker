from mmredes.com.sda.dashboard.dao.SdaBaseDao import SdaBaseDao

__author__ = 'macbook'


class CatEnvironmentDao(SdaBaseDao):
    def update_list_tracker(self, code_env, id_list_tracker):
        Base = self._Base
        CatEnvironment = Base.classes.cat_environment
        row = self._session.query(CatEnvironment).filter(CatEnvironment.code_env == code_env).one
        row.id_list_tracker = id_list_tracker

    def get_id_environment(self, crm, code_environment):
        search_code = '%s.%s' % (crm, code_environment)
        CatEnvironment = self._Base.classes.cat_environment
        row = self._session.query(CatEnvironment).filter(CatEnvironment.code_environment == search_code).one()

        if row:
            return row.id_environment

        return None




