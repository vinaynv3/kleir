from django import forms


from django.forms import ModelForm, TextInput
from Technical.models import *


"""
Layout Forms
"""
PLOT_LABELS_FIELD_DICT = {
                        'East_to_west_in_Feet' : '',
                        'North_to_South_in_Feet' : '',
                        'Land_area_or_UDS_in_SFT' : '',
                        'Carpet_area_of_flat_in_SFT' : '',
                        'SBUA_of_Flat_in_SFT' : '',
                    }

class LayoutForm(ModelForm):
    class Meta:
        model = Layout
        exclude = ['connection']


class DocsForm(ModelForm):
    class Meta:
        model = AsPerDocuments
        exclude = ['connection']
        widgets = {
            'East_to_west_in_Feet': TextInput(attrs={'id':'d_num1','class':'docs'}),
            'North_to_South_in_Feet': TextInput(attrs={'id':'d_num2','class':'docs'}),
            'Land_area_or_UDS_in_SFT': TextInput(attrs={'id':'d_total','class':'docs'}),
        }
        labels = PLOT_LABELS_FIELD_DICT


class PlanForm(ModelForm):
    class Meta:
        model = AsPerPlan
        exclude = ['connection']
        widgets = {
            'East_to_west_in_Feet': TextInput(attrs={'id':'p_num1','class':'plan'}),
            'North_to_South_in_Feet': TextInput(attrs={'id':'p_num2','class':'plan'}),
            'Land_area_or_UDS_in_SFT': TextInput(attrs={'id':'p_total','class':'plan'}),
        }
        labels = PLOT_LABELS_FIELD_DICT

class ActualsForm(ModelForm):
    class Meta:
        model = Actuals
        exclude = ['connection']
        widgets = {
            'East_to_west_in_Feet': TextInput(attrs={'id':'a_num1','class':'actual'}),
            'North_to_South_in_Feet': TextInput(attrs={'id':'a_num2','class':'actual'}),
            'Land_area_or_UDS_in_SFT': TextInput(attrs={'id':'a_total','class':'actual'}),
        }
        labels = PLOT_LABELS_FIELD_DICT


"""
Floor Forms
"""

FLOOR_LABELS_FIELD_DICT = {
                        'Basement_Stilt_area' : '',
                        'No_of_floors': '',
                        'GF_area_units' : '',
                        'FF_area_units' : '',
                        'SF_area_units' : '',
                        'TF_area_units' : '',
                        'Total' : '',
                        'FAR_FSI' : '',

                    }

class DeviationsForm(ModelForm):
    class Meta:
        model = Deviations
        exclude = ['connection']
        labels = {
                  'Total_BUA_deviation':'',
                  'Total_SBUA_considered':'',
                  'FAR_FSI_deviation':'',
                 
                  'Total_Bedrooms':'',
        }

class PermissibleBUAForm(ModelForm):
    class Meta:
        model = PermissibleBUA
        exclude = ['connection']
        widgets = {
            'Basement_Stilt_area': TextInput(attrs={'id':'p_stilt','class':'Permissible'}),
            'No_of_floors': TextInput(attrs={'id':'p_floors','class':'Permissible'}),
            'GF_area_units': TextInput(attrs={'id':'p_GF','class':'Permissible'}),
            'FF_area_units': TextInput(attrs={'id':'p_FF','class':'Permissible'}),
            'SF_area_units': TextInput(attrs={'id':'p_SF','class':'Permissible'}),
            'TF_area_units': TextInput(attrs={'id':'p_TF','class':'Permissible'}),
            'Total': TextInput(attrs={'id':'perm_total','class':'Permissible'}),
            'FAR_FSI': TextInput(attrs={'id':'p_FAR_FSI','class':'Permissible'}),
        }
        labels = FLOOR_LABELS_FIELD_DICT


class ActualBUAForm(ModelForm):
    class Meta:
        model = ActualBUA
        exclude = ['connection']
        widgets = {
            'Basement_Stilt_area': TextInput(attrs={'id':'a_stilt','class':'ActualBUA'}),
            'No_of_floors': TextInput(attrs={'id':'a_floors','class':'ActualBUA'}),
            'GF_area_units': TextInput(attrs={'id':'a_GF','class':'ActualBUA'}),
            'FF_area_units': TextInput(attrs={'id':'a_FF','class':'ActualBUA'}),
            'SF_area_units': TextInput(attrs={'id':'a_SF','class':'ActualBUA'}),
            'TF_area_units': TextInput(attrs={'id':'a_TF','class':'ActualBUA'}),
            'Total': TextInput(attrs={'id':'a_total','class':'ActualBUA'}),
            'FAR_FSI': TextInput(attrs={'id':'a_FAR_FSI','class':'ActualBUA'}),
        }
        labels = FLOOR_LABELS_FIELD_DICT


class SanctionedAreaForm(ModelForm):
    class Meta:
        model = SanctionedArea
        exclude = ['connection']
        widgets = {
            'Basement_Stilt_area': TextInput(attrs={'id':'s_stilt','class':'Sanctioned'}),
            'No_of_floors': TextInput(attrs={'id':'s_floors','class':'Sanctioned'}),
            'GF_area_units': TextInput(attrs={'id':'s_GF','class':'Sanctioned'}),
            'FF_area_units': TextInput(attrs={'id':'s_FF','class':'Sanctioned'}),
            'SF_area_units': TextInput(attrs={'id':'s_SF','class':'Sanctioned'}),
            'TF_area_units': TextInput(attrs={'id':'s_TF','class':'Sanctioned'}),
            'Total': TextInput(attrs={'id':'s_total','class':'Sanctioned'}),
            'FAR_FSI': TextInput(attrs={'id':'s_FAR_FSI','class':'Sanctioned'}),
        }
        labels = FLOOR_LABELS_FIELD_DICT

"""
Property Value Forms
"""


PROPERTY_LABELS_FIELD_DICT = {
                        'Land_area' : '',
                        'BUA_SBUA': '',
                        'Interiors' : '',
                        'Car_park' : '',

                    }

class AreaDetailsForm(ModelForm):
    class Meta:
        model = AreaDetails
        exclude = ['connection']
        widgets = {
            'Land_area': TextInput(attrs={'id':'area_land','class':'Area'}),
            'BUA_SBUA': TextInput(attrs={'id':'area_BUA','class':'Area'}),
            'Interiors': TextInput(attrs={'id':'area_interior','class':'Area'}),
            'Car_park': TextInput(attrs={'id':'area_park','class':'Area'}),
        }
        labels = PROPERTY_LABELS_FIELD_DICT


class AreaDetailsForm(ModelForm):
    class Meta:
        model = AreaDetails
        exclude = ['connection']
        widgets = {
            'Land_area': TextInput(attrs={'id':'area_land','class':'items'}),
            'BUA_SBUA': TextInput(attrs={'id':'area_BUA','class':'items'}),
            'Interiors': TextInput(attrs={'id':'area_interior','class':'items'}),
            'Car_park': TextInput(attrs={'id':'area_park','class':'items'}),
        }
        labels = PROPERTY_LABELS_FIELD_DICT


class RateForm(ModelForm):
    class Meta:
        model = Rate
        exclude = ['connection']
        widgets = {
            'Land_area': TextInput(attrs={'id':'Rate_Land','class':'items'}),
            'BUA_SBUA': TextInput(attrs={'id':'Rate_BUA','class':'items'}),
            'Interiors': TextInput(attrs={'id':'Rate_interior','class':'items'}),
            'Car_park': TextInput(attrs={'id':'Rate_park','class':'items'}),
        }
        labels = PROPERTY_LABELS_FIELD_DICT



class TotalValueForm(ModelForm):
    class Meta:
        model = TotalValue
        exclude = ['connection']
        widgets = {
            'Land_area': TextInput(attrs={'id':'total_Land','class':'items'}),
            'BUA_SBUA': TextInput(attrs={'id':'total_BUA','class':'items'}),
            'Interiors': TextInput(attrs={'id':'total_interior','class':'items'}),
            'Car_park': TextInput(attrs={'id':'total_park','class':'items'}),
        }
        labels = PROPERTY_LABELS_FIELD_DICT



class FairMarketValueForm(ModelForm):
    class Meta:
        model = FairMarketValue
        exclude = ['connection']
        widgets = {
            'completion': TextInput(attrs={'id':'completion','class':'items'}),
            'Date': TextInput(attrs={'id':'Date','class':'items'}),
            'Distressed': TextInput(attrs={'id':'Distressed','class':'items'}),
            'GovtValue': TextInput(attrs={'id':'GovtValue','class':'items'}),
        }
        labels = {
                  'completion':'',
                  'Date':'',
                  'Distressed':'',
                  'GovtValue':'',

        }



class PropertyStatusForm(ModelForm):
    class Meta:
        model = PropertyStatus
        exclude = ['connection']
        labels = {
                  'Progress':'',
                  'Recommended':'',
                  'CurrentAge':'',
                  'ResidualAge':'',

        }

"""
Final Notes Form
"""
class FinalForm(ModelForm):
    class Meta:
        model = FinalNotes
        exclude = ['connection']
