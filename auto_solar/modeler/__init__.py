# -*- coding: utf-8 -*-
# Copyright © Felipe Bogaerts de Mattos
# Contact: me@felipebm.com

import numpy as np

from utils import get_disjuntores_disponiveis, calculo_disjuntor
from config import get_safety_factor


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


class Inverter:
    def __init__(
        self,
        brand: str,
        model: str,
        v_cc_max: float,
        voltage_range_mppt: float,
        p_cc_max_input: float,
        v_cc_start: float,
        i_cc_max: float,
        string_count: int,
        p_max: float,
        i_ca_max: float,
        p_ca_nom: float,
        v_saida_nom: float,
        freq: float,
        eficiencia_mppt: float,
        eficiencia_max: float,
        peso: float,
        dimensoes: str,
    ) -> None:
        self.brand = brand
        self.model = model
        self.v_cc_max = float(v_cc_max)  # em V
        self.voltage_range_mppt = voltage_range_mppt
        self.p_cc_max_input = float(p_cc_max_input)  # em W
        self.v_cc_start = v_cc_start  # em V
        self.i_cc_max = i_cc_max  # em A
        self.string_count = int(string_count)
        self.p_max = float(p_max)  # em W
        self.i_ca_max = float(i_ca_max)  # em A
        self.p_ca_nom = float(p_ca_nom)  # em W
        self.v_saida_nom = float(v_saida_nom)  # em V
        self.freq = freq  # em Hz
        self.eficiencia_mppt = eficiencia_mppt  # em %
        self.eficiencia_max = eficiencia_max  # em %
        self.peso = peso  # em kg
        self.dimensoes = dimensoes  # em mm


class PowerPlant:
    def __init__(
        self,
        module: Module,
        inverters: list[Inverter],
        inverter_count: int,
        module_count: int,
        address: str,
        plant_id: str,  # "numero da instalacao" for plants licensed with CEMIG
        classe: str,
        din_padrao: int,
        din_geral: int,
        subgrupo: str,
        coordenadas: list[float],
        inv_boolean: int,
        structural_type: str,
        concessionaria: str,
    ):
        self.module = module
        self.inverters = inverters
        self.inverter_count = np.array(
            inverter_count
        )  # lista com quantidade de cada um dos inverters
        self.module_count = int(module_count)
        self.address = address
        self.plant_id = plant_id
        self.classe = classe
        self.din_padrao = float(din_padrao)
        self.din_geral = float(din_geral)
        self.subgrupo = subgrupo
        self.coordenadas = coordenadas
        self.inv_boolean = int(inv_boolean)  # 0 para inv. central e 1 para micro
        self.structural_type = structural_type
        self.concessionaria = concessionaria

        self.validacao_de_dados()

        self.pv_strings = self.get_strings_usina()

    def validacao_de_dados(self):
        """
        Valida os dados de entrada da classe Usina.
        Caso haja alguma inconsistência durante a declaração do objeto, um erro é disparado.
        """
        if self.inv_boolean not in [0, 1, 2]:  # verificando inv_boolean
            raise Exception('"inv_boolean" nao esta entre 0 e 2.')
        if len(self.inverters) != len(
            self.inverter_count
        ):  # verificando se as listas possuem a mesma dimensão
            raise Exception(
                "Lista com numero de inverters incompativel com a lista de inverters."
            )

    def get_strings_usina(self):
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
                module_count_inv = 0  # quantidade de módulos alocados ao inv atual
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
                    PVString(self.modulo, module_count_string_atual, inv)
                )
            pv_strings += pv_strings_inv_atual

        # Validação dos cálculos:
        soma_modulos = (
            0  # declaração da variável de somatório dos módulos em todas strings
        )
        for string in pv_strings:
            soma_modulos += string.module_count
        if (
            soma_modulos != self.module_count
        ):  # se a soma dos módulos nas strings for diferente do total de módulos na usina
            raise Exception("Inconsistencia ao distribuir as strings do sistema.")

        return pv_strings

    def get_pv_strings_diferentes(self):
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

    def compare_pv_string(self, index_pv_string_1, index_pv_string_2):
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

    def get_inverter_count_total(self):
        return np.sum(self.inverter_count)

    def get_cabeamento_por_polo(self):
        return 50 + 2 * self.module_count

    def get_numero_total_strings(self):
        numero_strings = 0
        for i, inv in enumerate(self.inverters):
            numero_strings += int(inv.string_count) * int(self.inverter_count[i])
        return numero_strings

    def get_modulos_impares(self):
        """
        Verifica se a quantidade de módulos é ímpar ou não.
        """
        if int(self.module_count) % self.get_numero_total_strings() != 0:
            modulos_impares = True
        else:
            modulos_impares = False
        return modulos_impares

    def get_potencia_ideal(self):
        """
        Calcula e retorna a potência ideal de toda usina.
        """
        return self.module_count * self.modulo.potencia

    def get_potencia_real(self, T_ref):
        """
        Calcula e retorna a potência real de toda usina.
        """
        p_real = self.get_potencia_ideal() * (1 - (T_ref * self.modulo.ppt / 100))
        return p_real

    def get_potencia_inverters(self):
        """
        Calcula e retorna a potência total dos inverters de toda a usina.
        """
        p_total_inverters = 0
        for i, inv in enumerate(self.inverters):
            p_total_inverters += inv.p_ca_nom * self.inverter_count[i]  # em W
        return p_total_inverters

    def get_potencia_modulos(self):
        """
        Calcula e retorna a potência total de todos módulos da usina.
        """
        return self.modulo.potencia * self.module_count  # em Wp

    def get_potencia_ativa(self):
        """
        Calcula e retorna a potência ativa da usina.
        """
        pot_modulos = self.get_potencia_modulos()
        pot_invs = self.get_potencia_inverters()
        if pot_modulos <= pot_invs:
            return pot_modulos
        else:
            return pot_invs

    def is_sup(self):
        if self.get_potencia_ativa() > 10000:
            return True
        else:
            return False

    def dividir_paineis_por_inv(self):
        """
        Retorna lista com número de painéis para cada inversor.
        """
        lista_paineis_por_inv = np.array([])  # inicializando a lista
        for i, inv in enumerate(self.inverters):
            qte_paineis_atual = (
                self.module_count
                * (inv.p_ca_nom / self.get_potencia_inverters())
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

    def get_corrente_maxima_invs(self, inv_id=None):
        if inv_id == None:  # caso seja micro ou somente 1 inv. central
            corrente_max = 0
            for i, inv in enumerate(self.inverters):
                corrente_max += inv.i_ca_max * self.inverter_count[i]
        else:  # se houver mais de um inv. central
            corrente_max = self.inverters[inv_id].i_ca_max
        return corrente_max

    def get_lista_din_usina(self):
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

    def get_area_paineis(self):
        return self.module_count * self.modulo.area


class PVString:
    """
    String fotovoltaica.
    Para efeito de modelagem computacional, o micro inversor será modelado como um inversor de string única.
    """

    def __init__(self, modulo, module_count, inversor):
        self.modulo = modulo
        self.module_count = int(module_count)
        self.inversor = inversor

    def get_v_oc(self):
        """
        Calcula e retorna a tensão de circuito aberto (V) da string
        """
        self.v_oc = self.modulo.v_oc * self.module_count
        return self.v_oc

    def get_v_max(self):
        """
        Calcula a tensão máxima (V) da string
        """
        self.v_max = self.modulo.v_max * self.module_count
        return self.v_max

    def get_i_sc(self):
        """
        Retorna a corrente de curto circuito (A) da string
        """
        return float(self.modulo.i_sc)

    def get_i_max(self):
        """
        Retorna a corrente máxima (A) da string
        """
        return float(self.modulo.i_max)

    def get_potencia_ideal(self):
        """
        Retorna a potência ideal da string
        """
        return self.module_count * self.modulo.potencia

    def get_potencia_real(self, T_ref):
        """
        Retorna a potência real da string
        """
        p_real = self.get_potencia_ideal() * (1 - (T_ref * self.modulo.ppt / 100))
        return p_real
