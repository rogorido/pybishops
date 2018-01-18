#!/usr/bin/env python
# -*- coding: utf-8 -*-

import utils
import fechas as f


class Obispo:
    """Esto es una clase que crea obispos y devuelve sus datos.

    Las variables son:
    url: del obispo 
    nombre
    apellido
    orden: acrónimo de la orden
    orden_id: id de la orden
    fechainicio
    fechafin
    nombramiento
    destino: si es trasladado, a donde (href!)
    motivoinicio: el motivo del inicio (appointed casi siempre).
    motivofin: el motivo del fin.
    afiliado: eso de affiliated...
    """

    # esto realmente es muy cutre porque va a hacer esta
    # consulta casda vez que cree (sicher?) un bishop...
    # pero es que no se me ocurre un sistema mejo...
    acronimos, diccionario = utils.listaOrdenes()

    def __new__(cls, creador, afiliado):
        """Eso es muy importante. Cuando no hay obispos aparece None y
        entonces hay que abortar la creación de la clase. Esto de __new__
        se ejecuta antes de __init__."""
        # metemos el texto inicial en una variable 
        cadena = creador.text

        if cadena == "None\n":
            return None
        else:
            return super(Obispo, cls).__new__(cls)
        
    def __init__(self, creador, afiliado):
        """El string creador es lo que viene de BeautifulSoup con
        el formateado de html. Afiliado es bool para saber qué tipo
        de obispo es."""

        self.creador = creador
        # metemos el texto inicial en una variable 
        self.cadena = creador.text

        # realmente el primer <a> es el nombre, aunque esto así hay
        # que tener cuidado. Lo guardamos como html porque nos permite sacar
        # lo que está en negrita que es el apellido. 
        nombrehtml = creador.a
        # extraemos la url del obispo 
        self.url = nombrehtml['href']

        # luego el nombre, etc. 
        self.nombre = nombrehtml.text.strip()
        apellidohtml = nombrehtml.b
        self.apellido = apellidohtml.text.strip()

        # esto es un poco cutre: a veces en el nombre/apellido
        # hay paréntesis y eso crea un lío cuando luego queremos
        # extraer los datos de las fechas. Con esto quitamos el nombre
        # de la cadena esa. Un poco primitivo... habría que hacer un check
        # de cuántos paréntesis hay, etc. 
        self.cadena = self.cadena.replace(self.nombre, '')
        
        # quitamos el apellido del nombre para tener el nombre final.
        self.nombre = self.nombre.replace(self.apellido, '')

        # inicializo algunas variables
        self.fechainicio, self.fechafin, self.orden_id = None, None, None
        self.orden, self.destino, self.nombramiento = None, None, None
        self.afiliado = afiliado

        self.__extractOrder()
        self.__extractFechas()
        
    def mostrarCadena(self):
        print(self.cadena)

    def __extractOrder(self):
        # entiendo que convetnuales y observantes es lo mismo, pero no hay
        # el acrónimo O.F.M. Obs. por lo que hago este truquito
        busqueda = self.cadena
        if 'O.F.M. Obs.' in busqueda:
            busqueda = 'O.F.M. Conv.'
        for n in self.acronimos:
            if n in busqueda:
                self.orden = n
                self.orden_id = self.diccionario[n]
                break

    def __extractFechas(self):
        # TODO: a veces hay más de unos paréntesis!!
        # extraemos las fechas de los paréntesis. En algunos casos
        # no hay nada, por lo que lo comprobamos...
        try:
            fechas = self.cadena[self.cadena.index("(") +
                                 1:self.cadena.rindex(")")]

            # las dividimos. Es importante usar ' - ' porque a veces
            # hay un guión en esa cadena. Cuidado con esto.
            fecha = f.Fechas(fechas, self.afiliado)
            self.fechainicio = fecha.inicio
            self.fechafin = fecha.final
            self.motivoinicio = fecha.motivoinicio
            self.motivofin = fecha.motivofin
            self.nombramiento = fecha.nombramiento

            # si fecha.destino es true, quiere decir que el tipo se mueve
            # y por tanto intentamos extraer el último anchor que suele ser
            # la referencia a adonde se mueve. 
            if fecha.destinoboolean:
                anchor = self.creador.find_all('a')[-1]
                self.destino = anchor['href']
        except:
            self.fechainicio = None
            self.fechafin = None
            self.motivoinicio = None
            self.motivofin = None
            self.nombramiento = None
