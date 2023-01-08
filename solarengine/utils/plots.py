# -*- coding: utf-8 -*-
# Copyright © Felipe Bogaerts de Mattos
# Contact: me@felipebm.com

import matplotlib.pyplot as plt


def previsao_geracao_figura(P_modulo, n_modulos, irradiacao_mensal):
    """
    Salva as figuras de geração anual e mensal.
    :param P_modulo: Potência do módulo
    :param n_modulos: Quantidade de módulos
    :param irradiacao_mensal: Vetor com irradiação mensal no local
    :return: None
    """

    meses_ano_abreviados = []
    for i in range(12):
        meses_ano_abreviados.append(get_mes_ano(i, True))

    geracao_mensal = get_geracao_mensal(P_modulo, n_modulos, irradiacao_mensal)
    figura_geracao_mensal = plt.figure(figsize=(15, 8))
    plt.plot(meses_ano_abreviados, geracao_mensal, 0, 0)
    plt.ylabel("Energia gerada por mês (kWh)")
    plt.xlabel("Meses do ano")
    plt.grid()
    figura_geracao_mensal.savefig(
        "automacao/automacao_files/output/geracao_mensal.png"
    )
    figura_geracao_anual = plt.figure(figsize=(15, 8))
    anos = np.arange(0, 25)
    geracao_anual = get_geracao_anual(geracao_mensal, 25, 0.01)
    plt.grid()
    plt.bar(anos, geracao_anual)
    plt.ylabel("Energia gerada por ano (kWh)")
    plt.xlabel("Anos")
    figura_geracao_anual.savefig(
        "automacao/automacao_files/output/geracao_anual.png"
    )
