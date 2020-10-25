"""
Contains a demonstration of the laws of reflection and refraction using VPython.

Functions:
    main: A geometric optics demo that visualizes the laws of reflection and refraction while also providing
    the option of visualizing reflectance and transmittance.
"""


import math
from vpython import canvas, vector, box, color, curve, label
from .medium import Air, Glass
from .optics import Optics


def main(incident_angle, incident_index, transmitted_index, parallel=False, labels=True, irradiance=True,
         incident_medium='', transmitted_medium='', display_width=1900, display_height=950, animate=False,
         angle_range=(0, 90, 10)):
    """ A geometric optics demo that visualizes the laws of reflection and refraction while also providing
    the option of visualizing reflectance and transmittance.

    :param incident_angle: (float) The angle of the incident light ray in units of degrees (0 <= angle <= 90).
    :param incident_index: (float) Refractive index of incident medium
    (speed of light in vacuum / speed of light in incident medium).
    :param transmitted_index: (float) Refractive index of transmitted medium
    (speed of light in vacuum / speed of light in transmitted medium).
    :param parallel: (bool) True if electric field is parallel to the plane of incidence and False if not
    (default is False).
    :param labels: (bool) True if you want to display boxes containing important values (default is True).
    :param irradiance: (bool) True if you want to visualize the reflectance and transmittance of the light
    (default is True).
    :param incident_medium: (str) The label for the incident medium; must be a string (default is '').
    :param transmitted_medium: (str) The label for the transmitted medium; must be a string (default is '').
    :param display_width: (int) VPython canvas width (default is 1900).
    :param display_height: (int) VPython canvas height (default is 950).
    :param animate: (bool) If true, will animate the light rays through a range of angles (default is False).
    :param angle_range: (lsit) A tuple that represents the start, end, and step size angles that you wish to animate in
    degrees; will override the incident_angle value given; should only be within the range of 0 to 90
    (default is (0, 90, 10)).
    """

    scene = canvas(background=color.black, width=display_width, height=display_height)
    box(pos=vector(0, -0.5, 0), size=vector(3, -0.5*2, -0.5*2), opacity=0.2)

    if animate:
        incident_angle_updated = angle_range[0]
    else:
        incident_angle_updated = incident_angle

    op = Optics(incident_angle=incident_angle_updated, incident_index=incident_index,
                transmitted_index=transmitted_index, parallel=parallel)
    normal = op.ray_position(math.pi)
    curve(pos=[normal*-1, normal], color=color.white)
    transmitted_ray = curve(pos=[op.rays[2][0], op.rays[2][1]], color=color.red, emissive=True)
    reflected_ray = curve(pos=[op.rays[1][0], op.rays[1][1]], color=color.red, emissive=True)
    incident_ray = curve(pos=[op.rays[0][0], op.rays[0][1]], color=color.red, emissive=True)

    if irradiance:
        transmitted_ray.color = vector(op.irradiance[1], 0, 0)
        reflected_ray.color = vector(op.irradiance[0], 0, 0)

    if labels:
        if not isinstance(incident_medium, str):
            incident_medium_label = ''
        else:
            incident_medium_label = incident_medium
        if not isinstance(transmitted_medium, str):
            transmitted_medium_label = ''
        else:
            transmitted_medium_label = transmitted_medium

        incident_index_label = f'n\u2081 = {op.incident_index}'
        transmitted_index_label = f'n\u2082 = {op.transmitted_index}'

        incident_angle_label = f'\u03B8\u1d62 ~ {round(math.degrees(op.incident_angle), 1)} \u00b0'
        if op.incident_angle >= op.critical_angle:
            transmitted_angle_label = '\u03B8\u209c = NaN'
        else:
            transmitted_angle_label = f'\u03B8\u209c ~ {round(math.degrees(op.transmitted_angle), 1)} \u00b0'

        if irradiance:
            reflectance_label = f'\nR ~ {round(op.irradiance[0], 2)}'
            transmittance_label = f'\nT ~ {round(op.irradiance[1], 2)}'
        else:
            reflectance_label, transmittance_label = '', ''

        incident_combined_label = f'{incident_medium_label}\n{incident_index_label}\n{incident_angle_label}' \
                                  f'{reflectance_label}'
        transmitted_combined_label = f'{transmitted_medium_label}\n{transmitted_index_label}\n' \
                                     f'{transmitted_angle_label}'f'{transmittance_label}'
        incident_label = label(pos=vector(-1.5, 0.5, 0), text=incident_combined_label)
        transmitted_label = label(pos=vector(-1.5, -0.5, 0), text=transmitted_combined_label)
        label(pos=vector(1.5, 1, 0), text='Law of Reflection\n\u03B8\u1d62 = \u03B8\u1D63')
        label(pos=vector(1.5, 0.8, 0), text='Law of Refraction\nn\u2081sin(\u03B8\u1d62) = n\u2082sin(\u03B8\u209c)')

    if animate:
        while True:
            scene.waitfor('redraw')

            if math.degrees(op.incident_angle) < angle_range[1]:
                op.incident_angle = round(math.degrees(op.incident_angle)) + angle_range[2]
            else:
                op.incident_angle = angle_range[0]

            transmitted_ray.modify(1, op.rays[2][1])
            reflected_ray.modify(1, op.rays[1][1])
            incident_ray.modify(1, op.rays[0][1])

            if irradiance:
                reflected_ray.color = vector(op.irradiance[0], 0, 0)
                transmitted_ray.color = vector(op.irradiance[1], 0, 0)

            if labels:
                incident_angle_label = f'\u03B8\u1d62 ~ {round(math.degrees(op.incident_angle), 1)} \u00b0'
                if op.incident_angle >= op.critical_angle:
                    transmitted_angle_label = '\u03B8\u209c = NaN'
                else:
                    transmitted_angle_label = f'\u03B8\u209c ~ {round(math.degrees(op.transmitted_angle), 1)} \u00b0'

                if irradiance:
                    reflectance_label = f'\nR ~ {round(op.irradiance[0], 2)}'
                    transmittance_label = f'\nT ~ {round(op.irradiance[1], 2)}'
                else:
                    reflectance_label, transmittance_label = '', ''

                incident_label.text = f'{incident_medium_label}\n{incident_index_label}\n{incident_angle_label}' \
                                      f'{reflectance_label}'
                transmitted_label.text = f'{transmitted_medium_label}\n{transmitted_index_label}\n' \
                                         f'{transmitted_angle_label}'f'{transmittance_label}'


if __name__ == '__main__':
    main(incident_angle=50, incident_index=Air.index, transmitted_index=Glass.index, incident_medium=Air.name,
         transmitted_medium=Glass.name, animate=False, irradiance=True, angle_range=(0, 90, 10))
