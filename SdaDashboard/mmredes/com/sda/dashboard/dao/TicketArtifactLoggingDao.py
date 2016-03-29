from sqlalchemy import func
import time

from mmredes.com.sda.dashboard.dao.SdaBaseDao import SdaBaseDao

__author__ = 'macbook'


class TicketArtifactLoggingDao(SdaBaseDao):
    def add(self, id_artifact, dict_artifact):
        creation_date = time.time()
        creation_user = dict_artifact["modification_user"]
        id_ticket = dict_artifact["id_ticket"]
        id_revision = dict_artifact["id_revision"]
        build_release = dict_artifact["build_release"]
        build_hotfix = dict_artifact["build_hotfix"]

        Base = self._Base
        TicketArtifactLogging = Base.classes.ticket_artifact_logging
        max_row = self._session.query(func.max(TicketArtifactLogging.id_ticket_row).label("max_row")).filter(
            TicketArtifactLogging.id_ticket == id_ticket).one().max_row
        id_ticket_row = max_row + 1 if max_row else 1
        ticket_artifact_logging = TicketArtifactLogging(id_ticket=id_ticket, id_ticket_row=id_ticket_row,
                                                        id_revision=id_revision, build_release=build_release,
                                                        build_hotfix=build_hotfix, creation_user=creation_user,
                                                        id_artifact=id_artifact, creation_date=creation_date)
        self._session.add(ticket_artifact_logging)
