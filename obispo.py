#!/usr/bin/env python
# -*- coding: utf-8 -*-

import utils
import fechas as f


class Obispo:
    """Esto es una clase que crea obispos y devuelve sus datos.

    Las variables son:
    nombre
    apellido
    orden
    fechainicio
    fechafin
    nombramiento
    destino: si es trasladado, a donde (href!)
    motivo: el motivo del fin.
    """

    def __init__(self, creador):
        """El string creador es lo que viene de BeautifulSoup con
        el formateado de html."""

        self.creador = creador
        # realmente el primer <a> es el nombre, aunque esto así hay
        # que tener cuidado. Lo guardamos como html porque nos permite sacar
        # lo que está en negrita que es el apellido. 
        nombrehtml = creador.a
        self.nombre = nombrehtml.text
        apellidohtml = nombrehtml.b
        self.apellido = apellidohtml.text

        # metemos el texto inicial en una variable 
        self.cadena = creador.text
        # esto es un poco cutre: a veces en el nombre/apellido
        # hay paréntesis y eso crea un lío cuando luego queremos
        # extraer los datos de las fechas. Con esto quitamos el nombre
        # de la cadena esa. Un poco primitivo... habría que hacer un check
        # de cuántos paréntesis hay, etc. 
        self.cadena = self.cadena.replace(self.nombre, '')
        
        # quitamos el apellido del nombre para tener el nombre final.
        self.nombre = self.nombre.replace(self.apellido, '')

        # inicializo algunas variables
        self.fechainicio, self.fechafin = None, None
        self.orden, self.destino, self.nombramiento = None, None, None

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

    def __extractFechas(self):
        # TODO: a veces hay más de unos paréntesis!!
        # extraemos las fechas de los paréntesis
        fechas = self.cadena[self.cadena.index("(") +
                             1:self.cadena.rindex(")")]

        # las dividimos. Es importante usar ' - ' porque a veces
        # hay un guión en esa cadena. Cuidado con esto.
        fecha = f.Fechas(fechas)
        self.motivofin = fecha.motivofin
        self.nombramiento = fecha.nombramiento

        # si fecha.destino es true, quiere decir que el tipo se mueve
        # y por tanto intentamos extraer el último anchor que suele ser
        # la referencia a adonde se mueve. 
        if fecha.destinoboolean:
            anchor = self.creador.find_all('a')[-1]
            self.destino = anchor['href']
