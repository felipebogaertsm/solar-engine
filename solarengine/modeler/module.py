# -*- coding: utf-8 -*-
# Copyright © Felipe Bogaerts de Mattos
# Contact: me@felipebm.com

from .generic import Brand


class Module:
    def __init__(
        self,
        brand: Brand,
        nominal_power: float,
        v_oc: float,
        i_sc: float,
        v_max: float,
        i_max: float,
        ppt: float,
        efficiency: float,
        area: float,
    ) -> None:
        """
        All module data must be filled according to STC test data.

        :param str brand: Module manufacturer brand
        :param str model: Model of module
        :param float nominal_power: Nominal power of module, in STC (Wp)
        :param float v_oc: Open circuit voltage (V)
        :param float i_sc: Short circuit current (A)
        :param float v_max: Max. voltage (V)
        :param float i_max: Max. current (A)
        :param float ppt: Decrease in efficiency per degree celcius (% / C)
        :param float efficiency: Module efficiency, from 0 to 1
        :param float area: Module PV area (m ** 2)
        """
        self.brand = brand
        self.nominal_power = float(nominal_power)
        self.v_oc = float(v_oc)
        self.i_sc = float(i_sc)
        self.v_max = float(v_max)
        self.i_max = float(i_max)
        self.ppt = float(ppt)
        self.efficiency = float(efficiency)
        self.area = float(area)

    def __str__(self) -> str:
        return f"{self.model} - {self.brand} - {self.nominal_power}Wp"
