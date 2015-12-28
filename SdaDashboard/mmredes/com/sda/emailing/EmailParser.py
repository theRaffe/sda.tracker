from bs4 import BeautifulSoup

__author__ = 'macbook'


class EmailParser:
    def get_cell_value(self, rows, field_label):
        for row in rows:
            cells = row.findAll('td')
            cell_text = cells[0].find(text=True)
            if len(cells) == 2 and cell_text == field_label:
                print ("cell_text: %s" % cell_text)
                cell_value = ''
                arr_cell_span = cells[1].findAll('span')
                for cell_span in arr_cell_span:
                    cell_content = cell_span.find(text=True)
                    if cell_content is not None:
                        cell_value = ''.join((cell_value, cell_content.encode('ascii', 'ignore').decode('ascii')))
                return cell_value
        return None

    def parse_mail_defect(self, html_body):
        soup = BeautifulSoup(html_body, "html.parser")
        tables = soup.findAll('table', attrs={'class': 'MsoNormalTable'})
        for table in tables:
            is_table_ok = False
            rows = table.findAll('tr')
            for row in rows:
                cell_span = row.findAll('span')
                if len(cell_span) > 0:
                    cell_text = cell_span[0].find(text=True)
                    # print "cell_text: %s" % cell_text
                    if cell_text == "Ambiente":
                        is_table_ok = True
                        break

            if is_table_ok:
                dict_defect = {'id_defect': None, 'environment': None, 'crm': None, 'description': None}
                # print "table found!!"
                dict_defect['id_defect'] = self.get_cell_value(rows, 'Defect ID')
                dict_defect['environment'] = self.get_cell_value(rows, 'Ambiente')
                dict_defect['crm'] = self.get_cell_value(rows, 'Mercado')
                dict_defect['description'] = self.get_cell_value(rows, 'Descripcion')
                return dict_defect
        return None
