from mmredes.com.sda.dashboard.dao.SdaBaseDao import SdaBaseDao

__author__ = 'macbook'


class TranslateEnvironmentDao(SdaBaseDao):
    def translate(self, dict_defect):
        crm = dict_defect["crm"]
        environment = dict_defect["environment"]

        Base = self._Base
        TranslateEnvironment = Base.classes.translate_environment

        row = self._session.query(TranslateEnvironment).filter(
            TranslateEnvironment.crm == crm and TranslateEnvironment.environment == environment).one

        id_environment = row.id_environment if row else None

        return None
