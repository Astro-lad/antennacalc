from django import forms

POLARIZATION_CHOICES = [
    ('vertical', 'Vertical'),
    ('horizontal', 'Horizontal'),
]
SPIRAL_POL_CHOICES = [
    ('rhsp', 'Right-Hand Circular'),
    ('lhsp', 'Left-Hand Circular'),
]
FREQUENCY_UNITS = [
    ('hz', 'Hz'),
    ('khz', 'kHz'),
    ('mhz', 'MHz'),
    ('ghz', 'GHz'),
]

class YagiCalculationForm(forms.Form):
    elements = forms.IntegerField(min_value=3)
    frequency = forms.FloatField(label="Frequency (Hz)")
    unit = forms.ChoiceField(choices=FREQUENCY_UNITS)

class DipoleCalculationForm(forms.Form):
    frequency = forms.FloatField(label="Frequency (Hz)")
    unit = forms.ChoiceField(choices=FREQUENCY_UNITS)

class SpiralCalculationForm(forms.Form):
    f_low = forms.FloatField(label="Lowest Frequency (Hz)")
    f_high = forms.FloatField(label="Highest Frequency (Hz)")

    f_low_unit = forms.ChoiceField(choices=FREQUENCY_UNITS)
    f_high_unit = forms.ChoiceField(choices=FREQUENCY_UNITS)
