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
    try:
        conn = psycopg2.connect("dbname='dominicos' user='igor' host='localhost'")
        cur = conn.cursor()
    except:
        print("I am unable to connect to the database")
else:
    print("Ejecutando en modo simulación")

print('fin')

def introducirDatos(obispo):
    """Esta es la función general que introduce los datos en la bd.
    Se le pasa un objeto Obispo."""

    


dioc = d.Diocesis('http://www.catholic-hierarchy.org/diocese/dzamb.html',
                  'd3')

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
