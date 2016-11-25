from django import forms
from .models import Input, STATES, YEARS, DATA

class InputForm(forms.ModelForm):

    attrs = {'class ' : 'form−control ',
             'onchange ' : 'this.form.submit() '}

    state1 = forms.ChoiceField(choices=STATES, required=True,
                              widget=forms.Select(attrs = attrs))
    state2 = forms.ChoiceField(choices=STATES, required=True,
                              widget=forms.Select(attrs = attrs))
    state3 = forms.ChoiceField(choices=STATES, required=True,
                              widget=forms.Select(attrs = attrs))
    data1 = forms.ChoiceField(choices=DATA, required=True,
                              widget=forms.Select(attrs = attrs))
    data2 = forms.ChoiceField(choices=DATA, required=True,
                              widget=forms.Select(attrs = attrs))
    data3 = forms.ChoiceField(choices=DATA, required=True,
                              widget=forms.Select(attrs = attrs))
    #year = forms.ChoiceField(choices=YEARS, required=True,
    #                          widget=forms.Select(attrs = attrs))

    class Meta:
        model = Input
        fields = ['state1', 'state2', 'state3', 'data1', 'data2', 'data3']
