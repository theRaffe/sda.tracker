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
                # arr_cell_span = cells[1].findAll('span')
                # for cell_span in arr_cell_span:
                #     cell_content = cell_span.find(text=True)
                #     if cell_content is not None:
                #         cell_value = ''.join((cell_value, cell_content.encode('ascii', 'ignore').decode('ascii')))
                return cell_value
        return '<valueNotFound>'

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
                # cell_span = row.findAll('span')
                # if len(cell_span) > 0:
                #     cell_text = cell_span[0].find(text=True)
                #     if cell_text == "Ambiente":
                #         is_table_ok = True
                #         break

            if is_table_ok:
                dict_defect = {'id_defect': None, 'environment': None, 'crm': None, 'description': None}
                # print "table found!!"
                dict_defect['id_ticket'] = 'T' + self.get_cell_value(rows, 'Defect ID')
                dict_defect['environment'] = self.get_cell_value(rows, 'Ambiente')
                dict_defect['crm'] = self.get_cell_value(rows, 'Mercado')
                dict_defect['description'] = self.get_cell_value(rows, 'Descripcion')
                dict_defect['id_release'] = self.get_cell_value(rows, 'Release')
                dict_defect['id_requirement'] = None
                return dict_defect
        return None
