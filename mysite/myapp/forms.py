from django import forms
from .models import Input, STATES, YEARS, DATA, DISPLAY_TYPES

class InputForm(forms.ModelForm):

    attrs = {'class ' : 'form−control ',
             'onchange ' : 'this.form.submit() '}
    display_type = forms.ChoiceField(choices = DISPLAY_TYPES, required = True,
                                    widget = forms.Select(attrs = attrs))
    start_year = forms.ChoiceField(choices = YEARS, required = True,
                                widget = forms.Select(attrs = attrs))
    end_year = forms.ChoiceField(choices = YEARS, required = True,
                                widget = forms.Select(attrs = attrs))
    state1 = forms.ChoiceField(choices=STATES, required=True,
                              widget=forms.Select(attrs = attrs))
    data1 = forms.ChoiceField(choices=DATA, required=True,
                              widget=forms.Select(attrs = attrs))
    state2 = forms.ChoiceField(choices=STATES, required=True,
                              widget=forms.Select(attrs = attrs))
    data2 = forms.ChoiceField(choices=DATA, required=True,
                              widget=forms.Select(attrs = attrs))
    state3 = forms.ChoiceField(choices=STATES, required=True,
                              widget=forms.Select(attrs = attrs))
    data3 = forms.ChoiceField(choices=DATA, required=True,
                              widget=forms.Select(attrs = attrs))
    state4 = forms.ChoiceField(choices=STATES, required=True,
                              widget=forms.Select(attrs = attrs))
    data4 = forms.ChoiceField(choices=DATA, required=True,
                              widget=forms.Select(attrs = attrs))
    state5 = forms.ChoiceField(choices=STATES, required=True,
                              widget=forms.Select(attrs = attrs))
    data5 = forms.ChoiceField(choices=DATA, required=True,
                              widget=forms.Select(attrs = attrs))
    state6 = forms.ChoiceField(choices=STATES, required=True,
                              widget=forms.Select(attrs = attrs))
    data6 = forms.ChoiceField(choices=DATA, required=True,
                                widget=forms.Select(attrs = attrs))
    state7 = forms.ChoiceField(choices=STATES, required=True,
                              widget=forms.Select(attrs = attrs))
    data7 = forms.ChoiceField(choices=DATA, required=True,
                              widget=forms.Select(attrs = attrs))
    state8 = forms.ChoiceField(choices=STATES, required=True,
                              widget=forms.Select(attrs = attrs))
    data8 = forms.ChoiceField(choices=DATA, required=True,
                              widget=forms.Select(attrs = attrs))
    state9 = forms.ChoiceField(choices=STATES, required=True,
                              widget=forms.Select(attrs = attrs))
    data9 = forms.ChoiceField(choices=DATA, required=True,
                              widget=forms.Select(attrs = attrs))
    state10 = forms.ChoiceField(choices=STATES, required=True,
                              widget=forms.Select(attrs = attrs))
    data10 = forms.ChoiceField(choices=DATA, required=True,
                              widget=forms.Select(attrs = attrs))
    #year = forms.ChoiceField(choices=YEARS, required=True,
    #                          widget=forms.Select(attrs = attrs))

    class Meta:
        model = Input
        fields = ['state1', 'data1', 'state2', 'data2', 'state3', 'data3']
