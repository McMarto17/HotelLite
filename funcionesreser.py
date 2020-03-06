#coding=utf-8

import conexion
import sqlite3
import variables
from datetime import datetime

def limpiarentry(fila):
    """
    Con este método vaciamos los datos introducidos en los entry de entrada de datos.
    :param fila: fila que vamos a limpiar de datos
    :return: Void
    """
    for i in range(len(fila)):
        fila[i].set_text('')
    for i in range(len(variables.menslabel)):
        variables.menslabel[i].set_text('')
    variables.cmbhab.set_active(-1)

def calculardias():
    """
    Metodo con el que se calcula el numero de noches de la reserva,
    en funcion de las fechas de entrda y de salida del cliente.
    :return: Retorna un numero entero (Numero de Noches)
    """
    diain = variables.filareserva[2].get_text()
    date_in = datetime.strptime(diain, '%d/%m/%Y').date()
    diaout = variables.filareserva[3].get_text()
    date_out = datetime.strptime(diaout, '%d/%m/%Y').date()
    noches = (date_out-date_in).days
    if noches <= 0:
        variables.menslabel[2].set_text('Check-Out debe ser posterior')
        variables.reserva = 0
    else:
        variables.reserva = 1
        variables.menslabel[2].set_text(str(noches))

def insertares(fila):
    """
    Consulta SQl con la que insertamos una reserva en nuestra base de datos
    :param fila: Lista con todos los datos de una reserva
    :return: Void
    """
    try:
        conexion.cur.execute('insert into  reservas(dni, numhab, checkin, checkout, noches) values(?,?,?,?,?)', fila)
        conexion.conex.commit()

    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listadores():
    """
    Lista todas las reservas en el treeView de reservas
    :return: Void
    """
    try:
        variables.listado = listares()
        variables.listreservas.clear()
        for registro in variables.listado:
            variables.listreservas.append(registro)
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listares():
    """
    Consulta SQL que recoge todos los datos de la tabla de reservas
    :return: Retorna una lista de reservas
    """
    try:
        conexion.cur.execute('select codreser, dni, numhab, checkin, checkout, noches from reservas')
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def buscarapelcli(dni):
    """
    Se busca el apellido del cliente que efectuó de la reserva
    :param dni: Paramatro que se utiliza en la consulta
    :return: Retorna el apellido del cliente
    """
    try:
        conexion.cur.execute('select apel from clientes where dni = ?', (dni,))
        apel = conexion.cur.fetchone()
        conexion.conex.commit()
        return apel
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def buscarnome(dni):
    """
    Se busca el nombre del cliente, que se busca por su dni
    :param dni: parametro con el que se realiza la consulta de busqueda del cliente
    :return:
    """
    try:
        conexion.cur.execute('select nome from clientes where dni = ?', (dni,))
        nombre = conexion.cur.fetchone()
        conexion.conex.commit()
        return nombre
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def buscarpreciohabitacion(numhabitacion):
    """
    Se busca una habitacion por su numero, para poder sacar su precio
    :param numhabitacion: Parametro utilizado para la consulta de busqueda de la habitacion
    :return: retorna el precio de la habitacion buscada
    """
    try:
        conexion.cur.execute('select prezo from habitacion where numero = ?', (numhabitacion,))
        precio = conexion.cur.fetchone()
        conexion.conex.commit()
        return precio

    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()
'''''
def bajareserva(cod):
    try:
        print(cod)
        conexion.cur.execute('select numhab from reservas where codreser = ?', (cod,))
        conexion.conex.commit()
        if variables.switch.get_active():
            libre = 'SI'
        else:
            libre = 'NO'
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()
'''''

def versilibre(numhab):
    """
    Busca una habitacion y comprueba si esta se encuentra libre
    :param numhab: Parametro con el que se busca la habitacion
    :return: Retorna True si se encuentra libre o False si no esta libre.
    """
    try:
        conexion.cur.execute('select libre from habitacion where numero = ?', (numhab,))
        lista= conexion.cur.fetchone()
        conexion.conex.commit()
        if lista[0] == 'SI':
            return True
        else:
            return False
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()