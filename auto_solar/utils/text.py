# -*- coding: utf-8 -*-
# Copyright © Felipe Bogaerts de Mattos
# Contact: me@felipebm.com


def get_string_modelo_inversores(invs):
    """
    Retorna, em texto, todos modelos de inversor da usina, separados por vírgula
    """
    string = ""
    for inv in invs:
        string += inv.modelo
        string += ", "
    string = string[:-2]
    return string


def get_numero_ordinal_texto(numero_inteiro):
    """
    Converte número inteiro para texto do número em ordinal.
    Por exemplo: para um input '2', a função retorna 'segundo'
    """
    numero_inteiro = int(numero_inteiro)
    if numero_inteiro == 1:
        return "primeiro"
    elif numero_inteiro == 2:
        return "segundo"
    elif numero_inteiro == 3:
        return "terceiro"
    else:
        raise Exception("Numero ordinal nao identificado.")
