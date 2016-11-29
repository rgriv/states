from django import forms
from .models import Input, STATES, YEARS, DATA, DISPLAY_TYPES, INTERSECT_DATA

class InputForm(forms.ModelForm):

    attrs = {'class ' : 'form−control ',
             'onchange ' : 'this.form.submit() '}
    display_type = forms.ChoiceField(choices = DISPLAY_TYPES, required = True,
                                    widget = forms.Select(attrs = attrs))
    intersect_data = forms.ChoiceField(choices = INTERSECT_DATA, required = True,
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
    class Meta:
        model = Input
        fields = ['display_type', 'start_year', 'end_year', 'intersect_data','state1', 'data1', 'state2', 'data2', 'state3', 'data3', 'state4', 'data4', 'state5', 'data5', 'state6', 'data6', 'state7', 'data7', 'state8', 'data8']
