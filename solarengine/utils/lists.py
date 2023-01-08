# -*- coding: utf-8 -*-
# Copyright © Felipe Bogaerts de Mattos
# Contact: me@felipebm.com


def get_index_list(lista, codigo):
    """
    Pega o índice da coluna de clientes onde o código do cliente se encontra.
    :param lista: Lista com o código dos clientes
    :param codigo: String com o código do cliente desejado
    :return: Int correspondente a linha com as infos do cliente desejado
    """
    i = 0
    row_index = 0
    for string in lista:
        i = i + 1
        if string == codigo:
            row_index = i
            break
    return row_index
