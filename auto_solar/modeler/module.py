# -*- coding: utf-8 -*-
# Copyright © Felipe Bogaerts de Mattos
# Contact: me@felipebm.com


class Module:
    def __init__(
        self,
        brand: str,
        model: str,
        nominal_power: float,
        v_oc: float,
        i_sc: float,
        v_max: float,
        i_max: float,
        ppt: float,
        efficiency: float,
        area: float,
    ) -> None:
        self.brand = brand
        self.model = model
        self.nominal_power = float(nominal_power)  # em Wp
        self.v_oc = float(v_oc)  # em V
        self.i_sc = float(i_sc)  # em A
        self.v_max = float(v_max)  # em V
        self.i_max = float(i_max)  # em A
        self.ppt = float(ppt)  # em % / grau C
        self.efficiency = float(efficiency)  # em %
        self.area = float(area)  # em m^2

    def __str__(self) -> str:
        return f"{self.model} - {self.brand} - {self.nominal_power}Wp"
