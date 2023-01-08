# -*- coding: utf-8 -*-
# Copyright © Felipe Bogaerts de Mattos
# Contact: me@felipebm.com

from .inverter import Inverter
from .module import Module


class PVString:
    """
    Models a photovoltaic string.
    A microinverter is modeled as a central inverter with only one string.
    """

    def __init__(
        self,
        module: Module,
        module_count: int,
        inverter: Inverter,
    ) -> None:
        """
        :param Module module: Module class object
        :param int module_count: Number of modules in the string
        :param Inverter inverter: Inverter class object
        """
        self.module = module
        self.module_count = int(module_count)
        self.inverter = inverter

    @property
    def v_oc(self) -> float:
        """
        Calculates the open circuit voltage of the PV string.

        :return: Open circuit voltage in Volts
        """
        return self.module.v_oc * self.module_count

    @property
    def v_max(self) -> float:
        """
        Calculates the max. voltage of the PV string.

        :return: Maximum voltage in Volts
        """
        self.v_max = self.module.v_max * self.module_count
        return self.v_max

    @property
    def i_sc(self) -> float:
        """
        :return: Short circuit voltage in Amperes
        """
        return float(self.module.i_sc)

    @property
    def i_max(self) -> float:
        """
        :return: Maximum current in Amperes
        """
        return float(self.module.i_max)

    @property
    def power_output_ideal(self) -> float:
        """
        :return: Ideal power in Watts
        """
        return self.module_count * self.module.potencia

    @property
    def power_output_real(self, T_ref: float) -> float:
        """
        :param float T_ref: Average operational temperature of the module
        :return: Real power in Watts
        """
        return self.power_output_ideal() * (
            1 - (T_ref * self.module.ppt / 100)
        )
