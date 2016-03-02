from mmredes.com.sda.dashboard.dao.SdaBaseDao import SdaBaseDao

__author__ = 'macbook'

class CatBranchDao(SdaBaseDao):

    def get_environment(self, id_branch):
        CatBranchGit = self._Base.classes.cat_branch_git
        rows = self._session.query(CatBranchGit).filter(CatBranchGit.id_branch == id_branch).all()
        if len(rows) > 0:
            row = rows[0]
            return row.id_environment_def
        return None