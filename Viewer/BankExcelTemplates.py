
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


    def personalDetailsContainer(self):
        cell_points = [(4,3),(4,9),(5,9),(6,9),(6,3),(7,4),(8,3)]
        data = self.clean()
        profile_data = data['BankRef'][0] + data['Documents'][1:4]+data['ClientInfo'][3]+data['Documents'][4:]
