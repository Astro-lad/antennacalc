from django.shortcuts import get_object_or_404, render
from .models import Antenna
from calculations.forms import YagiCalculationForm, DipoleCalculationForm, SpiralCalculationForm
from calculations.services import design_yagi, design_dipole, design_spiral, generate_dipole_pattern, generate_yagi_pattern, generate_spiral_pattern, generate_spiral_shape, convert_to_hz

def antennas_list(request):
    antennas = Antenna.objects.all()

    return render(
        request,
        'antennas/list.html',
        {'antennas': antennas}
    )

def antenna_detail(request, id):
    antenna = get_object_or_404(Antenna, id=id)

    form = None

    if antenna.type == 'yagi':
        template = "antennas/yagi_detail.html"

        form = YagiCalculationForm(request.POST or None)

        result = None
        pattern_url = None
        shape_url = None

        if request.method == 'POST' and form.is_valid():
            elements = form.cleaned_data['elements']
            frequency = form.cleaned_data['frequency']

            unit = form.cleaned_data['unit']

            frequency_hz = convert_to_hz(frequency, unit)

            result = design_yagi(elements, frequency_hz)

            pattern_url = generate_yagi_pattern(elements, frequency_hz)

    elif antenna.type == "dipole":
        template = "antennas/dipole_detail.html"

        form = DipoleCalculationForm(request.POST or None)
        result = None
        pattern_url = None
        shape_url = None

        if request.method == "POST" and form.is_valid():
            frequency = form.cleaned_data["frequency"]
            unit = form.cleaned_data['unit']
            frequency_hz = convert_to_hz(frequency, unit)
            result = design_dipole(frequency_hz)

            pattern_url = generate_dipole_pattern()

    elif antenna.type == "spiral":
        template = "antennas/spiral_detail.html"

        form = SpiralCalculationForm(request.POST or None)
        result = None
        pattern_url = None
        shape_url = None

        if request.method == "POST" and form.is_valid():
            f_low = form.cleaned_data['f_low']
            f_low_unit = form.cleaned_data['f_low_unit']

            f_high = form.cleaned_data['f_high']
            f_high_unit = form.cleaned_data['f_high_unit']

            f_low_hz = convert_to_hz(f_low, f_low_unit)
            f_high_hz = convert_to_hz(f_high, f_high_unit)

            result = design_spiral(f_low_hz, f_high_hz)
            pattern_url = generate_spiral_pattern(f_low_hz, f_high_hz)

            shape_url = generate_spiral_shape(
                result['inner_radius'],
                result['outer_radius'],
                result['turns']
            )

    else:
        template = "antennas/detail.html"

    return render(
        request,
        template,
        {
            'antenna': antenna,
            'form': form,
            'result': result,
            'pattern_url': pattern_url,
            'shape_url': shape_url,
        }
    )
