"""This module is used to provide the form interface"""

from django import forms
from CSharpConWallet.models import Contacts


class AddContactForms(forms.ModelForm):
    """This class extends the ModelForm class"""

    class Meta:
        """This class is used to define the meta data for the form interface"""

        modal = Contacts
        field = "__all__"
