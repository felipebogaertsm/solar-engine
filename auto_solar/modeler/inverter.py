# -*- coding: utf-8 -*-
# Copyright © Felipe Bogaerts de Mattos
# Contact: me@felipebm.com


class Inverter:
    def __init__(
        self,
        brand: str,
        model: str,
        category: str,
        v_dc_max: float,
        voltage_range_mppt: str,
        p_dc_max_input: float,
        v_dc_start: float,
        i_dc_max: float,
        string_count: int,
        p_max: float,
        i_ac_max: float,
        p_ac_nom: float,
        v_ac_nom: float,
        freq: float,
        efficiency_mppt: float,
        efficiency_max: float,
        weight: float,
        dimensions: str,  # in mm
    ) -> None:
        """
        :param category: either central or micro
        """
        self.brand = brand
        self.model = model
        self.category = category
        self.v_dc_max = float(v_dc_max)  # em V
        self.voltage_range_mppt = voltage_range_mppt
        self.p_dc_max_input = float(p_dc_max_input)  # em W
        self.v_dc_start = v_dc_start  # em V
        self.i_dc_max = i_dc_max  # em A
        self.string_count = int(string_count)
        self.p_max = float(p_max)  # em W
        self.i_ac_max = float(i_ac_max)  # em A
        self.p_ac_nom = float(p_ac_nom)  # em W
        self.v_ac_nom = float(v_ac_nom)  # em V
        self.freq = freq  # em Hz
        self.efficiency_mppt = efficiency_mppt  # em %
        self.efficiency_max = efficiency_max  # em %
        self.weight = weight  # em kg
        self.dimensions = dimensions  # em mm

    def __str__(self) -> str:
        return f"{self.model} - {self.brand} - {self.p_ac_nom / 1000}kW"
