# -*- coding: utf-8 -*-
# Copyright © Felipe Bogaerts de Mattos
# Contact: me@felipebm.com

import numpy as np

from solarengine.modeler.module import Module
from solarengine.modeler.inverter import Inverter
from solarengine.modeler.strings import PVString
from solarengine.config import get_safety_factor
from solarengine.utils import get_available_din, size_circuit_breaker


class PowerPlant:
    def __init__(
        self,
        module: Module,
        module_count: int,
        inverters: list[Inverter],
        inverter_count: list[int],
        din_padrao: int,
        coordinates: list[float],
        inv_boolean: int,
        surface_tilt: float = 22.0,
        surface_azimuth: float = 180.0,
    ):
        """
        :param Module module: Module class object
        :param list[Inverter] inverters: List of Inverter objects in the plant
        :param list[int] inverter_count: List with number of Inverters,
            respective to "inverters" parameter
        :param int module_count: Number of modules in the plant
        :param int din_padrao: DIN of the plant
        :param list[float] coordinates: [LATITUDE, LONGITUDE]
        :param int inv_boolean: 0 for central inverter, 1 for micro
        :param float surface_tilt: Tilt angle of the PV array
        :param float surface_azimuth: Azimuth angle of the PV array
        """
        self.module = module
        self.module_count = int(module_count)
        self.inverters = inverters
        self.inverter_count = np.array(inverter_count)
        self.din_padrao = din_padrao
        self.coordinates = coordinates
        self.inv_boolean = int(inv_boolean)
        self.surface_tilt = surface_tilt
        self.surface_azimuth = surface_azimuth

        self.validate_inputs()

    def validate_inputs(self) -> None:
        """
        Validates input data.

        :raises Exception: If there is incompatible input data
        """
        assert self.inv_boolean in (
            0,
            1,
        ), '"inv_boolean" should be either 0 or 1'

        assert len(self.inverters) == len(
            self.inverter_count
        ), "Inverter and inverter_count lists must have the same length"

    @property
    def pv_strings(self) -> list[PVString]:
        """
        :return: List of solar array strings in the power plant
        :rtype: list[PVString]
        """
        pv_strings = []

        for i, inv in enumerate(self.inverters):  # iterating through inverters
            module_count = self.get_module_count_for_inverter(index=i)

            pv_strings_inv_current = []

            for _ in range(
                inv.string_count
            ):  # iterating through strings in the inverter
                module_count_inv = (
                    0  # number of modules allocated to current inverter
                )
                # Iterating through strings already allocated to current
                # inverter:
                for string in pv_strings_inv_current:
                    module_count_inv += string.module_count
                module_count_string_current = int(
                    (module_count - module_count_inv)
                    / (inv.string_count - len(pv_strings_inv_current))
                )
                pv_strings_inv_current.append(
                    PVString(self.module, module_count_string_current, inv)
                )
            pv_strings += pv_strings_inv_current

        return pv_strings

    def get_different_pv_strings(self) -> list[int]:
        """
        Example:
        If a PV system contains stirngs 1 to 10 with similar attributes and 11
        to 13 with other attributes, the method must return:
        [10, 13].

        :return: List of strings that are different from each other
        :rtype: list[int]
        """
        pv_strings_diferentes = [0]
        j = 0
        for i in range(len(self.pv_strings)):
            if self.compare_pv_string(self, i, j):
                pass
            else:
                pv_strings_diferentes.append(i)
                j = i

        return pv_strings_diferentes

    def compare_pv_string(
        self, index_pv_string_1: int, index_pv_string_2: int
    ) -> bool:
        """
        Compares and returns boolean indicating if strings 1 and 2 share
        similar model and module_count properties.

        :param int index_pv_string_1: Index of PV string
        :param int index_pv_string_2: Index of PV string
        :return: True if both strings share same Inv. model and module count
        :rtype: bool
        """
        module_count_str_1 = self.pv_strings[index_pv_string_1].module_count
        module_count_str_2 = self.pv_strings[index_pv_string_2].module_count
        modelo_inv_str_1 = self.pv_strings[index_pv_string_1].inversor.modelo
        modelo_inv_str_2 = self.pv_strings[index_pv_string_2].inversor.modelo

        if (
            module_count_str_1 == module_count_str_2
            and modelo_inv_str_1 == modelo_inv_str_2
        ):
            return True
        else:
            return False

    def get_number_of_inverters(self) -> int:
        """
        :return: Total number of inverters in the plant
        :rtype: int
        """
        return np.sum(self.inverter_count)

    def get_cable_length_per_pole(self) -> float:
        return 50 + 2 * self.module_count

    def get_number_of_strings(self) -> int:
        numero_strings = 0
        for i, inv in enumerate(self.inverters):
            numero_strings += int(inv.string_count) * int(
                self.inverter_count[i]
            )
        return numero_strings

    def is_modules_odd(self) -> bool:
        """
        Verifies if the number of PV modules is odd or not.

        :return: True if total number of PV modules is not odd
        :rtype: bool
        """
        if int(self.module_count) % self.get_number_of_strings() != 0:
            return True
        else:
            return False

    def get_ideal_module_output_power(self) -> float:
        """
        :return: Ideal power from modules in the power plant (W)
        :rtype: float
        """
        return self.module_count * self.module.p_nominal

    def get_real_module_output_power(self, T_ref) -> float:
        """
        :return: Real power from modules in the power plant (W)
        :rtype: float
        """
        return self.get_ideal_module_output_power() * (
            1 - (T_ref * self.module.ppt / 100)
        )

    def get_inverter_output_power(self) -> float:
        """
        :return: Total power from inverters in the plant (W)
        :rtype: float
        """
        total_power = 0

        for i, inv in enumerate(self.inverters):
            total_power += inv.p_ac_nom * self.inverter_count[i]

        return total_power

    def get_active_power(self) -> float:
        """
        Calculates total power generated by the plant. Chooses the largest of
        either the module total power or the inverter total power.

        :return: Total power from the plant (W)
        :rtype: float
        """
        pot_modules = self.get_ideal_module_output_power()
        pot_invs = self.get_inverter_output_power()

        if pot_modules <= pot_invs:
            return pot_modules
        else:
            return pot_invs

    def is_sup(self, power_treshold: float = 10000) -> bool:
        """
        :param Optional[float] power_treshold: Default to 10 kW
        :return: True if total active power is superior to power_treshold
        :rtype: bool
        """
        if self.get_active_power() > power_treshold:
            return True
        else:
            return False

    def get_module_count_for_inverter(self, index: int) -> int:
        """
        :param int index: Index of inverter
        :return: Number of PV modules attributed to inverter
        :rtype: int
        """
        inv = self.inverters[index]
        inv_count = self.inverter_count[index]

        return round(
            self.module_count
            * (inv.p_ac_nom / self.get_inverter_output_power())
            * inv_count
        )

    def get_voltage_spd_poles(self):
        """
        Retorna a tensão e o número de polos do(s) DPS(s) da usina.
        Função itera sobre todos inverters, e retorna o valor máximo da tensão
        do DPS e do número de polos.
        """
        spd_voltage_array = np.array([])
        number_of_poles_array = np.array([])

        for inv in self.inverters:
            if 100 <= float(inv.v_ac_nom) <= 150:
                spd_voltage_array = np.append(spd_voltage_array, 220)
                number_of_poles_array = np.append(number_of_poles_array, 1)
            elif 200 <= float(inv.v_ac_nom) <= 240:
                spd_voltage_array = np.append(spd_voltage_array, 220)
                number_of_poles_array = np.append(number_of_poles_array, 2)
            elif 360 <= float(inv.v_ac_nom) <= 400:
                spd_voltage_array = np.append(spd_voltage_array, 275)
                number_of_poles_array = np.append(number_of_poles_array, 3)
        spd_voltage = np.max(spd_voltage_array)
        pole_count = np.max(number_of_poles_array)

        return spd_voltage, pole_count

    def get_max_output_current_from_inverters(
        self, inv_index: int = None
    ) -> float:
        if inv_index == None:  # caso seja micro ou somente 1 inv. central
            corrente_max = 0
            for i, inv in enumerate(self.inverters):
                corrente_max += inv.i_ac_max * self.inverter_count[i]
        else:  # se houver mais de um inv. central
            corrente_max = self.inverters[inv_index].i_ac_max
        return corrente_max

    def get_din_list_plant(self) -> list[int]:
        # If there's more than 1 central inverter, there will be more than 1
        # DIN
        din_list = np.array([])

        # If there's more than 1 central inverter:
        if len(self.inverter_count) > 1 and self.inv_boolean == 0:
            for i in range(len(self.inverter_count)):
                din_list = np.append(
                    din_list,
                    size_circuit_breaker(
                        self.get_max_output_current_from_inverters(
                            inv_index=i
                        ),
                        get_available_din(),
                        get_safety_factor(),
                    ),
                )
        else:  # if it's a micro inv or multiple central invs
            din_list = np.append(
                din_list,
                size_circuit_breaker(
                    self.get_max_output_current_from_inverters(),
                    get_available_din(),
                    get_safety_factor(),
                ),
            )

        return din_list

    def get_total_module_area(self) -> float:
        """
        :return: Total module area in the power plant (sq. m)
        :rtype: float
        """
        return self.module_count * self.module.area
