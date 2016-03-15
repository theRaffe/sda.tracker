from mmredes.com.sda.dashboard.dao.SdaBaseDao import SdaBaseDao

__author__ = 'macbook'


class CatArtifactDao(SdaBaseDao):

    # def __init__(self, dict_database):
    #     SdaBaseDao.__init__(self, dict_database)
    #     self._cat_artifacts = dict_database['base'].classes.cat_artifact

    def list_all(self):
        cat_artifacts = self._Base.classes.cat_artifact
        return self._session.query(cat_artifacts).all()

