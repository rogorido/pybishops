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


# vamos a meter también el campo orden, aunque ya está lo de orden_id
# porque tengo el lío de O.F.M. Obs. que no aparece en la tabla y
# lo transformo a O.F.M. Conv. y no sé ahora mismo si no es un error...
def introducirDatos(diocesis, obispo):
    """Esta es la función general que introduce los datos en la bd.
    Se le pasa un int para la diócesis y un objeto Obispo."""
    
    sql = """INSERT INTO bishops.bishops_all(bishop_surname, bishop_name,
    diocese_id, religious_order, religious_order_id, date_nomination,
    date_end, reason_begin, reason_end, nomination, destination,
    affiliated, url) VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    data = (obispo.nombre, obispo.apellido, diocesis,
            obispo.orden, obispo.orden_id, obispo.fechainicio, obispo.fechafin,
            obispo.motivoinicio, obispo.motivofin, obispo.nombramiento,
            obispo.destino, obispo.afiliado, obispo.url,)
    
    try:
        cur.execute(sql, data)
        conn.commit()
        print('Introducido el obispo {} {}'.format(obispo.nombre,
                                                   obispo.apellido))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def extraerDiocesis():
    """Extraemos las diócesis de la bd."""

    cur.execute("""SELECT d.diocese_id, d.url_hierarchy FROM dioceses d WHERE
    diocese_id NOT IN (SELECT DISTINCT diocese_id FROM bishops_all)
    AND d.url_hierarchy IS NOT NULL LIMIT 3;""")
    rows = cur.fetchall()
    # lo metemos en un dict porque así metemos también la id!
    lista = {}
    for r in rows:
        lista[r[1]] = r[0]

    return lista

# conectamos a la bd 
try:
    conn = psycopg2.connect("dbname='dominicos' user='igor' host='localhost'")
    cur = conn.cursor()
except:
    print("I am unable to connect to the database")

lista_diocesis = extraerDiocesis()
#lista_diocesis.append('http://www.catholic-hierarchy.org/diocese/dr506.html')

for diocesis in lista_diocesis:
    tipos = ['d3', 'd7']
    for t in tipos:
        dioc = d.Diocesis(diocesis, t)
        bishops = dioc.getObispos()

        print('\nEstos son las datos de D{}-------'.format(lista_diocesis[diocesis]))
        for o in bishops:
            # en algunos casos el obispo es none porque realmente no
            # hay obispos!
            if o is not None:
                if args.simular:
                    introducirDatos(lista_diocesis[diocesis], o)
                else:
                    print(o.__dict__)


if args.simular:
    cur.close()
    conn.close()
