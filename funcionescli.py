#coding=utf-8
"""
Created on Feb 19, 2020

@author: martinca
"""
from xlrd import sheet
import conexion
import sqlite3
import funciones_excel
import variables

def limpiarentry(fila):
    """
    Con este método vaciamos los datos introducidos en los entry
    de entrada de datos.
    :param fila: fila que vamos a limpiar de datos
    :return: Void
    """
    variables.menslabel[1].set_text('')
    for i in range(len(fila)):
        fila[i].set_text('')

def validoDNI(dni):
    """
    Método con el que realizamos las coprobaciones necesarias al dato introducido
    como DNI, comprobando su validez.
    :param dni: dato recogido para validar.
    :return: False
    """
    try:
        tabla = "TRWAGMYFPDXBNJZSQVHLCKE"   #letras del dni, es estandar
        dig_ext = "XYZ"                     #tabla letras extranjeroreemp_
        reemp_dig_ext = {'X':'0', 'Y':'1', 'Z':'2'}
        numeros = "1234567890"
        dni = dni.upper()
        if len(dni) == 9:                   #el dni debe tener 9 caracteres
            dig_control = dni[8]
            dni = dni[:8]                   #el numero que son los 8 primeros
            if dni[0] in dig_ext:
                print(dni)
                dni = dni.replace(dni[0],reemp_dig_ext[dni[0]])
            return len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni)%23] == dig_control
        return False
    except:
        print("Error")
        return None

#inserta un registro
def insertarcli(fila):
    """
    Función utilizada para introducir los clientes en nuestra base de datos
    :param fila: Array que contiene todos los datos del cliente.
    :return: None
    """
    try:
        conexion.cur.execute('insert into  clientes(dni,apel,nome, data) values(?,?,?,?)',fila)
        conexion.conex.commit()

    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

# select para utilizar en las operaciones de datos
def listar():
    """
    Consulta a la base de datos para seleccionar todos los clientes guardados.
    :return: Retorna todas los clientes de la base de datos.
    """
    try:
        conexion.cur.execute('select * from clientes')
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

# esta funcion da de baja un clieente
def bajacli(dni):
    """
    Consulta a la base de datos realizada para eliminar un cliente,
    el cual es buscado por el DNI.
    :param dni: Dato utilizado como primary key de los clientes.
    :return: None
    """
    try:
        conexion.cur.execute('delete from clientes where dni = ?', (dni,))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def modifcli(registro, cod):
    """
    Modifica los datos de los clientes.
    :param registro: Lista con todos los datos de un cliente.
    :param cod: Primary key del cliente del que se van a modificar los datos.
    :return: Void
    """
    try:
        conexion.cur.execute('update clientes set dni = ?, apel= ?, nome = ?, data = ? where id = ?',
                             (registro[0], registro[1], registro[2], registro[3], cod))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()


def listadocli(listclientes):
    """
    Este método carga los datos de la tabla clientes en el treeView
    :param listclientes: Lista con todos los datos de los clientes
    :return: None
    """
    try:
        variables.listado = listar()
        listclientes.clear()
        for registro in variables.listado:
            listclientes.append(registro[1:5])
    except:
        print("error en cargar treeview")


def selectcli(dni):
    """
    Busqueda de un cliente mediante el dato DNI
    :param dni: Dato con el que se hace la consulta SQL
    :return: Retorna un cliente
    """
    try:
        conexion.cur.execute('select id from clientes where dni = ?', (dni,))
        listado = conexion.cur.fetchone()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()


def apelnomfac(dni):
    """
    Consulta para recuperar los datos nombre y apellido de un cliente
    buscando por su DNI
    :param dni: Parametro con el que se va a realizar la consulta
    :return:
    """
    try:
        conexion.cur.execute('select apel, nome from clientes where dni = ?', (dni,))
        listado = conexion.cur.fetchone()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def insertar_cliente_excel_BD(celdas_clientes):
    """
    Importar los clientes guardados en un fichero excel a nuestra base de datos.
    :param celdas_clientes: Son todas las celdas del fichero que contienen los datos de un cliente
    :return:
    """
    cliente = []
    for celda_cliente in celdas_clientes:
        if celda_cliente.ctype == sheet.XL_CELL_DATE:
            cliente.append(funciones_excel.formatear_fecha_excel(celda_cliente))
        else:
            cliente.append(celda_cliente.value)
    insertarcli(cliente)




