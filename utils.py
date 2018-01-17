#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2

# ponemos lo de Obs. antes de OFM porque tengo un for
# en el que uso break con el primero que encuentra
ordenes = ('O.P.', 'O.S.M.', 'C.R.S.A.', 'C.R.M.', 'O.F.M. Obs.',
           'O.F.M. Conv.', 'O.F.M. Cap.', 'O.F.M.', 'O.S.B', 'O.M.', 'O.Cist.',
           'O.Praem.', 'C.R.L.', 'C.S.Ch.', 'O.S.H.', 'T.O.R.',
           'O.S.Io.Hieros.', 'O.Ss.C.A.', 'S.J', 'O.S.',
           'C.R.')

meses = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
         'Aug', 'Sep', 'Oct', 'Nov', 'Dec')

motivos = ('Died', 'Resigned', 'Appointed', 'Retired', 'Succeeded',
           'Confirmed')

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
