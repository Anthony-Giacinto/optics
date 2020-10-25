"""
Contains the Optics class.

Classes:
    Optics: Collection of functions for geometric optics that determine the orientation of light rays.
"""


import math
from vpython import vector


class Optics:
    """ Collection of functions for geometric optics that determine the orientation of light rays.

    Instance Attributes:
        incident_angle: (float) The angle of the incident light ray in units of degrees (0 <= angle <= 90).
        incident_index: (float) Refractive index of the incident medium
        (speed of light in vacuum / speed of light in incident medium).
        transmitted_index: (float) Refractive index of transmitted medium
        (speed of light in vacuum / speed of light in transmitted medium).
        parallel: (bool) True if electric field is parallel to the plane of incidence, False if not (default is False).
    """

    def __init__(self, incident_angle, incident_index, transmitted_index, parallel=False):
        """
        :param incident_angle: (float) The angle of the incident light ray in units of degrees (0 <= angle <= 90).
        :param incident_index: (float) Refractive index of incident medium
        (speed of light in vacuum / speed of light in incident medium).
        :param transmitted_index: (float) Refractive index of transmitted medium
        (speed of light in vacuum / speed of light in transmitted medium).
        :param parallel: (bool) True if electric field is parallel to the plane of incidence, False if not
        (default is False).
        """

        self._incident_angle = incident_angle
        self._incident_index = incident_index
        self._transmitted_index = transmitted_index
        self.parallel = parallel

    @property
    def incident_angle(self):
        """ Makes sure that incident_angle is always between 0 and 90 degrees. """

        if 0 <= self._incident_angle <= 90:
            return math.radians(self._incident_angle)
        else:
            raise ValueError('The incident angle must be between 0 and 90 degrees')

    @incident_angle.setter
    def incident_angle(self, value):
        """ Allows you to update the value of incident_angle outside the class. """

        self._incident_angle = value

    @property
    def incident_index(self):
        return self._incident_index

    @property
    def transmitted_index(self):
        return self._transmitted_index

    @property
    def transmitted_angle(self):
        """ Calculates the transmitted angle using Snell's Law / the Law of Refraction.

        :return: (float) The transmitted angle in radians.
        """

        return math.asin(self.incident_index/self.transmitted_index*math.sin(self.incident_angle))

    @property
    def critical_angle(self):
        """ Determines the critical angle of the incident light ray, if any.

        :return: (float) Returns the critical angle in radians; if no critical angle, returns pi/2 radians.
        """

        if self.incident_index > self.transmitted_index:
            return math.asin(self.transmitted_index/self.incident_index)
        else:
            return math.pi/2

    @property
    def irradiance(self):
        """ Calculates the reflectance and transmittance of the light rays. First by calculating
        the reflection and transmission amplitude coefficients of the electric field using the Fresnel equations
        (parallel or perpendicular to the plane of incidence.

        :return: (list) Reflectance, Transmittance.
        """
        
        if self.incident_angle >= self.critical_angle:
            reflectance_coeff = 1.0
            transmittance_coeff = 0.0
        elif self.parallel:
            reflectance_coeff = (self.transmitted_index*math.cos(self.incident_angle) -
                                self.incident_index*math.cos(self.transmitted_angle)) / \
                                     (self.incident_index*math.cos(self.transmitted_angle) +
                                      self.transmitted_index*math.cos(self.incident_angle))
            transmittance_coeff = (2*self.incident_index*math.cos(self.incident_angle)) / \
                                       (self.incident_index*math.cos(self.transmitted_angle) +
                                        self.transmitted_index*math.cos(self.incident_angle))
        else:
            reflectance_coeff = (self.incident_index*math.cos(self.incident_angle) -
                                self.transmitted_index*math.cos(self.transmitted_angle)) / \
                                     (self.incident_index*math.cos(self.incident_angle) +
                                      self.transmitted_index*math.cos(self.transmitted_angle))
            transmittance_coeff = (2*self.incident_index*math.cos(self.incident_angle)) / \
                                       (self.incident_index*math.cos(self.incident_angle) +
                                        self.transmitted_index*math.cos(self.transmitted_angle))
        if reflectance_coeff == 0:
            reflectance = 0
        else:
            reflectance = reflectance_coeff**2
        if transmittance_coeff == 0:
            transmittance = 0
        else:
            transmittance = ((self.transmitted_index*math.cos(self.transmitted_angle)) /
                         (self.incident_index*math.cos(self.incident_angle)))*(transmittance_coeff**2)
        return reflectance, transmittance

    @property
    def rays(self):
        """ Determines the start and end positions of all the three light rays.

        :return: (list) Incident, reflected, and transmitted light ray start and end positions.
        """

        origin = vector(0, 0, 0)
        reflected_ray_end = self.ray_position(self.incident_angle)
        incident_ray_end = self.ray_position(self.incident_angle)
        incident_ray_end.x *= -1
        incident_ray = (origin, incident_ray_end)
        reflected_ray = (origin, reflected_ray_end)

        if self.incident_angle < self.critical_angle:
            transmitted_ray_end = self.ray_position(self.transmitted_angle)
            transmitted_ray_end.y *= -1
            transmitted_ray = (origin, transmitted_ray_end)
        else:
            transmitted_ray = (origin, reflected_ray_end)
        return incident_ray, reflected_ray, transmitted_ray

    @staticmethod
    def ray_position(angle):
        """ Calculates the end position of the ray with the start assumed to be at the origin.

        :param angle: (float) The desired angle in radians.
        :return: (VPython vector) The end position of the ray in cartesian coordinates.
        """

        return vector(math.cos(math.pi/2 - angle), math.sin(math.pi/2 - angle), 0)
