from django.db import models
from PropertyDocs.models import ClientInfo, BankRef
from django.shortcuts import get_object_or_404
from django.urls import reverse


#Layout  Infrastructure model
class Layout(models.Model):
    # Models attributes (Database columns)
    connection = models.OneToOneField(BankRef,on_delete=models.CASCADE)
    Approach_Road = models.BooleanField(blank=False)
    Sewer_system =  models.BooleanField(blank=False)
    Water_supply = models.BooleanField(blank=False)
    Electricity = models.BooleanField(blank=False)
    Construction_quality = models.BooleanField(blank=False)
    No_of_lifts = models.CharField(max_length=200)

    class Meta:
        db_table = "LayoutInfrastructure"

    def __str__(self):
        return str(self.id)

"""
Abstraction model - Technical Layout
"""
class LayoutCommonInfo(models.Model):
    East_to_west_in_Feet = models.PositiveIntegerField(blank = True, null = True)
    North_to_South_in_Feet = models.PositiveIntegerField(blank = True, null = True)
    Land_area_or_UDS_in_SFT = models.PositiveIntegerField(blank = True, null = True)
    Carpet_area_of_flat_in_SFT = models.PositiveIntegerField(blank = True, null = True)
    SBUA_of_Flat_in_SFT = models.PositiveIntegerField(blank = True, null = True)

    class Meta:
        abstract = True


class AsPerDocuments(LayoutCommonInfo):
    connection = models.OneToOneField(BankRef,on_delete=models.CASCADE)
    class Meta:
        db_table = "PlotAreaDocuments"

    def __str__(self):
        return str(self.id)

class AsPerPlan(LayoutCommonInfo):
    connection = models.OneToOneField(BankRef,on_delete=models.CASCADE)
    class Meta:
        db_table = "PlotAreaPlan"

    def __str__(self):
        return str(self.id)

class Actuals(LayoutCommonInfo):
    connection = models.OneToOneField(BankRef,on_delete=models.CASCADE)
    class Meta:
        db_table = "PlotAreaActuals"

    def __str__(self):
        return str(self.id)


"""
Abstraction model - Technical Floor details
"""
class FloorsCommonInfo(models.Model):

    Basement_Stilt_area = models.PositiveIntegerField(blank = True, null = True)
    No_of_floors = models.PositiveIntegerField(blank = True, null = True)
    GF_area_units = models.PositiveIntegerField(blank = True, null = True)
    FF_area_units = models.PositiveIntegerField(blank = True, null = True)
    SF_area_units = models.PositiveIntegerField(blank = True, null = True)
    TF_area_units = models.PositiveIntegerField(blank = True, null = True)
    Total = models.PositiveIntegerField(blank = True, null = True)
    FAR_FSI = models.DecimalField(blank = True, null = True, max_digits=10, decimal_places=2)

    class Meta:
        abstract = True


class Deviations(models.Model):

    Total_BUA_deviation = models.CharField(max_length=200)
    Total_SBUA_considered = models.CharField(max_length=200)
    FAR_FSI_deviation = models.CharField(max_length=200)
    Risk_of_Demolition  = models.BooleanField(blank=False)
    connection = models.OneToOneField(BankRef,on_delete=models.CASCADE)
    Total_Bedrooms = models.CharField(max_length=200)

    class Meta:
        db_table = "Deviations"

    def __str__(self):
        return str(self.id)


class PermissibleBUA(FloorsCommonInfo):
    connection = models.OneToOneField(BankRef,on_delete=models.CASCADE)
    class Meta:
        db_table = "PermissibleBUA"

    def __str__(self):
        return str(self.id)

class ActualBUA(FloorsCommonInfo):
    connection = models.OneToOneField(BankRef,on_delete=models.CASCADE)
    class Meta:
        db_table = "ActualBUA"

    def __str__(self):
        return str(self.id)

class SanctionedArea(FloorsCommonInfo):
    connection = models.OneToOneField(BankRef,on_delete=models.CASCADE)
    class Meta:
        db_table = "SanctionedArea"

    def __str__(self):
        return str(self.id)



"""
Abstraction model - Property value assesment
"""
class PropertyValueCommonInfo(models.Model):

    Land_area = models.PositiveIntegerField(blank = True, null = True)
    BUA_SBUA = models.PositiveIntegerField(blank = True, null = True)
    Interiors = models.PositiveIntegerField(blank = True, null = True)
    Car_park = models.PositiveIntegerField(blank = True, null = True)

    class Meta:
        abstract = True

class AreaDetails(PropertyValueCommonInfo):
    connection = models.OneToOneField(BankRef,on_delete=models.CASCADE)

    class Meta:
        db_table = "AreaDetails"

    def __str__(self):
        return str(self.id)


class Rate(PropertyValueCommonInfo):
    connection = models.OneToOneField(BankRef,on_delete=models.CASCADE)

    class Meta:
        db_table = "Rate"

    def __str__(self):
        return str(self.id)


class TotalValue(PropertyValueCommonInfo):
    connection = models.OneToOneField(BankRef,on_delete=models.CASCADE)

    class Meta:
        db_table = "TotalValue"

    def __str__(self):
        return str(self.id)


#FairMarketValue model
class FairMarketValue(models.Model):

    completion = models.PositiveIntegerField(blank = True, null = True)
    Date =  models.DecimalField(blank = True, null = True, max_digits=10, decimal_places=2)
    Distressed =  models.DecimalField(blank = True, null = True, max_digits=10, decimal_places=2)
    GovtValue = models.CharField(max_length=200)
    connection = models.OneToOneField(BankRef,on_delete=models.CASCADE)

    class Meta:
        db_table = "FairMarketValue"

    def __str__(self):
        return str(self.id)


#PropertyStatus model
class PropertyStatus(models.Model):
    Progress = models.CharField(max_length=200)
    Recommended = models.CharField(max_length=200)
    CurrentAge = models.CharField(max_length=200)
    ResidualAge = models.CharField(max_length=200)
    connection = models.OneToOneField(BankRef,on_delete=models.CASCADE)

    class Meta:
        db_table = "PropertyStatus"

    def __str__(self):
        return str(self.id)

#FinalPropertyNotes model
class FinalNotes(models.Model):
    ValuationDoneEarlier = models.BooleanField(blank=False,verbose_name=" Validation Done Earlier ?")
    IsNegative = models.BooleanField(blank=False,verbose_name=" Property in bad community ?")
    IsInDemolitionList = models.BooleanField(blank=False, verbose_name=" Property in Demolition list ?")
    Remarks =  models.TextField()
    connection = models.OneToOneField(BankRef,on_delete=models.CASCADE)

    class Meta:
        db_table = "FinalPropertyNotes"

    def __str__(self):
        return str(self.id)
