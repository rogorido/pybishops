#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2

meses = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
         'Aug', 'Sep', 'Oct', 'Nov', 'Dec')

motivos = ('Died', 'Resigned', 'Appointed', 'Retired', 'Succeeded',
           'Confirmed')

# ponemos este orden porque luego uso un for 
# en el que uso break con el primero que encuentra
cargos = ('Archbishop (Personal Title)', 'Coadjutor Archbishop',
          'Archbishop', 'Apostolic Administrator', 'Administrator',
          'Auxiliary Bishop', 'Coadjutor Bishop', 'Bishop', 'Cardinal-Priest',
          'Cardinal', 'Prelate')


def listaOrdenes():
    try:
        conn = psycopg2.connect("dbname='dominicos' user='igor' host='localhost'")
        cur = conn.cursor()
    except:
        print("I am unable to connect to the database")

    cur.execute("""SELECT order_id, order_acronym FROM religious_orders
    ORDER BY length(order_acronym) DESC""")

    rows = cur.fetchall()

    acronimos = []
    diccionario = {}

    for row in rows:
        acronimos.append(row[1])
        diccionario[row[1]] = row[0]

    return acronimos, diccionario
