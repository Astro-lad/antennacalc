import numpy as np
import matplotlib.pyplot as plt
import os
from django.conf import settings
import math 
import uuid

c = 300_000_000

def design_yagi(elements, frequency):

    wavelength = c / frequency

    if elements < 3:
        return None

    reflector_length = 0.55 * wavelength
    driven_length = 0.48 * wavelength

    directors = []
    for i in range(elements - 2):
        length = (0.42 - i * 0.005) * wavelength
        directors.append(round(length, 4))

    reflector_spacing = 0.2 * wavelength
    director_spacing = 0.15 * wavelength

    gain = 6 + (2 * math.log10(elements))

    return {
        "wavelength": round(wavelength, 4),
        "reflector_length": round(reflector_length, 4),
        "driven_length": round(driven_length, 4),
        "directors": directors,
        "reflector_spacing": round(reflector_spacing, 4),
        "director_spacing": round(director_spacing, 4),
        "gain": round(gain, 2),
    }

def design_dipole(frequency):

    if frequency <= 0:
        return None

    wavelength = c / frequency

    total_length = 0.95 * (wavelength / 2)

    arm_length = total_length / 2

    gain = 2.15
    radiation_resistance = 73

    return {
        "wavelength": round(wavelength, 4),
        "total_length": round(total_length, 4),
        "arm_length": round(arm_length, 4),
        "gain": gain,
        "radiation_resistance": radiation_resistance,
    }

def design_spiral(f_low, f_high):

    if f_low <= 0 or f_high <= 0 or f_low >= f_high:
        return None

    lambda_low = c / f_low
    lambda_high = c / f_high

    r_outer = lambda_low / (2 * math.pi)
    r_inner = lambda_high / (2 * math.pi)

    spacing = 0.02 * lambda_low

    turns = (r_outer - r_inner) / spacing

    gain = 8

    return {
        "lambda_low": round(lambda_low, 4),
        "lambda_high": round(lambda_high, 4),
        "outer_radius": round(r_outer, 4),
        "inner_radius": round(r_inner, 4),
        "spacing": round(spacing, 4),
        "turns": round(turns, 2),
        "gain": gain,
    }

def generate_dipole_pattern():
    theta = np.linspace(0, 2 * np.pi, 360)
    r = np.abs(np.sin(theta))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='polar')
    ax.plot(theta, r)
    ax.set_title("Dipole Radiation Pattern")

    image_path = os.path.join(settings.MEDIA_ROOT, 'dipole_pattern.png')
    plt.savefig(image_path)
    plt.close()

    return settings.MEDIA_URL + 'dipole_pattern.png'

def generate_yagi_pattern(elements, frequency):
    theta = np.linspace(0, 2 * np.pi, 720)
    wavelength = c / frequency

    d = 0.15 * wavelength
    k = 2 * np.pi / wavelength
    beta = -k * d
    psi = k * d * np.cos(theta) + beta

    denominator = np.sin(psi / 2)
    denominator = np.where(np.abs(denominator) < 1e-6, 1e-6, denominator)

    af = np.abs(np.sin(elements * psi / 2) / denominator)
    af = af / np.max(af)
    element_pattern = np.abs(np.sin(theta))
    total_pattern = af * element_pattern
    total_pattern = total_pattern / np.max(total_pattern)

    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111, projection='polar')

    ax.plot(theta, total_pattern)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_title(f"Yagi Radiation Pattern ({elements} elements)")

    filename = f'yagi_pattern_{elements}.png'
    image_path = os.path.join(settings.MEDIA_ROOT, filename)

    plt.savefig(image_path)
    plt.close(fig)

    return settings.MEDIA_URL + filename

def generate_spiral_pattern(f_low, f_high):
    theta = np.linspace(0, 2 * np.pi, 720)

    # Bandwidth ratio
    bandwidth_ratio = f_high / f_low

    # Map ratio to beam shape (tunable)
    n = 1 + np.log10(bandwidth_ratio + 1)

    # Pattern
    r = np.abs(np.cos(theta)) ** n

    # Normalize
    r = r / np.max(r)

    # Plot
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111, projection='polar')

    ax.plot(theta, r)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)

    ax.set_title(f"Spiral Pattern (BW ratio: {round(bandwidth_ratio,2)})")

    # Save
    filename = "spiral_pattern.png"
    image_path = os.path.join(settings.MEDIA_ROOT, filename)

    plt.savefig(image_path)
    plt.close(fig)

    return settings.MEDIA_URL + filename

def generate_spiral_shape(r_inner, r_outer, turns):
    theta = np.linspace(0, 2 * np.pi * turns, 1000)
    b = (r_outer - r_inner) / (2 * np.pi * turns)
    r = r_inner + b * theta
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    fig = plt.figure(figsize=(5, 5))
    plt.plot(x, y)

    plt.gca().set_aspect('equal', adjustable='box')
    plt.title("Spiral Antenna Geometry")
    plt.axis('off')

    filename = f"spiral_{uuid.uuid4().hex}.png"
    image_path = os.path.join(settings.MEDIA_ROOT, filename)

    plt.savefig(image_path)
    plt.close(fig)

    return settings.MEDIA_URL + filename

def convert_to_hz(value, unit):
    multipliers = {
        'hz': 1,
        'khz': 1e3,
        'mhz': 1e6,
        'ghz': 1e9,
    }
    return value * multipliers[unit]

"""
def generate_yagi_pattern(elements, frequency):
    theta = np.linspace(0, 2 * np.pi, 500)

    psi = (2 * np.pi * 0.15) * np.cos(theta) + (-0.5 * np.pi)
    af = np.abs(np.sin(elements * psi / 2) / np.sin(psi / 2))

    element_pattern = np.abs(np.sin(theta))

    total_pattern = (af / np.max(af)) * element_pattern

    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111, projection='polar')
    ax.plot(theta, total_pattern)
    ax.set_theta_zero_location("N")
    ax.set_title(f"Radiation Pattern ({elements}) Elements")

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)

    return image_base64
"""
