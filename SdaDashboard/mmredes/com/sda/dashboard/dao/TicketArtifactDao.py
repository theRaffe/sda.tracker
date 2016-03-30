import time
from mmredes.com.sda.dashboard.dao.SdaBaseDao import SdaBaseDao

__author__ = 'macbook'


class TicketArtifactDao(SdaBaseDao):
    def get_ticket_artifact(self, id_ticket, id_artifact, type_tech):
        TicketArtifact = self._Base.classes.ticket_artifact
        return self._session.query(TicketArtifact).filter(TicketArtifact.id_ticket == id_ticket,
                                                          TicketArtifact.id_artifact == id_artifact,
                                                          TicketArtifact.id_type_tech == type_tech).one()

    def get_all_ticket_artifact(self, id_ticket):
        TicketArtifact = self._Base.classes.ticket_artifact
        return self._session.query(TicketArtifact).filter(TicketArtifact.id_ticket == id_ticket).all()

    def get_ticket_artifact_code(self, id_ticket):
        TicketArtifact = self._Base.classes.ticket_artifact
        CatTypeTech = self._Base.classes.cat_type_tech
        CatArtifact = self._Base.classes.cat_artifact
        return self._session.query(TicketArtifact, CatTypeTech, CatArtifact).join(CatTypeTech).join(CatArtifact).filter(
            TicketArtifact.id_ticket == id_ticket).all()

    def process_ticket_artifact(self, id_artifact, dict_artifact):
        id_ticket = dict_artifact["id_ticket"]
        id_type_tech = dict_artifact["id_type_tech"]
        date_current = time.time()
        creation_user = dict_artifact["modification_user"]
        id_revision = dict_artifact["id_revision"]
        build_release = dict_artifact["build_release"]
        build_hotfix = dict_artifact["build_hotfix"]

        TicketArtifact = self._Base.classes.ticket_artifact
        rows = self._session.query(TicketArtifact).filter(
            TicketArtifact.id_ticket == id_ticket, TicketArtifact.id_artifact == id_artifact,
            TicketArtifact.id_type_tech == id_type_tech).all()
        print len(rows)
        if len(rows) == 0:
            row = TicketArtifact(id_ticket=id_ticket, id_artifact=id_artifact, id_type_tech=id_type_tech,
                                 creation_user=creation_user, creation_date=date_current, id_revision=id_revision,
                                 build_release=build_release, build_hotfix=build_hotfix,
                                 modification_user=creation_user)
            self._session.add(row)
        else:
            row = rows[0]
            row.modification_user = creation_user
            row.modification_date = date_current
            row.id_revision = id_revision
            row.build_release = build_release
            row.build_hotfix = build_hotfix
