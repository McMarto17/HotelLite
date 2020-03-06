#coding=utf-8
"""
Aquí vendran todas las funciones que afectan a la ¡gestion de los
habitaciones
Limpiarentry vaciará el contenido de los entry

"""

import conexion, sqlite3, variables

def insertarhab(fila):
    """
    Metodo con el que insertamos una habitacion a la base de datos
    :param fila: Contiene un lista de todos los datos de la habitacion
    :return:
    """
    try:
        conexion.cur.execute('insert into habitacion(numero,tipo,prezo,libre) values(?,?,?,?)', fila)
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listarhab():
    """
    Consulta SQL para recuperar todas las habitaciones guardadas en
     la base de datos
    :return: Retorna una lista con todos los numeros de las habitaciones
    """
    try:
        conexion.cur.execute('select * from habitacion')
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def limpiarentry(fila):
    """
    Con este método vaciamos los datos introducidos en los entry
    de entrada de datos.
    :param fila: fila que vamos a limpiar de datos
    :return: Void
    """
    for i in range(len(fila)):
        fila[i].set_text('')
    variables.filarbt[1].set_active(True)

def listadohab(listhab):
    """
    Este método carga los datos de la tabla habitaciones en el treeView
    :param listclientes: Lista con todos los datos de las habitaciones.
    :return:
    """
    try:
        variables.listado = listarhab()
        variables.listhab.clear()
        for registro in variables.listado:
            listhab.append(registro)
    except:
        print("error en cargar treeview de hab")


def bajahab(numhab):
    """
    Consulta SQL que utilizamos para eliminar una habitacion de
    nuestra base de datos.
    :param numhab: Primary key que utilizamos para buscar la habitacion deseada
    :return: Void
    """
    try:
        conexion.cur.execute('delete from habitacion where numero = ?', (numhab,))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()


def modifhab(registro, numhab):
    """
    Metodo utilizado para modificar los datos de una habitacion.
    :param registro: Lista con todos los datos modificados de la habitacion.
    :param numhab: Parametro con el que vamos a seleccionar la habitacion.
    :return: Void
    """
    try:
        conexion.cur.execute('update habitacion set tipo = ?, prezo = ?, libre = ? where numero = ?',
                             (registro[1], registro[0], registro[2], numhab))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listadonumhab():
    """
     Busca todos los numeros de las habitaciones para visualizarlos en
     el combobox de la zona de reservas
    :return: Void
    """
    try:
        conexion.cur.execute('select numero from habitacion')
        listado = conexion.cur.fetchall()
        variables.listcmbhab.clear()
        for row in listado:
            variables.listcmbhab.append(row)
        conexion.conex.commit()

    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()


def listadonumhabres():
    """
    Se buscan los numeros de todas las habitaciones
    :return: Void
    """
    try:
        conexion.cur.execute('select numero from habitacion')
        lista = conexion.cur.fetchall()
        return lista
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()


def cambiaestadohab(libre, numhabres):
    """
    Metodo utilizado para cambiar el estado de la habitacion.
    :param libre: Booleno utilizado para cambiar el estado de la habitacion
    :param numhabres: Clave primaria con la que se realiza la consulta de la habitacion
    :return: Void
    """
    try:
        print(libre)
        conexion.cur.execute('update habitacion set libre = ? where numero = ?',
                             (libre, numhabres))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
       print(e)
       conexion.conex.rollback()