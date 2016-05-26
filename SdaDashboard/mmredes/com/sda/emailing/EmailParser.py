from bs4 import BeautifulSoup

__author__ = 'macbook'


class EmailParser:
    def __init__(self):
        pass

    @staticmethod
    def get_cell_value(rows, field_label):
        for row in rows:
            cells = row.findAll('td')
            # cell_span = cells[0].findAll('span')
            cell_text = cells[0].find(text=True) if len(cells) > 0 else ''
            # print ("get_cell_value.cell_text: %s" % cell_text)
            if len(cells) == 2 and cell_text == field_label:
                # print ("cell_text: %s" % cell_text)
                cell_value = cells[1].find(text=True) if len(cells) > 0 else ''
                return cell_value
        return '<valueNotFound>'

    @staticmethod
    def get_cell_description_value(rows, field_label):
        for row in rows:
            cells = row.findAll('td')
            # cell_span = cells[0].findAll('span')
            cell_text = cells[0].find(text=True) if len(cells) > 0 else ''
            # print ("get_cell_value.cell_text: %s" % cell_text)
            if len(cells) == 2 and cell_text == field_label:
                # print ("cell_text: %s" % cell_text)
                tag_desc_value = cells[1].findAll('div')
                for tag_div in tag_desc_value:
                    tags_span = tag_div.findAll('span')
                    tag_span_ok = False
                    for tag_span in tags_span:
                        tag_span_text = tag_span.find(text=True)
                        if 'Descripcion del Ticket:' in tag_span_text:
                            tag_span_ok = True
                            break

                    if tag_span_ok:
                        cell_value = tags_span[1].find(text=True) if len(tags_span) > 1 else ''
                        return cell_value
        return '<valueNotFound>'

    @staticmethod
    def get_list_tickets(rows, user_installer, is_req):
        list_ticket = []
        prefix = 'R' if is_req else 'T'
        for row in rows:
            cells = row.findAll('td')
            cell_span = cells[0].findAll('span')
            cell_text = cell_span[0].find(text=True) if len(cell_span) > 0 else None
            if cell_text and cell_text != 'TICKET':
                id_ticket = cell_text
                cell_app_span = cells[3].findAll('span')
                id_app = cell_app_span[0].find(text=True) if len(cell_span) > 0 else None
                find_sda = 'SDA' in id_app
                # print "find SDA in app: %s" % find_sda
                if find_sda:
                    dict_ticket = {'id_ticket': prefix + id_ticket, 'user_installer': user_installer, 'id_status': 2}
                    list_ticket.append(dict_ticket)

        return list_ticket

    def parse_mail_defect(self, html_body):
        soup = BeautifulSoup(html_body, "html.parser")
        tables = soup.findAll('table', attrs={'class': 'textfont'})
        for table in tables:
            is_table_ok = False
            rows = table.findAll('tr')
            for row in rows:
                cells = row.findAll('td')
                cell_field_text = cells[0].find(text=True) if len(cells) > 0 else ''
                # print 'cell_field_text = %s' % cell_field_text
                if cell_field_text == 'Ambiente':
                    is_table_ok = True
                    break

            if is_table_ok:
                dict_defect = {'id_defect': None, 'environment': self.get_cell_value(rows, 'Ambiente'),
                               'crm': self.get_cell_value(rows, 'Mercado'),
                               'description': self.get_cell_description_value(rows, 'Descripcion'),
                               'id_ticket': 'T' + self.get_cell_value(rows, 'Defect ID'),
                               'id_release': self.get_cell_value(rows, 'Release'),
                               'id_requirement': self.get_cell_value(rows, 'Requerimiento'),
                               'user_detect': self.get_cell_value(rows, 'Detectado por'),
                               'id_type_defect': self.get_cell_value(rows, 'Tipo Defecto'),
                               'user_assign': self.get_cell_value(rows, 'Asignado a')}
                # print "table found!!"
                return dict_defect
        return None

    def parse_updating_environment(self, html_body, user_email):
        soup = BeautifulSoup(html_body, "html.parser")
        tables = soup.findAll('table', attrs={'class': 'MsoNormalTable'})
        for table in tables:
            is_table_ok = False
            is_req = False
            rows = table.findAll('tr')
            for row in rows:
                cell_span = row.findAll('span')
                if len(cell_span) > 0:
                    cell_text = cell_span[0].find(text=True)
                    if cell_text == "TICKET" or cell_text == "REQUERIMIENTO":
                        is_table_ok = True
                        is_req = True if cell_text == "REQUERIMIENTO" else False
                        break
            if is_table_ok:
                return self.get_list_tickets(rows, user_email, is_req)
        return None
