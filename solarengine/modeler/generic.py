# -*- coding: utf-8 -*-
# Copyright © Felipe Bogaerts de Mattos
# Contact: me@felipebm.com


class Brand:
    def __init__(self, name: str, model: list) -> None:
        """
        :param str name: Brand name
        :param str model: Model name
        """
        self.name = name
        self.model = model


class PhysicalProperties:
    def __init__(
        self,
        weight: float,
        width: float,
        height: float,
        depth: float,
    ) -> None:
        """
        :param float weight: Total weight (kg)
        :param float width: Width (mm)
        :param float height: Height (mm)
        :param float depth: Depth (mm)
        """
        self.weight = weight
        self.width = width
        self.height = height
        self.depth = depth

    @property
    def dimensions(self) -> tuple:
        return (self.width, self.height, self.depth)
