#!/usr/bin/env python
# -*- coding: utf-8 -*-

import utils
import fechas as f


class Obispo:
    """Esto es una clase que crea obispos y devuelve sus datos."""

    def __init__(self, creador):
        """El string creador es lo que viene de BeautifulSoup con
        el formateado de html."""

        # realmente el primer <a> es el nombre, aunque esto así hay
        # que tener cuidado. Lo guardamos como html porque nos permite sacar
        # lo que está en negrita que es el apellido. 
        nombrehtml = creador.a
        self.nombre = nombrehtml.text
        apellidohtml = nombrehtml.b
        self.apellido = apellidohtml.text
        # quitamos el apellido del nombre para tener el nombre final.
        self.nombre = self.nombre.replace(self.apellido, '')

        self.cadena = creador.text

        self.__extractOrder()
        self.__extractFechas()
        
    def getName(self):
        return self.nombre

    def getSurname(self):
        return self.apellido

    def getOrder(self):
        return self.orden

    def mostrarCadena(self):
        print(self.cadena)

    def __extractOrder(self):
        for n in utils.ordenes:
            if n in self.cadena:
                self.orden = n
                break
            else:
                self.orden = None

    def __extractFechas(self):
        # TODO: a veces hay más de unos paréntesis!!
        # extraemos las fechas de los paréntesis
        fechas = self.cadena[self.cadena.index("(") +
                             1:self.cadena.rindex(")")]

        # las dividimos. Es importante usar ' - ' porque a veces
        # hay un guión en esa cadena. Cuidado con esto.
        fecha = f.Fechas(fechas)
        
