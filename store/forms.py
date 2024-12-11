from django import forms
from .models import Store, ReportForStore

class StoreUpdateForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'description', 'address', 'contact']


class ReportForStoreForm(forms.ModelForm):
    class Meta:
        model = ReportForStore
        fields = ['report_type']
