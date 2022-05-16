# -*- coding: utf-8 -*-
# Copyright © Felipe Bogaerts de Mattos
# Contact: me@felipebm.com

import numpy as np

from .module import Module
from .inverter import Inverter
from .strings import PVString
from ..config import get_safety_factor
from ..utils import get_disjuntores_disponiveis, calculo_disjuntor


class PowerPlantInfo:
    """
    Data from the power plant that is not needed to perform any simulation.
    """

    address: str
    plant_id: str
    class_type: str
    subgroup: str
    structural_type: str
    power_company: str


class PowerPlant:
    def __init__(
        self,
        module: Module,
        inverters: list[Inverter],
        inverter_count: list[int],
        module_count: int,
        din_padrao: int,
        din_geral: int,
        coordinates: list[float],
        inv_boolean: int,
        info: PowerPlantInfo = None,
    ):
        """
        :param Module module: Module class object
        :param list[Inverter] inverters: List of Inverter objects in the plant
        :param list[int] inverter_count: List with number of Inverters,
            respective to "inverters" parameter
        :param int module_count: Number of modules in the plant
        :param int din_padrao:
        :param int din_geral:
        :param list[float] coordinates: [LATITUDE, LONGITUDE]
        :param int inv_boolean: 0 for central inverter, 1 for micro
        :param PowerPlantInfo info: Info class object, contains metadata
        """
        self.module = module
        self.inverters = inverters
        self.inverter_count = np.array(inverter_count)
        self.module_count = int(module_count)
        self.din_padrao = float(din_padrao)
        self.din_geral = float(din_geral)
        self.coordinates = coordinates
        self.inv_boolean = int(inv_boolean)
        self.info = info

        self.validate_inputs()

    def validate_inputs(self) -> None:
        """
        Validates input data.

        :raises Exception: If there is incompatible input data
        """
        if self.inv_boolean not in [0, 1, 2]:  # verificando inv_boolean
            raise Exception('"inv_boolean" nao esta entre 0 e 2.')
        if len(self.inverters) != len(
            self.inverter_count
        ):  # verificando se as listas possuem a mesma dimensão
            raise Exception(
                "Lista com numero de inverters incompativel com a lista de "
                "inverters."
            )

    @property
    def pv_strings(self) -> list[PVString]:
        """
        :return: List of solar array strings in the power plant
        :rtype: list[PVString]
        """
        pv_strings = []

        numero_paineis_por_inversor = self.distribute_panels_by_inverter()

        for i, inv in enumerate(self.inverters):  # iterating through inverters
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
                    (numero_paineis_por_inversor[i] - module_count_inv)
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
        :return: Ideal power from modules in the power plant (W)        :rtype: float
        """
        return self.module_count * self.module.nominal_power

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

    def distribute_panels_by_inverter(self) -> list[int]:
        """
        :return: List with number of PV modules attributed to each inverter,
            respectively
        :rtype: np.array[int]
        """
        module_list_per_inv = np.array([])  # inicializando a lista
        for i, inv in enumerate(self.inverters):
            number_of_modules = (
                self.module_count
                * (inv.p_ac_nom / self.get_inverter_output_power())
                * self.inverter_count[i]
            )
            module_list_per_inv = np.append(
                module_list_per_inv, round(number_of_modules)
            )
        return module_list_per_inv

    def get_voltage_spd_poles(self):
        """
        Retorna a tensão e o número de polos do(s) DPS(s) da usina.
        Função itera sobre todos inverters, e retorna o valor máximo da tensão
        do DPS e do número de polos.
        """
        spd_voltage_array = np.array([])
        number_of_poles_array = np.array([])

        for i, inv in enumerate(self.inverters):
            if 100 <= float(inv.v_ac_nom) <= 150:
                spd_voltage_array = np.append(spd_voltage_array, 220)
                number_of_poles_array = np.append(number_of_poles_array, 1)
            elif 200 <= float(inv.v_ac_nom) <= 240:
                spd_voltage_array = np.append(spd_voltage_array, 220)
                number_of_poles_array = np.append(number_of_poles_array, 2)
            elif 360 <= float(inv.v_ac_nom) <= 400:
                spd_voltage_array = np.append(spd_voltage_array, 275)
                number_of_poles_array = np.append(number_of_poles_array, 3)
        tensao_dps = np.max(spd_voltage_array)
        n_polos = np.max(number_of_poles_array)

        return tensao_dps, n_polos

    def get_max_output_current_from_inverters(
        self, inv_id: int = None
    ) -> float:
        if inv_id == None:  # caso seja micro ou somente 1 inv. central
            corrente_max = 0
            for i, inv in enumerate(self.inverters):
                corrente_max += inv.i_ac_max * self.inverter_count[i]
        else:  # se houver mais de um inv. central
            corrente_max = self.inverters[inv_id].i_ac_max
        return corrente_max

    def get_din_list_plant(self) -> list[int]:
        # Inicializando lista que calcula disjuntores para cada um dos
        # inverters. Se houver mais de 1 inv. central, haverá mais de um
        # disjuntor (1 DIN por inversor).
        correntes_disjuntores = np.array([])

        if (
            len(self.inverter_count) > 1 or self.inverter_count[0] > 1
        ) and self.inv_boolean == 0:  # se houver mais de um inv. central
            for i in range(len(self.inverter_count)):
                correntes_disjuntores = np.append(
                    correntes_disjuntores,
                    calculo_disjuntor(
                        self.get_max_output_current_from_inverters(inv_id=i),
                        get_disjuntores_disponiveis(),
                        get_safety_factor(),
                    ),
                )
        else:  # caso seja micro ou somente 1 inv. central
            correntes_disjuntores = np.append(
                correntes_disjuntores,
                calculo_disjuntor(
                    self.get_max_output_current_from_inverters(),
                    get_disjuntores_disponiveis(),
                    get_safety_factor(),
                ),
            )

        return correntes_disjuntores

    def get_total_module_area(self) -> float:
        """
        :return: Total module area in the power plant (sq. m)
        :rtype: float
        """
        return self.module_count * self.module.area
