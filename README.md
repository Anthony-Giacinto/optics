# optics
Demonstrates the laws of reflection and refraction using VPython.

## Table of Contents
* [General info](#general-info)
* [Technologies](#technologies)
* [How to Use](#how-to-use)

## General Info
This demo file calculates the paths of light rays travelling through different media using the laws of reflection and refraction:
1. incident angle = reflected angle
2. incident index  x  sin(incident angle) = transmitted index  x  sin(transmitted angle) ,  

where incident angle is the angle of the incident light ray, reflected angle is the angle of the reflected light ray, transmitted angle is the angle of the transmitted light ray, incident index is the refractive index of the medium containing the incident light ray, and  transmitted index is the refractive index of the medium containing the transmitted light ray (all angles are measured from the normal).  

There are also the options to animate the light rays through a range of incident angle values and to visually display the reflectance and transmittance of the light.  

The user must provide an incident angle, incident index, and transmitted index to run main.

## Technologies
Project was created with:
* Python 3.6

## How to Use
All you need to do is run optics.main.  
Here are the arguments for main:
* incident_angle: The angle of the incident light ray in units of degrees (0 <= angle <= 90).
* incident_index: Refractive index of incident medium (speed of light in vacuum / speed of light in incident medium).
* transmitted_index: Refractive index of transmitted medium (speed of light in vacuum / speed of light in transmitted medium).
* parallel: True if electric field is parallel to the plane of incidence and False if not (default is False).
* labels: True if you want to display boxes containing important values (default is True).
* irradiance: True if you want to visualize the reflectance and transmittance of the light (default is True).
* incident_medium: The label for the incident medium; must be a string (default is '').
* transmitted_medium: The label for the transmitted medium; must be a string (default is '').
* display_width: VPython canvas width (default is 1900).
* display_height: VPython canvas height (default is 950).
* animate: If true, will animate the light rays through a range of angles (default is False).
* angle_range: A tuple that represents the start, end, and step size angles that you wish to animate in degrees; will override the incident_angle value given; should only be within the range of 0 to 90 (default is (0, 90, 10)).
