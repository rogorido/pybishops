#!/usr/bin/env python
# -*- coding: utf-8 -*-

import diocesis as d

dioc = d.Diocesis('http://www.catholic-hierarchy.org/diocese/drace.html',
                  'd3')

#dioc = d.Diocesis('http://www.catholic-hierarchy.org/diocese/dr506.html', 'd3')

bishops = dioc.getObispos()

print('\nEstas son las órdenes\n---------------\n')
for o in bishops:
    if o.getOrder() is not None:
        print(o.getName())
        print(o.getOrder())


