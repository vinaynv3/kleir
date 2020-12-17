
"""
class implements client information
"""

from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

class ClientInfo(models.Model):

    # Models attributes (Database columns)
    Client_ID = models.AutoField(primary_key=True)
    Firstname = models.CharField(max_length=200)
    Lastname = models.CharField(max_length=200)
    Contact = models.PositiveBigIntegerField()
    Email = models.EmailField(max_length=200,null=True, blank = True)
    Date_Time = models.DateField(auto_now = True)
    Created_By = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    Slug = models.SlugField(null=False, unique=True)


    #GET client
    def __str__(self):
        return f'{self.Firstname}'


    #Override save button
    def save(self, *args, **kwargs):
        """
        client firstname and lastname is being sluged to reflect in URL route
        """
        self.Slug = slugify(f'{self.Firstname}_{self.Lastname}')
        super().save(*args, **kwargs)



    #get absolute URL
    def get_absolute_url(self):
        """
        After adding new client row in db, Django built-in method redirects to next url namespace.
        """
        return reverse('Ref-Num', kwargs={'slug': self.Slug,'pk':self.Client_ID})


class BankRef(models.Model):

    #Banks choice options
    Bank_types = [('BFL','Bajaj Urban'),
                  ('ABHFL','Aditya Birla'),
                  ('L&T','Larsen Turbo'),
                  ('NA','NA')

    ]


    client_info = models.ForeignKey(ClientInfo, on_delete=models.CASCADE)
    Reference_Number =  models.CharField(max_length=250, unique = True)
    Bank_Type =  models.CharField(max_length=100,choices=Bank_types,default='NA')
    Date = models.DateField(auto_now = True)


    def __str__(self):
        return f'{self.Bank_Type}'

    #get absolute URL
    def get_absolute_url(self):
        """
        After adding client Bank details row in db, Django built-in method redirects to next url namespace.
        """
        client = get_object_or_404(ClientInfo,pk=self.client_info_id)
        return reverse('Detail-Page', kwargs={'slug': client.Slug,'pk':client.Client_ID})

class Documents(models.Model):

    #Loan type choices
    Loan_types = [('LAP','LAP'),
                      ('HL','HL'),
                      ('BT','BT'),
                      ('NA','NA')
        ]

    # Models attributes (Database columns)
    connection = models.OneToOneField(BankRef,on_delete=models.CASCADE)
    SFDC_no =  models.CharField(max_length=200 , blank = True)
    Report_Date = models.DateField(auto_now = True)
    Product_Loan_Type = models.CharField(max_length=50,choices=Loan_types,default='NA')
    Person_met_at_site = models.CharField(max_length=200)
    Name_of_Applicant  =  models.CharField(max_length=200)
    Name_of_Property_Owner_as_per_legal_document = models.CharField(max_length=200)
    Documents_Provided =  models.CharField(max_length=300)


    def __str__(self):
        return f'{self.Product_Loan_Type}'

    def get_absolute_url(self):
        bank = get_object_or_404(BankRef,pk=self.connection_id)
        customer = get_object_or_404(ClientInfo,pk=bank.client_info_id)
        return reverse('doc-address', kwargs={'slug': customer.Slug,'pk':customer.Client_ID,
                                                'bank_type':bank.Bank_Type,'bank_id':bank.id})

class Address(models.Model):

    # Models attributes (Database columns)
    connection = models.OneToOneField(BankRef,on_delete=models.CASCADE)
    Postal_address_of_the_property = models.CharField(max_length=300)
    Legal_address_of_the_property = models.CharField(max_length=200)
    Landmark_nearby = models.CharField(max_length=200)
    Lat_and_Long = models.CharField(max_length=200)
    Distance_from_City_Centre = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.Distance_from_City_Centre}'

    #get absolute URL
    def get_absolute_url(self):
        bank = get_object_or_404(BankRef,pk=self.connection_id)
        customer = get_object_or_404(ClientInfo,pk=bank.client_info_id)
        return reverse('doc-insights', kwargs={'slug': customer.Slug,'pk':customer.Client_ID,
                                                'bank_type':bank.Bank_Type,'bank_id':bank.id})

class Insights(models.Model):

    #Property types
    Property_types = [('Residential','Residential'),
                      ('Commercial','Commercial'),
                      ('Industrial','Industrial'),
                      ('Mixed_Usage','Mixed_Usage')
        ]

    # Holding type status
    Holding = [('Freehold','Freehold'),
                      ('Leasehold','Leasehold')

        ]

    # Models attributes (Database columns)
    connection = models.OneToOneField(BankRef,on_delete=models.CASCADE)
    Property_holding_type  =  models.CharField(max_length=50,choices=Holding)
    Type_of_the_property  =  models.CharField(max_length=50,choices=Property_types)
    Approved_usage = models.CharField(max_length=200, choices=Property_types)
    Actual_usage = models.CharField(max_length=50,choices=Property_types)
    Current_Zoning_as_per_CDP = models.CharField(max_length=50,choices=Property_types)
    Occupancy_details_floorwise = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.Property_holding_type}'

    #get absolute URL
    def get_absolute_url(self):
        bank = get_object_or_404(BankRef,pk=self.connection_id)
        customer = get_object_or_404(ClientInfo,pk=bank.client_info_id)
        return reverse('doc-market-value', kwargs={'slug': customer.Slug,'pk':customer.Client_ID,
                                                'bank_type':bank.Bank_Type,'bank_id':bank.id})

class MarketingValue(models.Model):

    #Bangalore city Jurisdiction/ Local Municipal types
    Jursidi_municipal_bodies = [('BBMP','BBMP'),
                      ('CMC','CMC'),
                      ('GP','GP'),
                      ('BMRDA','BMRDA'),
                      ('NA','NA')
        ]
    # Marketing status
    marketable = [('Low','Low'),
                      ('Medium','Medium'),
                      ('Good','Good')

        ]

    # Models attributes (Database columns)
    connection = models.OneToOneField(BankRef,on_delete=models.CASCADE)
    Address_Matching =  models.BooleanField(blank=True)
    Local_Municipal_body =  models.CharField(max_length=50,choices=Jursidi_municipal_bodies,default='NA')
    Marketability = models.CharField(max_length=50,choices=marketable)
    Boundaries_matching = models.BooleanField(blank=True)
    Property_Identified = models.BooleanField(blank=True)

    def __str__(self):
        return f'{self.Local_Municipal_body}'

    #get absolute URL
    def get_absolute_url(self):
        bank = get_object_or_404(BankRef,pk=self.connection_id)
        customer = get_object_or_404(ClientInfo,pk=bank.client_info_id)
        return reverse('doc-apt-plan', kwargs={'slug': customer.Slug,'pk':customer.Client_ID,
                                                'bank_type':bank.Bank_Type,'bank_id':bank.id})

class Plan(models.Model):

    # Models attributes (Database columns)
    connection = models.OneToOneField(BankRef,on_delete=models.CASCADE)
    Layout_plan_details = models.CharField(max_length=300, blank=True)
    Approving_authority = models.CharField(max_length=300, blank=True)
    Construction_plan_details = models.CharField(max_length=300, blank=True)
    Plan_validity_from = models.CharField(max_length=300, blank=True)
    To_date = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f'{self.Approving_authority}'

    #get absolute URL
    def get_absolute_url(self):
        bank = get_object_or_404(BankRef,pk=self.connection_id)
        customer = get_object_or_404(ClientInfo,pk=bank.client_info_id)
        return reverse('doc-legal-landmarks', kwargs={'slug': customer.Slug,'pk':customer.Client_ID,
                                                'bank_type':bank.Bank_Type,'bank_id':bank.id})

class LegalLandmarks(models.Model):

    # Models attributes (Database columns)
    connection = models.OneToOneField(BankRef,on_delete=models.CASCADE)
    East = models.CharField(max_length=300, blank=True)
    West = models.CharField(max_length=300, blank=True)
    North = models.CharField(max_length=300, blank=True)
    South = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f'{self.id}'

    #get absolute URL
    def get_absolute_url(self):
        bank = get_object_or_404(BankRef,pk=self.connection_id)
        customer = get_object_or_404(ClientInfo,pk=bank.client_info_id)
        return reverse('doc-site-landmarks', kwargs={'slug': customer.Slug,'pk':customer.Client_ID,
                                                'bank_type':bank.Bank_Type,'bank_id':bank.id})

class SiteVisitLandmarks(models.Model):

    # Models attributes (Database columns)
    connection = models.OneToOneField(BankRef,on_delete=models.CASCADE)
    East = models.CharField(max_length=300, blank=True)
    West = models.CharField(max_length=300, blank=True)
    North = models.CharField(max_length=300, blank=True)
    South = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f'{self.id}'

    #get absolute URL
    def get_absolute_url(self):
        bank = get_object_or_404(BankRef,pk=self.connection_id)
        customer = get_object_or_404(ClientInfo,pk=bank.client_info_id)
        return reverse('doc-photo', kwargs={'slug': customer.Slug,'pk':customer.Client_ID,
                                                'bank_type':bank.Bank_Type,'bank_id':bank.id})
