import logging

from django import forms

from aremind.apps.groups.models import Group
from aremind.apps.groups.validators import validate_phone

from rapidsms.models import Contact, Backend


__all__ = ('GroupForm', 'ContactForm', 'ForwardingRuleFormset',)


logger = logging.getLogger('aremind.apps.groups.forms')


class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        exclude = ('is_editable',)

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        self.fields['contacts'].help_text = ''
        qs = Contact.objects.filter(patient__isnull=True).order_by('name')
        self.fields['contacts'].queryset = qs
        self.fields['contacts'].widget.attrs['class'] = 'horitzonal-multiselect'


class ContactForm(forms.ModelForm):
    """ Form for managing contacts """

    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.none())
    phone = forms.CharField(validators=[validate_phone], required=True)

    class Meta:
        model = Contact
        exclude = ('language', 'name', 'primary_backend', 'pin')

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance and instance.pk:
            pks = instance.groups.values_list('pk', flat=True)
            kwargs['initial'] = {'groups': list(pks)}
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['groups'].widget = forms.CheckboxSelectMultiple()
        self.fields['groups'].queryset = Group.objects.order_by('name')
        self.fields['groups'].required = False
        for name in ('first_name', 'last_name', 'phone'):
            self.fields[name].required = True

    def save(self, commit=True):
        instance = super(ContactForm, self).save()
        instance.groups = self.cleaned_data['groups']
        return instance
