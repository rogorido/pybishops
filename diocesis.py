#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import obispo


class Diocesis:
    """Esto es la clase que controla las diócesis"""

    def __init__(self, url, tipo):
        self.obispos = []
        self.url = url
        self.tipo = tipo
        if tipo == "d3":  # esto son los normales
            afiliado = False
        else:
            afiliado = True

        pagina = requests.get(url)
        # tenemos que usar html5lib como parser porque es menos
        # pejiguero que el que viene por defecto. El problema son las
        # listas que no están bien en la página.
        soup = BeautifulSoup(pagina.content, 'html5lib')
        obisposhtml = soup.find("div", attrs={"id":tipo})

        listaobisposenbruto = obisposhtml.find("ul")
        print('Diócesis {} tiene {} obispos'.format(soup.title.text,
                                                    len(listaobisposenbruto)))

        self.listaobispos = listaobisposenbruto.find_all("li")
        for o in self.listaobispos:
            self.anadirObispos(o, afiliado)

    def anadirObispos(self, o, afiliado):
        """El parámetro o es el string en html"""
        nuevoob = obispo.Obispo(o, afiliado)
        self.obispos.append(nuevoob)

    def totalObispos(self):
        print(len(self.obispos))

    def getObispos(self):
        return self.obispos
    
