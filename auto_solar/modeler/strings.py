# -*- coding: utf-8 -*-
# Copyright © Felipe Bogaerts de Mattos
# Contact: me@felipebm.com

from .inverter import Inverter
from .module import Module


class PVString:
    """
    String fotovoltaica.
    Para efeito de modelagem computacional, o micro inverter será modelado
    como um inverter de string única.
    """

    def __init__(
        self,
        module: Module,
        module_count: int,
        inverter: Inverter,
    ) -> None:
        self.module = module
        self.module_count = int(module_count)
        self.inverter = inverter

    @property
    def v_oc(self) -> float:
        """
        Calcula e retorna a tensão de circuito aberto (V) da string
        """
        return self.module.v_oc * self.module_count

    @property
    def v_max(self) -> float:
        """
        Calcula a tensão máxima (V) da string
        """
        self.v_max = self.module.v_max * self.module_count
        return self.v_max

    @property
    def i_sc(self) -> float:
        """
        Retorna a corrente de curto circuito (A) da string
        """
        return float(self.module.i_sc)

    @property
    def i_max(self) -> float:
        """
        Retorna a corrente máxima (A) da string
        """
        return float(self.module.i_max)

    @property
    def power_output_ideal(self) -> float:
        """
        Retorna a potência ideal da string
        """
        return self.module_count * self.module.potencia

    @property
    def power_output_real(self, T_ref: float) -> float:
        """
        Retorna a potência real da string
        """
        return self.power_output_ideal() * (
            1 - (T_ref * self.module.ppt / 100)
        )
