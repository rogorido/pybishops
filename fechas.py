#!/usr/bin/env python
# -*- coding: utf-8 -*-

import utils

class Fechas:
    """Clase para gestionar el lío de las fechas."""

    def __init__(self, fecha):
        fecha = fecha.split(' - ')
        inicio = fecha[0].strip()
        fin = fecha[1].strip()

        self.inicio = self.__crearFecha(inicio)
        self.fin = self.__crearFecha(fin)

    def __crearFecha(self, fecha):
        """Extraemos lo que sería la fecha para construir una string
        de fecha. Realmente hay que hacerlo de forma casuística."""

        fechatramos = fecha.split(' ')

        if fechatramos[0].isdigit() and len(fechatramos[0]) < 3:
            # esto sería que la fecha empieza por un día
            # y por tanto hay día, mes, año
            mes = utils.meses.index(fechatramos[1]) + 1
            temporal = '{}-{}-{}'.format(fechatramos[2], mes, fechatramos[0])
        elif fechatramos[0].isdigit() and len(fechatramos[0]) >= 3:
            # solo hay un año, puede ser <1000!
            temporal = '{}-01-01'.format(fechatramos[0])
        elif fechatramos[0].isalpha():
            # es un mes
            mes = utils.meses.index(fechatramos[0]) + 1
            temporal = '{}-{}-01'.format(fechatramos[1], mes)
        print(temporal)
        return temporal
