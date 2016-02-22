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
