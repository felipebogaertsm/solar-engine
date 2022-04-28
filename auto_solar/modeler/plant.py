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
        inverter_count: int,
        module_count: int,
        din_padrao: int,
        din_geral: int,
        coordinates: list[float],
        inv_boolean: int,
        info: PowerPlantInfo = None,
    ):
        self.module = module
        self.inverters = inverters
        self.inverter_count = np.array(
            inverter_count
        )  # lista com quantidade de cada um dos inverters
        self.module_count = int(module_count)
        self.din_padrao = float(din_padrao)
        self.din_geral = float(din_geral)
        self.coordinates = coordinates
        self.inv_boolean = int(inv_boolean)  # 0 para central e 1 para micro
        self.info = info

        self.validate_inputs()

    def validate_inputs(self) -> None:
        """
        Valida os dados de entrada da classe Usina.
        Caso haja alguma inconsistência durante a declaração do objeto, um
        erro é disparado.
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
        Retorna uma lista de strings de painéis da usina.
        Esta lista é composta por objetos da classe PVString.
        """
        pv_strings = []

        numero_paineis_por_inversor = self.dividir_paineis_por_inv()

        for i, inv in enumerate(self.inverters):  # iterando inverters da usina
            pv_strings_inv_atual = []
            for j in range(inv.string_count):  # iterando strings do inversor
                # Pegando quantidade de módulos já alocados ao inversor atual:
                module_count_inv = (
                    0  # quantidade de módulos alocados ao inv atual
                )
                for (
                    string
                ) in (
                    pv_strings_inv_atual
                ):  # iterando strings já alocadas ao inversor atual
                    module_count_inv += string.module_count
                module_count_string_atual = int(
                    (numero_paineis_por_inversor[i] - module_count_inv)
                    / (inv.string_count - len(pv_strings_inv_atual))
                )
                pv_strings_inv_atual.append(
                    PVString(self.module, module_count_string_atual, inv)
                )
            pv_strings += pv_strings_inv_atual

        # Validação dos cálculos:
        sum_modules = 0  # declaração da variável de somatório dos módulos em todas strings
        for string in pv_strings:
            sum_modules += string.module_count
        if (
            sum_modules != self.module_count
        ):  # se a soma dos módulos nas strings for diferente do total de módulos na usina
            raise Exception(
                "Inconsistencia ao distribuir as strings do sistema."
            )

        return pv_strings

    def get_pv_strings_diferentes(self) -> list[int]:
        """
        Retorna lista de strings diferentes umas das outras.
        Por exemplo:
        Se um sistema possui as strings 1 a 10 com as mesmas propriedades e as
        strings de 11 a 13 com outras propriedades, o método deve retornar:
        [10, 13].
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
        Compara e retorna um boolean indicando se as strings 1 e 2 são iguais.
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

    def get_inverter_count_total(self) -> int:
        return np.sum(self.inverter_count)

    def get_cabeamento_por_polo(self) -> float:
        return 50 + 2 * self.module_count

    def get_numero_total_strings(self) -> int:
        numero_strings = 0
        for i, inv in enumerate(self.inverters):
            numero_strings += int(inv.string_count) * int(
                self.inverter_count[i]
            )
        return numero_strings

    def get_modulos_impares(self) -> bool:
        """
        Verifica se a quantidade de módulos é ímpar ou não.
        """
        if int(self.module_count) % self.get_numero_total_strings() != 0:
            return True
        else:
            return False

    def get_potencia_ideal(self) -> float:
        """
        Calcula e retorna a potência ideal de toda usina.
        """
        return self.module_count * self.modulo.potencia

    def get_potencia_real(self, T_ref) -> float:
        """
        Calcula e retorna a potência real de toda usina.
        """
        return self.get_potencia_ideal() * (
            1 - (T_ref * self.modulo.ppt / 100)
        )

    def get_potencia_inverters(self) -> float:
        """
        Calcula e retorna a potência total dos inverters de toda a usina.
        """
        p_total_inverters = 0
        for i, inv in enumerate(self.inverters):
            p_total_inverters += inv.p_ac_nom * self.inverter_count[i]  # em W
        return p_total_inverters

    def get_potencia_modulos(self) -> float:
        """
        Calcula e retorna a potência total de todos módulos da usina.
        """
        return self.modulo.potencia * self.module_count  # em Wp

    def get_potencia_ativa(self) -> float:
        """
        Calcula e retorna a potência ativa da usina.
        """
        pot_modulos = self.get_potencia_modulos()
        pot_invs = self.get_potencia_inverters()
        if pot_modulos <= pot_invs:
            return pot_modulos
        else:
            return pot_invs

    def is_sup(self, power_treshold: float = 10000) -> bool:
        if self.get_potencia_ativa() > power_treshold:
            return True
        else:
            return False

    def dividir_paineis_por_inv(self) -> list[int]:
        """
        Retorna lista com número de painéis para cada inversor.
        """
        lista_paineis_por_inv = np.array([])  # inicializando a lista
        for i, inv in enumerate(self.inverters):
            qte_paineis_atual = (
                self.module_count
                * (inv.p_ac_nom / self.get_potencia_inverters())
                * self.inverter_count[i]
            )
            lista_paineis_por_inv = np.append(
                lista_paineis_por_inv, round(qte_paineis_atual)
            )
        return lista_paineis_por_inv

    def get_tensao_polos_dps(self):
        """
        Retorna a tensão e o número de polos do(s) DPS(s) da usina.
        Função itera sobre todos inverters, e retorna o valor máximo da tensão
        do DPS e do número de polos.
        """
        tensao_dps_array = np.array([])
        n_polos_array = np.array([])
        for i, inv in enumerate(self.inverters):
            if 100 <= float(inv.v_saida_nom) <= 150:
                tensao_dps_array = np.append(tensao_dps_array, 220)
                n_polos_array = np.append(n_polos_array, 1)
            elif 200 <= float(inv.v_saida_nom) <= 240:
                tensao_dps_array = np.append(tensao_dps_array, 220)
                n_polos_array = np.append(n_polos_array, 2)
            elif 360 <= float(inv.v_saida_nom) <= 400:
                tensao_dps_array = np.append(tensao_dps_array, 275)
                n_polos_array = np.append(n_polos_array, 3)
        tensao_dps = np.max(tensao_dps_array)
        n_polos = np.max(n_polos_array)
        return tensao_dps, n_polos

    def get_corrente_maxima_invs(self, inv_id: int = None) -> float:
        if inv_id == None:  # caso seja micro ou somente 1 inv. central
            corrente_max = 0
            for i, inv in enumerate(self.inverters):
                corrente_max += inv.i_ac_max * self.inverter_count[i]
        else:  # se houver mais de um inv. central
            corrente_max = self.inverters[inv_id].i_ac_max
        return corrente_max

    def get_lista_din_usina(self) -> list[int]:
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
                        self.get_corrente_maxima_invs(inv_id=i),
                        get_disjuntores_disponiveis(),
                        get_safety_factor(),
                    ),
                )
        else:  # caso seja micro ou somente 1 inv. central
            correntes_disjuntores = np.append(
                correntes_disjuntores,
                calculo_disjuntor(
                    self.get_corrente_maxima_invs(),
                    get_disjuntores_disponiveis(),
                    get_safety_factor(),
                ),
            )

        return correntes_disjuntores

    def get_area_paineis(self) -> float:
        """
        Calculates total area occupied by PV modules in the plant.
        """
        return self.module_count * self.modulo.area
