from mmredes.com.sda.dashboard.dao.SdaBaseDao import SdaBaseDao
from sqlalchemy import func

__author__ = 'macbook'


class CatArtifactDao(SdaBaseDao):
    # def __init__(self, dict_database):
    #     SdaBaseDao.__init__(self, dict_database)
    #     self._cat_artifacts = dict_database['base'].classes.cat_artifact

    def list_all(self):
        cat_artifacts = self._Base.classes.cat_artifact
        return self._session.query(cat_artifacts).all()

    def get_id_artifact(self, code_artifact):
        CatArtifact = self._Base.classes.cat_artifact
        rows = self._session.query(CatArtifact).filter(CatArtifact.code_artifact == code_artifact).all()
        if len(rows) > 0:
            row = rows[0]
            return row.id_artifact

        max_row = self._session.query(func.max(CatArtifact.id_artifact).label("max_row")).one().max_row
        id_ticket_row = max_row + 1 if max_row else 1
        new = CatArtifact(id_artifact=id_ticket_row, code_artifact=code_artifact, path_directory=code_artifact,
                          description=code_artifact)
        self._session.add(new)

        return new.id_artifact
