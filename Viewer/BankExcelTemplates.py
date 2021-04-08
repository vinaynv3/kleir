import openpyxl
import pandas as pd
"""
Data representation & Manipulation classes
"""

class BFL_Urban:

    def __init__(self,data = None):
        self.data = data

    def clean(self):

        data = {}
        for obj in self.data:
            data[str(obj.__class__).split(".")[-1].split("'")[0]] = []

            for k,v in obj.__dict__.items():
                if (not k.startswith("_")) and k != "id" and k != "connection_id":
                        data[str(obj.__class__).split(".")[-1].split("'")[0]].append(v)
        #Structure data into tabular form
        df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in data.items() ]))

        return df

    def create_xlsx(self):
        wb = openpyxl.Workbook()
        s = wb['Sheet']
        s.title = 'HEY'
        wb.save('HEY.xlsx')
        wb.close()
        """
        with open('FileOperations/test.xlsx','wb') as excel:
            load_xlsx = openpyxl.load_workbook(excel)
            sheet = load_xlsx.active
            sheet.title = "Valuation Report"
            load_xlsx.save(excel)
        """
    def personalDetailsContainer(self):

        """
        Excel cell points data structuring
        """

        df = self.clean()
        value_cell_points = ['B3','I3','C4','I4','C5','I5','D6','C7']
        #value_cell_points = [(3,2),(3,9)(4,3),(4,9),(5,3),(5,9),(6,4),(7,3)]
        data_tuple = (df['Documents'][0],df['Documents'][1],
                    df['Documents'][2],df['Documents'][3],
                    df['Documents'][4],df['ClientInfo'][3],
                    df['Documents'][5],df['ClientInfo'][6]) # data is relative to value_cell_points position
        columns_cell_points = { 'Valuation Report':(1,1),
                    'Bajaj Housing Finance limited':(2,1),
                    'SFDC no':(3,1), 'Report date':(3,5),
                    'Product Loan Type':(4,1),'Person met at site':(4,5),
                    'Name of Applicant':(5,1),'Contact no':(5,7),
                    'Name of Property Owner as per legal document':(6,1),
                    'Documents provided':(7,1)


        }

        load_xlsx = openpyxl.load_workbook('HEY.xlsx')
        sheet = load_xlsx.active
        for i in range(len(value_cell_points)):
            sheet[value_cell_points[i]] = data_tuple[i]
        load_xlsx.save('HEY.xlsx')
        load_xlsx.close()
