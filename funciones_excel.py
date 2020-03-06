#coding=utf-8

import datetime
from xlrd.sheet import Cell
import xlrd


def formatear_fecha_excel(celda):
    """
    Cambia el formato de la fecha del fichero excel
    :param celda: Posicion de la fecha en el fichero
    :return: Retorna la fecha formateada
    """
    archivo_excel = xlrd.open_workbook("clientes.xls")
    fecha_formateada = datetime.datetime(*xlrd.xldate_as_tuple(celda.value, archivo_excel.datemode))
    return fecha_formateada.strftime('%d/%m/%Y')
