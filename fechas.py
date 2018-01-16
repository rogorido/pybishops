#!/usr/bin/env python
# -*- coding: utf-8 -*-

import utils


class Fechas:
    """Clase para gestionar el lío de las fechas."""

    def __init__(self, fecha):
        fecha = fecha.split(' - ')
        inicio = fecha[0].strip()
        fin = fecha[1].strip()

        self.nombramiento = None
        self.destinoboolean = False
        self.motivofin = None

        if len(inicio) > 0:
            self.inicio = self.__crearFecha(inicio)
        else:
            self.inicio = None
            
        if len(fin) > 0:
            self.fin = self.__crearFecha(fin)
            self.motivofin = self.__extraerMotivo(fin)
        else:
            self.fin = None
            self.motivofin = None
            
    def __crearFecha(self, fecha):
        """Extraemos lo que sería la fecha para construir una string
        de fecha. Realmente hay que hacerlo de forma casuística."""

        fechatramos = fecha.split(' ')

        # aquí hay un problema: a veces aparece 'Did not take effect'
        if fechatramos[0] == 'Did':
            self.motivofin = 'Did not take effect'
            return None

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
        return temporal

    def __extraerMotivo(self, cadena):
        """Extraemos el motivo del fin/inicio, etc."""

        # en los casos de 'Did not take effect' este motivofin
        # ya está puesto por lo que salimos...
        if self.motivofin is not None:
            return self.motivofin

        motivo = None
        for m in utils.motivos:
            if m in cadena:
                motivo = m

        # en el caso de Appointed podemos extraer el nombramiento...
        if motivo == 'Appointed' or motivo == 'Succeeded' or motivo == 'Confirmed':
            for c in utils.cargos:
                if c in cadena:
                    self.nombramiento = c
                    self.destinoboolean = True
                    break
                else:
                    self.nombramiento = None
                    
        return motivo
