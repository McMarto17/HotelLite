#coding=utf-8

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os, funcionescli

import variables


def basico(pdf):
    """
    Se define el formato de la factura
    :return: Retorna la factura
    """
    try:
        factura = pdf
        texto_bienvenida = 'Bienvenido a nuestro hotel'
        cif = 'CIF:00000000A'
        factura.drawImage('./img/logohotel.png', 475, 675, width=64, height=64)
        factura.setFont('Helvetica-Bold', size=16)
        factura.drawString(250, 780, 'HOTEL LITE')
        factura.setFont('Times-Italic', size=10)
        factura.drawString(240, 765, texto_bienvenida)
        factura.drawString(260, 755, cif)
        factura.line(50, 670, 540, 670)
        texto_pie = 'Hotel Lite, Tlfo = 986291132 e-mail = info@hotellite.com'
        factura.setFont('Times-Italic', size=8)
        factura.drawString(170, 40, texto_pie)
        factura.setFont('Helvetica-Bold', size=10)
        page_num = factura.getPageNumber()
        text = "%s" % page_num
        factura.drawString(550, 25, text)
        factura.line(50, 50, 540, 50)
        return factura
    except Exception as e:
        print(e)
        print('Error en basico')


def factura(datos_factura):
    """
    Se insertan todos los tipos de datos dentro de la factura
    :param datos_factura: Lista que contiene todos los datos de la factura
    :return: Void
    """
    try:
        pdf = canvas.Canvas('factura.pdf', pagesize=A4)
        factura = basico(pdf)
        factura.setTitle('FACTURA')

        factura.setFont('Helvetica-Bold', size=8)
        numero_factura = 'Número de Factura:'
        factura.drawString(50, 735, numero_factura)
        factura.setFont('Helvetica', size=8)
        factura.drawString(140, 735, str(datos_factura[0]))

        factura.setFont('Helvetica-Bold', size=8)
        fecha_factura = 'Fecha Factura:'
        factura.drawString(300, 735, fecha_factura)
        factura.setFont('Helvetica', size=8)
        factura.drawString(360, 735, str(datos_factura[4]))

        factura.setFont('Helvetica-Bold', size=8)
        dni_cliente = 'DNI CLIENTE:'
        factura.drawString(50, 710, dni_cliente)
        factura.setFont('Helvetica', size=8)
        factura.drawString(120, 710, str(datos_factura[2]))

        factura.setFont('Helvetica-Bold', size=8)
        numero_habitacion = 'Nº de Habitación:'
        factura.drawString(300, 710, numero_habitacion)
        factura.setFont('Helvetica', size=8)
        factura.drawString(380, 710, str(datos_factura[3]))
        nombre_y_apellidos = funcionescli.apelnomfac(datos_factura[2])

        factura.setFont('Helvetica-Bold', size=8)
        apellidos_cliente = 'APELLIDOS:'

        factura.drawString(50, 680, apellidos_cliente)
        factura.setFont('Helvetica', size=8)
        factura.drawString(120, 680, nombre_y_apellidos[0])
        factura.setFont('Helvetica-Bold', size=8)
        nombre_cliente = 'NOMBRE:'
        factura.drawString(300, 680, nombre_cliente)
        factura.setFont('Helvetica', size=8)
        factura.drawString(350, 680, nombre_y_apellidos[1])

        alojamiento = ['Noches', str(datos_factura[1]), str(datos_factura[5]),variables.strPrecioTotal]
        cabecera = ['CONCEPTO', 'UNIDADES', 'PRECIO/UNIDAD', 'TOTAL']

        x = 75
        for i in range(0, 4):
            factura.setFont('Helvetica-Bold', size=10)
            factura.drawString(x, 655, cabecera[i])
            factura.setFont('Helvetica', size=8)
            factura.drawString(x, 625, alojamiento[i])
            x += 130

        y = 600
        for registro in variables.listaServicios:
            x = 75
            for i in range(1, 3):
                factura.setFont('Helvetica', size=8)
                factura.drawString(x, y, str(registro[i]))
                x += 390
            y -= 30

        y = 600
        for registro in variables.listaServicios:
            x = 465
            for i in range(2, 3):
                factura.setFont('Helvetica', size=8)
                factura.drawString(x, y, str(registro[i])+"€")

            y -= 30

        y = 600
        for registro in variables.listaServicios:
            x = 335
            for i in range(2, 3):
                factura.setFont('Helvetica', size=8)
                factura.drawString(x, y, str(registro[i])+"€")
                x += 360
            y -= 30

        factura.line(50, 85, 540, 85)

        factura.line(50, 645, 540, 645)
        facturaTotal = ['SUBTOTAL:','IVA%:','TOTAL:']
        preciosFacturaTotal = [variables.lblSubtotalFactura.get_text(), variables.lblIvaFactura.get_text(),variables.lblTotalFactura.get_text()]

        y = 75
        for i in range(0, 3):
            factura.setFont('Helvetica', size=8)
            factura.drawRightString(440, y, facturaTotal[i])
            y -= 20

        y = 75
        for i in range(0, 3):
            factura.setFont('Helvetica', size=8)
            factura.drawRightString(490, y, preciosFacturaTotal[i])
            y -= 20


        factura.showPage()
        factura.save()
        directorio_actual = os.getcwd()
        os.system('/usr/bin/xdg-open ' + directorio_actual + '/prueba.pdf')
    except Exception as e:
        print(e)
        print('Error en factura')

def clientes(listclientes):
    try:
        pdf = canvas.Canvas('clientes.pdf', pagesize=A4)
        factura = basico(pdf)
        factura.setTitle('LISTA CLIENTES')

        cabecera = ['DNI','APELIDOS','NOME','DATA ALTA']

        x = 75
        for i in range(0, 4):
            factura.setFont('Helvetica-Bold', size=10)
            factura.drawString(x, 655, cabecera[i])
            x += 130
        y = 620
        for registro in listclientes:
            x = 75
            if y <= 50:
                y = 780
                pdf.showPage()
                page_num = factura.getPageNumber()
                text = "%s" % page_num
                factura.drawString(550, 25, text)
                x = 75
                for i in range(0, 4):
                    factura.setFont('Helvetica-Bold', size=10)
                    factura.drawString(x, 780, cabecera[i])
                    x += 130
                #factura.line(50,800,540,800)
                factura.line(50,770,540,770)
                factura.line(50,50,540,50)

            for i in range(0, 4):
                factura.setFont('Helvetica', size=8)
                if(i == 0):
                    factura.drawString(x, y, str("******"+registro[i][6]+registro[i][7]+registro[i][8]))
                else:
                    factura.drawString(x, y, str(registro[i]))
                x += 130
            y -= 30

        factura.showPage()
        factura.save()
        directorio_actual = os.getcwd()
        os.system('/usr/bin/xdg-open ' + directorio_actual + '/clientes.pdf')

    except Exception as e:
        print(e)
        print('Error en factura')


