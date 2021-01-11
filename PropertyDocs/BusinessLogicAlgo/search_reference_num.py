
from PropertyDocs.models import BankRef, ClientInfo
"""
Search Algorithm, which return a bank record of a corresponding customer based user input, here
the input is bank record Reference number
"""

class RefNumSearch:

    __BANKS = ['BFL','ABHFL','L&T']

    def __init__(self,RefNum):

        self.RefNum = RefNum
        self.Year = self.getYear()
        self.Month = self.getMonth()


        self.__MONTH_TOTAL_DAYS = {'january':31,
                              'february': 29 if self.isLeapYear(self.Year) else 28,
                               'march':31,
                               'april':30,
                               'may':31,
                               'june':30,
                               'july':31,
                               'august':31,
                               'september':30,
                               'october':31,
                               'november':30,
                               'december':31,
                                                     }


    # first Reference_Number search operation
    def firstSearchOps(self):

        bank_name = self.RefNum.split('-')[1]

        import datetime

        month = int(list(self.__MONTH_TOTAL_DAYS.keys()).index(self.Month)+ 1)
        final_monthly_day = self.__MONTH_TOTAL_DAYS[self.Month.lower()]
        start_date = datetime.date(int(self.Year),month,1)
        end_date = datetime.date(int(self.Year),month,final_monthly_day)

        #filter bank objects between start date & end date
        bank_objects = BankRef.objects.filter(Date__gte = start_date , Date__lte = end_date)

        bank_objects = bank_objects.filter(Bank_Type = bank_name)
        print(bank_objects)

        found = False
        position = 0

        while position < len(bank_objects) and not found:

            if self.RefNum == bank_objects[position].Reference_Number:
                found = True
                return bank_objects[position]
            else:
                position +=1

        if not found:
            return False

    #collect year value from Reference_Number string
    def getYear(self):
        import re
        regexExp = re.compile(r'(?:19[7-9]\d|2\d{3})')
        extract_year = regexExp.search(self.RefNum)
        return extract_year.group()

    #collect month value from Reference_Number string
    def getMonth(self):
        import re
        regexExp = re.compile(r'[A-Z][a-z]*')
        extract_month = regexExp.search(self.RefNum.split('-')[0])
        return extract_month.group().lower()

    #Leap year program
    def isLeapYear(self,year):
        year = int(year)

        if (year % 4) == 0:
            if (year % 100) == 0:
                if (year % 400) == 0:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False
