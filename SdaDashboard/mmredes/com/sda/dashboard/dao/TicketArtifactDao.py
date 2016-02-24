import time
from mmredes.com.sda.dashboard.dao.SdaBaseDao import SdaBaseDao

__author__ = 'macbook'


class TicketArtifactDao(SdaBaseDao):
    def get_ticket_artifact(self, id_ticket, id_status=1):
        TicketArtifact = self._Base.classes.ticket_artifact
        return self._session.query(TicketArtifact).filter(TicketArtifact.id_ticket == id_ticket,
                                                          TicketArtifact.id_status == id_status)

    def get_ticket_artifact(self, id_ticket):
        TicketArtifact = self._Base.classes.ticket_artifact
        CatTypeTech = self._Base.classes.cat_type_tech
        CatArtifact = self._Base.classes.cat_artifact
        return self._session.query(TicketArtifact, CatTypeTech, CatArtifact).join(CatTypeTech).join(CatArtifact).filter(
            TicketArtifact.id_ticket == id_ticket).all()

    def process_ticket_artifact(self, id_ticket, dict_artifact):
        id_artifact = dict_artifact["id_artifact"]
        id_type_tech = dict_artifact["id_type_tech"]
        date_current = time.time()
        creation_user = dict_artifact["email"]

        TicketArtifact = self._Base.classes.ticket_artifact
        row = self._session.query(TicketArtifact).filter(
            TicketArtifact.id_ticket == id_ticket and TicketArtifact.id_artifact == id_artifact and TicketArtifact.id_type_tech == id_type_tech).one
        if not row:
            row = TicketArtifact(id_ticket=id_ticket, id_artifact=id_artifact, id_type_tech=id_type_tech,
                                 creation_user=creation_user, creation_date=date_current,
                                 modification_user=creation_user)
            self._session.add(row)
        else:
            row.modification_user = creation_user
            row.modification_date = date_current
