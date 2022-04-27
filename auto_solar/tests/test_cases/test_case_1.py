# -*- coding: utf-8 -*-
# Copyright © Felipe Bogaerts de Mattos
# Contact: me@felipebm.com

from auto_solar.modeler.inverter import Inverter
from auto_solar.modeler.module import Module
from auto_solar.modeler.plant import PowerPlant


def test_case_1():
    module = Module(
        brand="Trina Solar",
        model="TSM-410",
        nominal_power=410,  # in Wp,
        v_oc=50.0,
        i_sc=10.25,
        v_max=42.6,
        i_max=9.63,
        ppt=0.37,
        efficiency=20.0,
        area=2,
    )

    inverter = Inverter(
        brand="Fronius",
        model="PRIMO 5.0-1",
        category="central",
        v_dc_max=1000,
        voltage_range_mppt="240-800 V",
        p_dc_max_input=7500,
        v_dc_start=420,
        i_dc_max=36,
        string_count=2,
        p_max=5000,
        i_ac_max=20.8,
        p_ac_nom=5000,
        v_ac_nom=220,
        freq=60,
        efficiency_mppt=0.99,
        efficiency_max=0.99,
        weight=21.5,
        dimensions="429x627x206",  # in mm
    )

    plant = PowerPlant(
        module=module,
        inverters=[inverter],
        inverter_count=[1],
        module_count=12,
        din_padrao=60,
        din_geral=60,
        coordinates=[-22.02, -42.02],
        inv_boolean=0,
    )
