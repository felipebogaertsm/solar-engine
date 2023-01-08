# -*- coding: utf-8 -*-
# Copyright © Felipe Bogaerts de Mattos
# Contact: me@felipebm.com

import numpy as np


def get_irradiacao_mensal():
    return [
        5.55,
        5.84,
        4.83,
        4.22,
        3.54,
        3.37,
        3.53,
        4.27,
        4.55,
        4.87,
        4.75,
        5.45,
    ]


def get_available_din():
    return np.array([16, 20, 25, 32, 40, 50, 60, 63, 70, 100, 125, 150, 225])


def get_carga_instalada(din_padrao, classe):
    """
    Calcula a carga instalada na instalação. Utiliza dados da CEMIG, atualizados
    em 2020.
    """
    din_padrao = float(din_padrao)
    if classe == "Residencial Monofásico" or classe == "Comercial Monofásico":
        if 15 <= din_padrao <= 16:
            carga_instalada = 1.4
        elif din_padrao == 40:
            carga_instalada = 4
        elif 60 <= din_padrao <= 63:
            carga_instalada = 9
        elif din_padrao == 70:
            carga_instalada = 9
        else:
            raise Exception(
                "Disjuntor não reconhecido pela função de dimensionamento de carga instalada."
            )
    elif classe == "Residencial Bifásico" or classe == "Comercial Bifásico":
        if 60 <= din_padrao <= 63 or din_padrao == 50:
            carga_instalada = 14
        elif 70 <= din_padrao <= 80:
            carga_instalada = 18
        elif din_padrao > 80:
            carga_instalada = 18
        else:
            raise Exception(
                "Disjuntor não reconhecido pela função de dimensionamento de carga instalada."
            )
    elif (
        classe == "Residencial Trifásico"
        or classe == "Comercial Trifásico"
        or classe == "Industrial Trifásico"
    ):
        if 40 <= din_padrao < 60:
            carga_instalada = 14
        elif 60 <= din_padrao <= 63:
            carga_instalada = 20
        elif 70 <= din_padrao <= 80:
            carga_instalada = 25
        elif 80 < din_padrao <= 100:
            carga_instalada = 36
        elif 100 < din_padrao <= 125:
            carga_instalada = 45
        elif 125 < din_padrao <= 150:
            carga_instalada = 55
        elif 150 < din_padrao <= 200:
            carga_instalada = 70
        elif 200 < din_padrao <= 225:
            carga_instalada = 80
        elif 225 < din_padrao <= 250:
            carga_instalada = 90
        else:
            raise Exception(
                "Disjuntor não reconhecido pela função de dimensionamento de carga instalada."
            )
    return carga_instalada


def calculo_disjuntor(corrente_max, disjuntores, sf):
    """
    Calcula o disjuntor adequado de acordo com a corrente máxima, o fator de
    segurança e a lista de disjuntores disponíveis.
    :return: Disjuntor adequado a operar
    """
    # Fonte:
    # https://www.solaredge.com/sites/default/files/determining-the-circuit-breaker-size-for-three-phase-inverters.pdf
    disjuntores_disponiveis = disjuntores[
        np.where(disjuntores >= corrente_max * sf)
    ]
    try:
        return disjuntores_disponiveis[0]
    except:
        print(
            f"Erro: disjuntores não são compatíveis com a corrente do projeto "
            f"de {corrente_max * sf:.2f} A."
        )


def get_geracao_mensal(P_modulo, n_modulos, irradiacao_mensal):
    """
    Retorna vetor numpy com a geração mensal da usina no primeiro ano de
    funcionamento.
    """
    try:
        P_modulo = float(P_modulo)
        n_modulos = int(n_modulos)
    except ValueError:  # se não conseguir converter para float e int acima
        raise Exception("Could not convert string to numerical value.")
    assert (
        len(irradiacao_mensal) == 12
    ), "Irradiação mensal deve ser lista de comprimento 12."
    geracao_mensal = np.zeros(
        np.size(irradiacao_mensal)
    )  # inicializando vetor de geração com 12 elementos 0s
    PR = 0.78  # performance ratio
    for i in range(np.size(irradiacao_mensal)):  # iterando meses do ano
        geracao_mensal[i] = (
            irradiacao_mensal[i]
            * float(P_modulo)
            * 30
            * PR
            * int(n_modulos)
            * 1e-3
        )  # em kWh
    return geracao_mensal


def get_geracao_anual(geracao_mensal, anos, taxa):
    geracao_anual = np.zeros(anos)  # inicializando vetor com 0s
    geracao_anual[0] = np.sum(geracao_mensal)
    for i in range(1, anos):
        geracao_anual[i] = geracao_anual[i - 1] * (1 - taxa)  # em kWh
    return geracao_anual


def get_geracao_mensal_media(geracao_mensal):
    return np.mean(geracao_mensal)


def get_irradiacao_mensal(orientacao="N"):
    """
    Calcula e retorna um vetor numpy com as irradiações mensais em kW/m-m-dia
    :param orientacao: orientação das placas, N, S, LO (Leste/Oeste) ou H (horizontal)
    :return: numpy array com as irradiações nos 12 meses
    """
    irradiacao_mensal_base = np.array(
        [
            5.55,
            5.84,
            4.83,
            4.22,
            3.54,
            3.37,
            3.53,
            4.27,
            4.55,
            4.87,
            4.75,
            5.45,
        ]
    )  # irradiação base usada para orientação ao Norte

    if orientacao == "N":  # inclinação Norte
        irradiacao_mensal = irradiacao_mensal_base
    elif (
        orientacao == "NE" or orientacao == "NO"
    ):  # inclinação Nordeste e Noroeste
        irradiacao_mensal = irradiacao_mensal_base * (100 - 4) / 100
    elif orientacao == "LO":  # inclinação Leste/Oeste
        irradiacao_mensal = irradiacao_mensal_base * (100 - 8.84) / 100
    elif orientacao == "S":  # inclinação Sul
        irradiacao_mensal = irradiacao_mensal_base * (100 - 26.31) / 100
    elif (
        orientacao == "SE" or orientacao == "SO"
    ):  # inclinação Sudeste e Sudoeste
        irradiacao_mensal = irradiacao_mensal_base * (100 - 20) / 100
    elif orientacao == "H":  # inclinação horizontal
        irradiacao_mensal = irradiacao_mensal_base * (100 - 4.63) / 100
    else:
        raise Exception("Orientacao dos paineis nao identificada.")

    return irradiacao_mensal
