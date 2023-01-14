# -*- coding: utf-8 -*-
# Copyright © Felipe Bogaerts de Mattos
# Contact: me@felipebm.com

import pytest

from ..modeler.generic import Brand, PhysicalProperties
from ..modeler.inverter import Inverter
from ..modeler.module import Module
from ..modeler.plant import PowerPlant


@pytest.fixture
def trina_410_module():
    return Module(
        brand=Brand(name="Trina Solar", model="TSM-410"),
        nominal_power=410,  # in Wp,
        v_oc=50.0,
        i_sc=10.25,
        v_max=42.6,
        i_max=9.63,
        ppt=0.37,
        efficiency=20.0,
        area=2,
    )


@pytest.fixture
def fronius_5k_inverter():
    return Inverter(
        brand=Brand(name="Fronius", model="PRIMO 5.0-1"),
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
        physical_properties=PhysicalProperties(
            weight=21.5, width=429, height=627, depth=206
        ),
    )


@pytest.fixture
def fronius_8k_inverter():
    return Inverter(
        brand=Brand(name="Fronius", model="PRIMO 8.2-1"),
        category="central",
        v_dc_max=1000,
        voltage_range_mppt="270-800 V",
        p_dc_max_input=12300,
        v_dc_start=420,
        i_dc_max=36,
        string_count=2,
        p_max=8200,
        i_ac_max=34.2,
        p_ac_nom=7900,
        v_ac_nom=220,
        freq=60,
        efficiency_mppt=0.99,
        efficiency_max=0.99,
        physical_properties=PhysicalProperties(
            weight=21.5, width=429, height=627, depth=206
        ),
    )


@pytest.fixture
def power_plant_single_central_inverter(trina_410_module, fronius_5k_inverter):
    return PowerPlant(
        module=trina_410_module,
        inverters=[fronius_5k_inverter],
        inverter_count=[1],
        module_count=12,
        din_padrao=60,
        din_geral=60,
        coordinates=[-22.02, -42.02],
        inv_boolean=0,
    )


@pytest.fixture
def power_plant_two_central_inverters_equal(
    trina_410_module, fronius_5k_inverter
):
    return PowerPlant(
        module=trina_410_module,
        inverters=[fronius_5k_inverter],
        inverter_count=[2],
        module_count=25,
        din_padrao=60,
        din_geral=60,
        coordinates=[-22.02, -42.02],
        inv_boolean=0,
    )


@pytest.fixture
def power_plant_two_central_inverters_different(
    trina_410_module, fronius_5k_inverter, fronius_8k_inverter
):
    return PowerPlant(
        module=trina_410_module,
        inverters=[fronius_8k_inverter, fronius_5k_inverter],
        inverter_count=[1, 1],
        module_count=32,
        din_padrao=60,
        din_geral=60,
        coordinates=[-22.02, -42.02],
        inv_boolean=0,
    )
