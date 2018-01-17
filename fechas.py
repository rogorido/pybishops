#!/usr/bin/env python
# -*- coding: utf-8 -*-

import utils


class Fechas:
    """Clase para gestionar el lío de las fechas. Los obispos afiliados
    tienen una estructura de fechas diferente."""

    def __init__(self, fecha, afiliado):

        self.nombramiento = None
        self.destinoboolean = False
        self.motivofin = None
        self.motivoinicio = None

        if afiliado:
            # los afiliados tienen varios datos que separan con ;
            # normalmente el único que interesa es el último
            fecha = fecha.split(';')[-1]
            # ahora dividimos esto para sacar la fecha...
            datos = fecha.split(':')
            self.motivoinicio = datos[0].strip()
            fecha = datos[1]

        if afiliado:
            fecha = fecha.split(' to ')
        else:
            fecha = fecha.split(' - ')
        inicio = fecha[0].strip()
        fin = fecha[1].strip()

        if len(inicio) > 0:
            self.inicio = self.__crearFecha(inicio)
            if not afiliado:
                # entiendo que en el caso de los afiliados ya está...
                self.motivoinicio = self.__extraerMotivo(inicio, 0)
        else:
            self.inicio = None
            
        if len(fin) > 0:
            self.fin = self.__crearFecha(fin)
            if not afiliado:
                # entiendo que en el caso de los afiliados no hay motivo?
                self.motivofin = self.__extraerMotivo(fin, 1)
        else:
            self.fin = None
            
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

    def __extraerMotivo(self, cadena, tipo):
        """Extraemos el motivo del fin/inicio, etc. Lo de tipo es 0/1,
        0 para inicio y 1 para fin."""

        # en los casos de 'Did not take effect' este motivofin
        # ya está puesto por lo que salimos...
        if tipo == 1 and self.motivofin is not None:
            return self.motivofin

        motivo = None
        for m in utils.motivos:
            if m in cadena:
                motivo = m

        # en el caso de Appointed podemos extraer el nombramiento...
        # esto solo vale cuando estamos extrayendo el motivofin
        if tipo == 1: 
            if motivo == 'Appointed' or motivo == 'Succeeded' or motivo == 'Confirmed':
                for c in utils.cargos:
                    if c in cadena:
                        self.nombramiento = c
                        self.destinoboolean = True
                        break
                    else:
                        self.nombramiento = None
                    
        return motivo
