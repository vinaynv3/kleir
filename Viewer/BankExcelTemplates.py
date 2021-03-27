import openpyxl

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
        return data


    def personalDetailsContainer(self,xlsx):
        cell_points = [(4,3),(4,9),(5,9),(6,9),(6,3),(7,4),(8,3)]
        data = self.clean()
        #print(data['BankRef'])
        #print(data['Documents'])
        #print(data['ClientInfo'])
        profile_data = [data['BankRef'][1]] + data['Documents'][1:4]+[data['ClientInfo'][3]]+data['Documents'][4:]
        print(profile_data)

        for i in range(len(cell_points)):
            cell = cell_points[i]
            sheet = xlsx.get_sheet_by_name('Valuation format')
            print(sheet.title)
            sheet = sheet.cell(row = cell[0],column = cell[1])
            sheet = profile_data[i]
