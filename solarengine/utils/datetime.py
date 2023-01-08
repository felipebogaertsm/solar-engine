# -*- coding: utf-8 -*-
# Copyright © Felipe Bogaerts de Mattos
# Contact: me@felipebm.com


def get_mes_ano(numero, abreviado):
    """
    Returns the written name of the month of the year
    :param numero: Number of the month
    :param abreviado: Boolean that selects abbreviated month name or not
    :return: written name of the month
    """
    meses_do_ano = [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ]
    meses_abreviados = []
    if abreviado:
        for mes in meses_do_ano:
            meses_abreviados.append(mes[0:3])
        return meses_abreviados[numero]
    else:
        return meses_do_ano[numero]
