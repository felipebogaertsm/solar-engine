# -*- coding: utf-8 -*-
# Copyright © Felipe Bogaerts de Mattos
# Contact: me@felipebm.com

import numpy as np

from auto_solar.tests.fixtures import (
    power_plant_single_central_inverter,
    power_plant_two_central_inverters_equal,
    trina_410_module,
    fronius_5k_inverter,
)


def test_modules_in_pv_strings_of_single_central_inverter_power_plant(
    power_plant_single_central_inverter,
):
    plant = power_plant_single_central_inverter

    pv_modules = [pv_string.module_count for pv_string in plant.pv_strings]
    sum_modules = np.sum(pv_modules)

    assert sum_modules == plant.module_count


def test_modules_in_pv_strings_of_dual_central_inverter_power_plant(
    power_plant_two_central_inverters_equal,
):
    plant = power_plant_two_central_inverters_equal

    pv_modules = [pv_string.module_count for pv_string in plant.pv_strings]
    sum_modules = np.sum(pv_modules)

    assert sum_modules == plant.module_count


def test_pv_string_v_oc(power_plant_single_central_inverter):
    plant = power_plant_single_central_inverter

    for pv_string in plant.pv_strings:
        assert pv_string.v_oc == pv_string.module.v_oc * pv_string.module_count
