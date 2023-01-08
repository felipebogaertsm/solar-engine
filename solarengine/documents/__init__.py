# -*- coding: utf-8 -*-
# Copyright © Felipe Bogaerts de Mattos
# Contact: me@felipebm.com

from abc import ABC, abstractmethod


class Document(ABC):
    @abstractmethod
    def generate(self):
        pass
