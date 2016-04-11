from mmredes.com.sda.dashboard.dao.SdaBaseDao import SdaBaseDao

__author__ = 'macbook'


class TranslateEnvironmentDao(SdaBaseDao):
    def translate(self, crm, environment):
        base = self._Base
        translateEnvironment = base.classes.translate_environment

        row = self._session.query(translateEnvironment).filter(
            translateEnvironment.crm == crm, translateEnvironment.environment == environment).one()

        id_environment = row.id_environment if row else None

        return id_environment
