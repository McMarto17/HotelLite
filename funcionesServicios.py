#coding=utf-8
import conexion
import sqlite3

import variables


def modificarPrecios(precios):
    """
    Consulta a la base de datos para actualizar los datos de los precios
    :param precios: Lista con todos los precios anteriores
    :return: Void
    """
    try:
        conexion.cur.execute('update precios set precioDesayuno = ?, precioComida= ?, precioParking = ?',
                             (precios[0], precios[1], precios[2]))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def eliminarServicio(codigoServicio):
    """
    Consulta que nos permite eliminar un servicio de nuestra base de datos
    :return: Void
    """
    try:
        conexion.cur.execute('delete from servicios where codigoServicio = ?', (codigoServicio,))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()


def insertarServicio(fila):
    """
    Consulta para insertar los precios de los servicios en la base de datos
    :param fila: Lista con todos los precios.
    :return: Void
    """
    try:
        conexion.cur.execute('insert into servicios(codigoReservaServicio,concepto, precio) values(?,?,?)', fila)
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listarServicio(codigoReserva):
    """
    Consulta a la base de datos para seleccionar todos los servicios guardados.
    :return: Retorna todos los servicios de la base de datos.
    """
    try:
        conexion.cur.execute('select codigoServicio,concepto,precio from servicios where codigoReservaServicio= ?', (codigoReserva, ))
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listadoServicio(listaServicios,codigoReserva):
    """
    Este método carga los datos de la tabla servicios en el treeView
    :param listclientes: Lista con todos los datos de los servicios
    :return: None
    """
    try:
        variables.listado = listarServicio(codigoReserva)
        listaServicios.clear()
        for registro in variables.listado:
            listaServicios.append(registro)
    except Exception as e:
        print(e)
        print("error en cargar treeview servicios")

def calcularPrecioServicios():
    precios = 0
    iva10 = 0.1
    iva21 = 0.21
    ivaTotal = 0
    try:
        for registro in variables.listaServicios:
            precios = precios + registro[2]

        precioNoches = float(variables.precioTotal)
        subTotal = precioNoches + precios
        variables.lblSubtotalFactura.set_text(str(subTotal)+"€")
        ivaNoches = precioNoches * iva21

        for registro in variables.listaServicios:
            concepto = registro[1]
            if concepto == "Desayuno" or concepto == "Comida" or concepto == "Parking":
                ivaTotal = ivaTotal + (registro[2] * iva10)
            else:
                ivaTotal = ivaTotal + (registro[2] * iva21)
        variables.lblIvaFactura.set_text(str("{0:.2f}".format(ivaTotal + ivaNoches))+"€")
        variables.lblTotalFactura.set_text(str("{0:.2f}".format(ivaTotal + ivaNoches + subTotal))+"€")


    except Exception as e:
        print(e)
        print("error al calcular subtotal")

