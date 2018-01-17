#!/usr/bin/env python
# -*- coding: utf-8 -*-

import diocesis as d
import psycopg2
import sys
import argparse

# Analizamos si se ha pasado la opción -s que sirve
# solamente para simular sin más, sin meter los datos en la bd.
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--simular", help="Simular sin meter los datos",
                    action="store_false")
args = parser.parse_args()
if args.simular:
    print("Ejecutando con normalidad: metiendo en la bd")
else:
    print("Ejecutando en modo simulación")


def introducirDatos(diocesis, obispo):
    """Esta es la función general que introduce los datos en la bd.
    Se le pasa un int para la diócesis y un objeto Obispo."""
    
    sql = """INSERT INTO bishops.bishops_all(bishop_surname,
    bishop_name, diocese_id, order_id, date_nomination, date_end,
    reason_begin, reason_end, nomination, destination,
    affiliated, url) VALUES(%s);"""
    data = (obispo.nombre, obispo.apellido, diocesis,
            obispo.orden_id, obispo.fechainicio, obispo.fechafin,
            obispo.motivoinicio, obispo.motivofin, obispo.nombramiento,
            obispo.destino, obispo.afiliado, obispo.url)
    try:
        cur.execute(sql, data)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


# conectamos a la bd 
try:
    conn = psycopg2.connect("dbname='dominicos' user='igor' host='localhost'")
    cur = conn.cursor()
except:
    print("I am unable to connect to the database")

lista_diocesis = []
lista_diocesis.append('http://www.catholic-hierarchy.org/diocese/dr506.html')

for diocesis in lista_diocesis:
    tipos = ['d3', 'd7']
    for t in tipos:
        dioc = d.Diocesis(diocesis, t)
        bishops = dioc.getObispos()

        print('\nEstas son las órdenes\n---------------\n')
        for o in bishops:
            # en algunos casos el obispo es none porque realmente no
            # hay obispos!
            if o is not None:
                print(o.__dict__)


if args.simular:
    cur.close()
    conn.close()
