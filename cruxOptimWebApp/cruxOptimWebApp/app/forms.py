from django import forms

from django.utils.translation import ugettext_lazy as _



class NutritionOptimizerInputForm(forms.Form):
    units_label = _('Units')

    def __init__(self,
        goals_choices,
        weight_units_choices,
        height_units_choices,
        gender_choices,
        age_units_choices,
        use_demerits,
         *args, **kwargs):

        super(NutritionOptimizerInputForm, self).__init__(*args, **kwargs)

        self.fields['use_demerits'] = forms.BooleanField(
            label=_('Use demerits'),
            initial=use_demerits,
            required=False
        )
        self.fields['use_demerits'].widget.attrs['class'] = 'form-check-input'

        self.fields['age'] = forms.IntegerField(label=_('Age'))
        self.fields['age'].widget.attrs['class'] = 'form-control'
        self.fields['age_unit'] = forms.ChoiceField(
            label=self.units_label,
            choices=age_units_choices
        )
        self.fields['age_unit'].widget.attrs['class'] = 'form-control'

        self.fields['weight_value'] = forms.DecimalField(
            label=_('Weight'),
            min_value=0.0,
            decimal_places=2)
        self.fields['weight_value'].widget.attrs['class'] = 'form-control'

        self.fields['height_value'] = forms.DecimalField(
            label=_('Height'),
            min_value=0.0,
            decimal_places=2)
        self.fields['height_value'].widget.attrs['class'] = 'form-control'

        self.fields['weight_unit'] = forms.ChoiceField(
            label=self.units_label,
            choices=weight_units_choices
        )
        self.fields['weight_unit'].widget.attrs['class'] = 'form-control'

        self.fields['height_unit'] = forms.ChoiceField(
            label=self.units_label,
            choices=height_units_choices)
        self.fields['height_unit'].widget.attrs['class'] = 'form-control'

        self.fields['goal'] = forms.ChoiceField(
            label=_('Goal'),
            choices=goals_choices,
            widget=forms.RadioSelect())
        #self.fields['goal'].widget.attrs['class'] = 'form-control'

        self.fields['gender'] = forms.ChoiceField(
            label=_('Gender'),
            choices=gender_choices)
        self.fields['gender'].widget.attrs['class'] = 'form-control'