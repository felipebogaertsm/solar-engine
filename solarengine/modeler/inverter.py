# -*- coding: utf-8 -*-
# Copyright © Felipe Bogaerts de Mattos
# Contact: me@felipebm.com

from solarengine.modeler.generic import PhysicalProperties


class Inverter:
    def __init__(
        self,
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
        physical_properties: PhysicalProperties,
    ) -> None:
        """
        :param str category: Either 'central' or 'micro'
        :param float v_dc_max: Max. input voltage (V)
        :param str voltage_range_mppt: Voltage range for one MPPT
        :param float p_dc_max_input: Max. input power (W)
        :param float v_dc_start: DC (input) starting voltage (V)
        :param float i_dc_max: Max. input current (A)
        :param int string_count: Number of strings (1 for a micro inverter)
        :param float p_max: Max. power (W)
        :param float i_ac_max: Max. output power (A)
        :param float p_ac_nom: Nominal output power (W)
        :param float v_ac_nom: Nominal output voltage (V)
        :param float freq: Inverter frequency (Hz)
        :param float efficiency_mppt: MPPT efficiency, number from 0 to 1
        :param float efficiency_max: Max. efficiency, number from 0 to 1
        :param float weight: Total weight (kg)
        :param str dimensions: dimensions in 'WIDTHxHEIGHTxDEPTH' (mm)
        """
        self.category = category
        self.v_dc_max = float(v_dc_max)
        self.voltage_range_mppt = voltage_range_mppt
        self.p_dc_max_input = float(p_dc_max_input)
        self.v_dc_start = v_dc_start
        self.i_dc_max = i_dc_max
        self.string_count = int(string_count)
        self.p_max = float(p_max)
        self.i_ac_max = float(i_ac_max)
        self.p_ac_nom = float(p_ac_nom)
        self.v_ac_nom = float(v_ac_nom)
        self.freq = freq
        self.efficiency_mppt = efficiency_mppt
        self.efficiency_max = efficiency_max

        self.physical_properties = physical_properties

    def __str__(self) -> str:
        return f"Inverter {self.p_ac_nom / 1000}kW"
