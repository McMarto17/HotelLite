#coding=utf-8
import webbrowser

import gi

import funcionesServicios

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import conexion, variables, funcionescli, funcioneshab, funcionesreser, funcionesvar, impresion
import os, shutil
import xlrd, xlwt
from datetime import date, datetime, time


class Eventos():

    # eventos generales del program
    def on_acercade_activate(self, widget):
        """
        Abre la ventana Acerca de
        :return: Void
        """
        try:
            variables.venacercade.show()
        except:
            print('error abrira acerca de')
    def on_btnMenuAxuda_activate(self,widget):
        """
        Permite acceder a la documentacion del programa
        :return: Void
        """
        os.system('pydoc -p 1234')
        webbrowser.open_new('http://localhost:1234')

    def on_btnCerrarabout_clicked(self, widget):
        """
        Evento que cierra la ventana Acerca de
        :return: Void
        """
        try:
            variables.venacercade.connect('delete-event', lambda w, e: w.hide() or True)
            variables.venacercade.hide()
        except:
            print('error abrir calendario')

    def on_menuBarsalir_activate(self, widget):
        """
        Evento que finaliza la aplicacion
        :return:
        """
        try:
            self.salir()
        except:
            print('salir en menubar')

    def salir(self, widget):
        """
        Metodo que finaliza la conexion con la base de datos y cierra la aplicacion
        :return: Void
        """
        try:
            conexion.Conexion.cerrarbbdd(self)
            funcionesvar.cerrartimer()
            Gtk.main_quit()
        except:
            print('error función salir')

    def on_venPrincipal_destroy(self, widget):
        """
        Evento que cierra la ventana principal de la aplicacion
        :return: Void
        """
        self.salir(widget)

    def on_btnSalirtool_clicked(self, widget):
        """
        Boton que nos muestra la ventana de dialogo de Salida
        :return: Void
        """
        variables.vendialogsalir.show()

    def on_btnCancelarsalir_clicked(self, widget):
        """
        Boton que oculta la ventana de dialogo de salida
        :return: Void
        """
        variables.vendialogsalir.connect('delete-event', lambda w, e: w.hide() or True)
        variables.vendialogsalir.hide()

    def on_btnAceptarsalir_clicked(self, widget):
        """
        Boton que llama al metodo salir() para finalizar la aplicacion
        :return: Void
        """
        self.salir(widget)

    """
    Eventos Clientes
    """

    def on_btnAltacli_clicked(self, widget):
        """
        Boton que da de alta un cliente
        :return: Void
        """
        try:
            dni = variables.filacli[0].get_text()
            apel = variables.filacli[1].get_text()
            nome = variables.filacli[2].get_text()
            data = variables.filacli[3].get_text()
            registro = (dni, apel, nome, data)
            if funcionescli.validoDNI(dni):
                funcionescli.insertarcli(registro)
                funcionescli.listadocli(variables.listclientes)
                funcionescli.limpiarentry(variables.filacli)
            else:
                variables.menslabel[0].set_text('ERROR DNI')
        except:
            print("Error alta cliente")


    def on_btnBajacli_clicked(self, widget):
        """
        Boton que da de baja un cliente
        :return: Void
        """
        try:
            dni = variables.filacli[0].get_text()
            if dni != '':
                funcionescli.bajacli(dni)
                funcionescli.listadocli(variables.listclientes)
                funcionescli.limpiarentry(variables.filacli)
            else:
                print('falta dni u otro error')
        except:
            print("error en botón baja cliente")

    #  modificamos cliente
    def on_btnModifcli_clicked(self, widget):
        """
        Boton que modificar los datos de un cliente
        :return: Void
        """
        try:
            cod = variables.menslabel[1].get_text()
            dni = variables.filacli[0].get_text()
            apel = variables.filacli[1].get_text()
            nome = variables.filacli[2].get_text()
            data = variables.filacli[3].get_text()
            registro = (dni, apel, nome, data)
            if dni != '':
                funcionescli.modifcli(registro, cod)
                funcionescli.listadocli(variables.listclientes)
                funcionescli.limpiarentry(variables.filacli)
            else:
                print('falta el dni')
        except:
            print('error en botón modificar')

    # controla el valor del deni
    def on_entDni_focus_out_event(self, dni, widget):
        """
        Controla el valor del dni
        :param dni: Variable
        :return: Void
        """
        try:
            dni = variables.filacli[0].get_text()
            if funcionescli.validoDNI(dni):
                variables.menslabel[0].set_text('')
                pass
            else:
                variables.menslabel[0].set_text('ERROR')
        except:
            print("Error alta cliente en out focus")

    def on_treeClientes_cursor_changed(self, widget):
        """
        Evento que selecciona un cliente en el treeView
        :return: Void
        """
        try:
            model, iter = variables.treeclientes.get_selection().get_selected()
            # model es el modelo de la tabla de datos
            # iter es el número que identifica a la fila que marcamos
            variables.menslabel[0].set_text('')
            funcionescli.limpiarentry(variables.filacli)
            if iter != None:
                sdni = model.get_value(iter, 0)
                sapel = model.get_value(iter, 1)
                snome = model.get_value(iter, 2)
                sdata = model.get_value(iter, 3)
                if sdata == None:
                    sdata = ''
                cod = funcionescli.selectcli(sdni)
                variables.menslabel[1].set_text(str(cod[0]))
                variables.filacli[0].set_text(str(sdni))
                variables.filacli[1].set_text(str(sapel))
                variables.filacli[2].set_text(str(snome))
                variables.filacli[3].set_text(str(sdata))
                variables.menslabel[4].set_text(str(sdni))
                variables.menslabel[5].set_text(str(sapel))
        except:
            print("error carga cliente")

    def on_btnCalendar_clicked(self, widget):
        """
        Evento que acciona una ventana emergente de calendario 1
        :return: Void
        """
        try:
            variables.semaforo = 1
            variables.vencalendar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.vencalendar.show()

        except:
            print('error abrir calendario')

    def on_btnCalendarResIn_clicked(self, widget):
        """
        Evento que acciona una ventana emergente de calendario
        :return: Void
        """
        try:
            variables.semaforo = 2
            variables.vencalendar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.vencalendar.show()
        except:
            print('error abrir calendario')

    def on_btnCalendarResOut_clicked(self, widget):
        """
        Evento que acciona una ventana emergente de calendario 3
        :return:
        """
        try:
            variables.semaforo = 3
            variables.vencalendar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.vencalendar.show()
        except:
            print('error abrir calendario')

    def on_Calendar_day_selected_double_click(self, widget):
        """
        Evento que selecciona un dia dentro de la ventana de calendario
        :return: Void
        """
        try:
            agno, mes, dia = variables.calendar.get_date()
            fecha = "%02d/" % dia + "%02d/" % (mes + 1) + "%s" % agno
            if variables.semaforo == 1:
                variables.filacli[3].set_text(fecha)
            elif variables.semaforo == 2:
                variables.filareserva[2].set_text(fecha)
            elif variables.semaforo == 3:
                variables.filareserva[3].set_text(fecha)
                funcionesreser.calculardias()
            else:
                pass
            # variables.semaforo = 0
            variables.vencalendar.hide()
        except:
            print('error al coger la fecha')

    # Eventos de las habitaciones

    def on_btnAltahab_clicked(self, widget):
        """
        Boton que da de alta una habtiacion
        :return: Void
        """
        try:
            numhab = variables.filahab[0].get_text()
            prezohab = variables.filahab[1].get_text()
            prezohab = prezohab.replace(',', '.')
            prezohab = float(prezohab)
            prezohab = round(prezohab, 2)
            if variables.filarbt[0].get_active():
                tipo = 'simple'
            elif variables.filarbt[1].get_active():
                tipo = 'doble'
            elif variables.filarbt[2].get_active():
                tipo = 'family'
            else:
                pass

            if variables.switch.get_active():
                libre = 'SI'
            else:
                libre = 'NO'
            registro = (numhab, tipo, prezohab, libre)
            if numhab != None:
                funcioneshab.insertarhab(registro)
                funcioneshab.listadohab(variables.listhab)
                funcioneshab.listadonumhab()
                funcioneshab.limpiarentry(variables.filahab)
            else:
                pass
        except:
            print("Error alta habitacion")

    def on_treeHab_cursor_changed(self, widget):
        """
        Evento que selecciona una habitacion dentro del treeView
        :return: Void
        """
        try:
            model, iter = variables.treehab.get_selection().get_selected()
            # model es el modelo de la tabla de datos
            # iter es el número que identifica a la fila que marcamos
            funcioneshab.limpiarentry(variables.filahab)
            if iter != None:
                snumhab = model.get_value(iter, 0)
                stipo = model.get_value(iter, 1)
                sprezo = model.get_value(iter, 2)
                sprezo = round(sprezo, 2)
                variables.filahab[0].set_text(str(snumhab))
                variables.filahab[1].set_text(str(sprezo))
                if stipo == str('simple'):
                    variables.filarbt[0].set_active(True)
                elif stipo == str('doble'):
                    variables.filarbt[1].set_active(True)
                elif stipo == str('family'):
                    variables.filarbt[2].set_active(True)
                slibre = model.get_value(iter, 3)
                if slibre == str('SI'):
                    variables.switch.set_active(True)
                else:
                    variables.switch.set_active(False)
        except:
            print("error carga habitacion")

    def on_btnBajahab_clicked(self, widget):
        """
        Evento que da de baja una habitacion
        :return: Void
        """
        try:
            numhab = variables.filahab[0].get_text()
            if numhab != '':
                funcioneshab.bajahab(numhab)
                funcioneshab.limpiarentry(variables.filahab)
                funcioneshab.listadohab(variables.listhab)
            else:
                pass
        except:
            print('borrar baja hab')

    def on_btnModifhab_clicked(self, widget):
        """
        Evento que modifica los datos de una habitacion
        :return: Void
        """
        try:
            numhab = variables.filahab[0].get_text()
            prezo = variables.filahab[1].get_text()
            if variables.switch.get_active():
                libre = 'SI'
            else:
                libre = 'NO'

            if variables.filarbt[0].get_active():
                tipo = 'simple'
            elif variables.filarbt[1].get_active():
                tipo = 'doble'
            elif variables.filarbt[2].get_active():
                tipo = 'family'
            else:
                pass
            registro = (prezo, tipo, libre)
            if numhab != '':
                funcioneshab.modifhab(registro, numhab)
                funcioneshab.listadohab(variables.listhab)
                funcioneshab.limpiarentry(variables.filahab)
            else:
                print('falta el numhab')
        except:
            print('error modif hab')

    # eventos de los botones del toolbar

    def on_Panel_select_page(self, widget):
        """
        Evento para seleccionar el panel deseado
        :return: Void
        """
        try:
            funcioneshab.listadonumhab()
        except:
            print("error botón cliente barra herramientas")

    def on_btnClitool_clicked(self, widget):
        """
        Evento de seleccion del panel de clientes
        :return: Void
        """
        try:
            panelactual = variables.panel.get_current_page()
            if panelactual != 0:
                variables.panel.set_current_page(0)
            else:
                pass
        except:
            print("error botón cliente barra herramientas")

    def on_btnReservatool_clicked(self, widget):
        """
        Evento de seleccion del panel de reservas
        :return:
        """
        try:
            panelactual = variables.panel.get_current_page()
            if panelactual != 1:
                variables.panel.set_current_page(1)
                funcioneshab.listadonumhab(self)
            else:
                pass
        except:
            print("error botón cliente barra herramientas")

    def on_btnHabita_clicked(self, widget):
        """
        Evento de seleccion del panel de habitaciones
        :return: Void
        """
        try:
            panelactual = variables.panel.get_current_page()
            if panelactual != 2:
                variables.panel.set_current_page(2)
            else:
                pass
        except:
            print("error botón habitacion barra herramientas")

    def on_btnCalc_clicked(self, widget):
        """
        Evento que ejecuta la aplicacion de calculadora del sistema
        :return: Void
        """
        try:
            os.system('/snap/bin/gnome-calculator')
        except:
            print('error lanzar calculadora')

    def on_btnRefresh_clicked(self, widget):
        """
        evento que vacia todos valores de los widget de entrada
        :return: Void
        """
        try:
            funcioneshab.limpiarentry(variables.filahab)
            funcionescli.limpiarentry(variables.filacli)
            funcionesreser.limpiarentry(variables.filareserva)
        except:
            print('error referes')

    def on_btnBackup_clicked(self, widget):
        """
        Evento que abre la ventana de seleccion de Backup
        :return: Void
        """
        try:
            variables.filechooserbackup.show()
            variables.neobackup = funcionesvar.backup()
            variables.neobackup = str(os.path.abspath(variables.neobackup))
            print(variables.neobackup)

        except:
            print('error abrir file choorse backup')

    def on_btnGrabarbackup_clicked(self, widget):
        """
        Evento que nos permite crear un backup de la base de datos que estamos utilizando
        :return: Void
        """
        try:
            destino = variables.filechooserbackup.get_filename()
            destino = destino + '/'
            variables.menslabel[3].set_text(str(destino))
            if shutil.move(str(variables.neobackup), str(destino)):
                variables.menslabel[3].set_text('Copia de Seguridad Creada')
        except:
            print('error dselect fichero')

    def on_btnCancelfilechooserbackup_clicked(self, widget):
        """
        Evento que cierra la ventana de seleccion de backup
        :return: Void
        """
        try:
            variables.filechooserbackup.connect('delete-event', lambda w, e: w.hide() or True)
            variables.filechooserbackup.hide()
        except:
            print('error cerrar file chooser')

    ## reservas

    def on_cmbNumres_changed(self, widget):
        """
        Evento que permite visualizar la lista de habitaciones en el panel de reservas
        :return:Void
        """
        try:
            index = variables.cmbhab.get_active()
            model = variables.cmbhab.get_model()
            item = model[index]
            variables.numhabres = item[0]
        except:
            print('error mostrar habitacion combo')

    def on_btnAltares_clicked(self, widget):
        """
        Evento que inserta una reservas en la base de datos
        :return: Void
        """
        try:
            if variables.reserva == 1:
                dnir = variables.menslabel[4].get_text()
                chki = variables.filareserva[2].get_text()
                chko = variables.filareserva[3].get_text()
                noches = int(variables.menslabel[2].get_text())
                registro = (dnir, variables.numhabres, chki, chko, noches)
                if funcionesreser.versilibre(variables.numhabres):
                    funcionesreser.insertares(registro)
                    funcionesreser.listadores()
                    # actualizar a NO
                    libre = ['NO']
                    funcioneshab.cambiaestadohab(libre, variables.numhabres)
                    funcioneshab.listadohab(variables.listhab)
                    funcioneshab.limpiarentry(variables.filahab)
                    funcionesreser.limpiarentry(variables.filareserva)
                else:
                    print('habitación ocupada')
        except:
            print('error en alta res')

    def on_btnRefreshcmbhab_clicked(self, widget):
        """
        Evento que actualiza la lista de las habitaciones
        :return: Void
        """
        try:
            variables.cmbhab.set_active(-1)
            funcioneshab.listadonumhab(self)
        except:
            print('error limpiar combo hotel')

    def on_treeReservas_cursor_changed(self, widget):
        """
        Evento que nos permite seleccionar una reserva dentro del treeView
        :return: Void
        """
        try:
            model, iter = variables.treereservas.get_selection().get_selected()
            # model es el modelo de la tabla de datos
            # iter es el número que identifica a la fila que marcamos
            funcionesreser.limpiarentry(variables.filareserva)
            if iter != None:
                variables.codr = model.get_value(iter, 0)
                sdni = model.get_value(iter, 1)
                sapel = funcionesreser.buscarapelcli(str(sdni))
                snome = funcionesreser.buscarnome(str(sdni))
                snumhab = model.get_value(iter, 2)
                lista = funcioneshab.listadonumhabres()
                m = -1
                for i, x in enumerate(lista):
                    if str(x[0]) == str(snumhab):
                        m = i
                variables.cmbhab.set_active(m)
                schki = model.get_value(iter, 3)
                schko = model.get_value(iter, 4)
                snoches = model.get_value(iter, 5)
                variables.menslabel[4].set_text(str(sdni))
                variables.menslabel[5].set_text(str(sapel[0]))
                variables.menslabel[2].set_text(str(snoches))
                variables.lblNochesFacturacion.set_text(str(snoches))
                variables.filareserva[2].set_text(str(schki))
                variables.filareserva[3].set_text(str(schko))
                variables.lblfechaFacturacion.set_text(str(schko))
                variables.lbldniFacturacion.set_text(str(sdni))
                variables.lblapelidoFacturacion.set_text(str(sapel[0]))
                variables.lblcodigoReservaFacturacion.set_text(str(variables.codr))
                variables.lblnomeFacturacion.set_text(str(snome[0]))
                variables.lblhabitacionFacturacion.set_text(str(snumhab))
                variables.precioUnidad = funcionesreser.buscarpreciohabitacion(str(snumhab))
                #variables.lblprecioUnidadFacturacion.set_text(str(precioUnidad[0]))
                variables.precioTotal = float(str(snoches)) * float(str(variables.precioUnidad[0]))
                variables.strPrecioTotal = str(variables.precioTotal)+"€"
                variables.lblPrecioFacturacion.set_text(variables.strPrecioTotal)
                variables.lblCodigoReservaServicio.set_text(str(variables.codr))
                variables.lblHabitacionServicio.set_text(str(snumhab))
                global datosfactura
                datosfactura = (variables.codr, snoches, sdni, snumhab, schko, str(variables.precioUnidad[0]))
                funcionesServicios.listadoServicio(variables.listaServicios, variables.codr)

                funcionesServicios.calcularPrecioServicios()
        except Exception as e:
            print(e)
            print('error cargar valores de reservas')

    def on_btnFinReserva_clicked(self, widget):
        """
        Evento que finaliza y borra una reserva
        :return: Void
        """
        try:
            libre = 'SI'
            numhabres = variables.numhabres
            funcioneshab.cambiaestadohab(libre, numhabres)
            funcionesreser.limpiarentry(variables.filareserva)
            funcionesreser.listadores()
            funcioneshab.listadohab(variables.listhab)

        except:
            print('error baja reserva')

    def on_btnModifres_clicked(self, widget):
        """
        Evento que modifica los datos de una reserva
        :return: Void
        """
        try:
            dnir = variables.menslabel[4].get_text()
            chki = variables.filareserva[2].get_text()
            chko = variables.filareserva[3].get_text()
            noches = int(variables.menslabel[2].get_text())
            registro = (dnir, variables.numhabres, chki, chko, noches)
            funcionesreser.modifreserva(registro, variables.codr)
            funcionesreser.limpiarentry(variables.filareserva)
            funcionesreser.listadores()

        except:
            print('error modificar reserva')

    def on_btChkout_clicked(self, widget):
        """
        Evento que cambia el estado de la habitacion
        :return: Void
        """
        try:
            chko = variables.filareserva[3].get_text()
            today = date.today()
            print(chko)

            hoy = datetime.strftime(today, '%d/%m/%Y')
            print(hoy)
            registro = (variables.numhabres)
            if str(hoy) == str(chko):
                funcioneshab.modifhabres(registro)
                funcioneshab.listadohab(variables.listhab)
            else:
                print('puede facturar')
                # cambiar el estado de la habitación de ocupada a libre

        except:
            print('error en checkout')

    def on_btnImprimir_clicked(self, widget):
        """
        Evento que lanza la impresion de la factura de la reserva
        :return: Void
        """
        try:
            impresion.factura(datosfactura)
        except Exception as e:
            print(e)

    def on_menuListarClientes_activate(self, widget):
        """
                Evento que lanza la impresion de la lista de clientes
                :return: Void
                """
        try:
            impresion.clientes(variables.listclientes)
        except Exception as e:
            print(e)

    def on_menuBarImportarClientes_activate(self, widget):
        """
        Evento que inicia la ventana de importacion de clientes
        :return: Void
        """
        try:
            variables.ventanaImportar.show()

        except Exception as e:
            print(e)
            print('Error en importar clientes')

    def on_menuBarExportarClientes_activate(self, widget):
        """
        Evento que inicia la ventana de exportacion
        :return: Void
        """
        try:
            variables.ventanaExportar.show()
        except Exception as e:
            print(e)
            print("Error en exportar clientes")

    def on_btnExportar_clicked(self, widget):
        """
        Evento que nos permite exportar un fichero con los cliente guardados
        :return: Void
        """
        try:
            destino = variables.ventanaExportar.get_filename()
            destino = str(destino) + str('/fichero_exportado.xls')
            estilo_cabecera = xlwt.easyxf('font: name Times New Roman, colour red, bold on')
            estilo_celda = xlwt.easyxf(num_format_str='DD-MM-YY')
            fichero_excel = xlwt.Workbook()

            hoja_excel = fichero_excel.add_sheet('NuevoClientes', cell_overwrite_ok=True)
            hoja_excel.write(0, 0, 'DNI', estilo_cabecera)
            hoja_excel.write(0, 1, 'APELIDOS', estilo_cabecera)
            hoja_excel.write(0, 2, 'NOMBRE', estilo_cabecera)
            hoja_excel.write(0, 3, 'FECHA_ALTA', estilo_cabecera)

            listado_clientes = funcionescli.listar()

            for i in range(len(listado_clientes)):
                for j in range(len(listado_clientes[0])):
                    hoja_excel.write(i, j, listado_clientes[i][j], estilo_celda)
            fichero_excel.save(destino)

            variables.ventanaExportar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.ventanaExportar.hide()
        except Exception as e:
            print(e)
            print("Error en exportar clientes")

    def on_btnCancelVentanaExportar_clicked(self, widget):
        """
        Evento que cancela y finaliza la ventana de exportacion
        :return: Void
        """
        try:
            variables.ventanaExportar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.ventanaExportar.hide()
        except:
            print('error cerrar ventana Exportar')

    def on_btnImportar_clicked(self, widget):
        """
        Evento que nos permite importar un fichero con los clientes
        :return: Void
        """

        try:
            fichero_excel = xlrd.open_workbook(variables.ventanaImportar.get_filename())
            hoja_clientes = fichero_excel.sheet_by_index(0)
            numero_filas_clientes = hoja_clientes.nrows
            numero_columnas_clientes = hoja_clientes.ncols

            for i in range(numero_filas_clientes):
                celdas_cliente = []
                if i > 0:
                    for j in range(numero_columnas_clientes):
                        celdas_cliente.append(hoja_clientes.cell(i, j))
                    funcionescli.insertar_cliente_excel_BD(celdas_cliente)
                    funcionescli.listadocli(variables.listclientes)
            variables.ventanaImportar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.ventanaImportar.hide()

        except Exception as e:
            print(e)
            print('Error en importar clientes')

    def on_btnCancelVentanaImportar_clicked(self, widget):
        """
        Evento que cancela y finaliza la ventana de importacion
        :return: Void
        """
        try:
            variables.ventanaImportar.connect('delete-event', lambda w, e: w.hide() or True)
            variables.ventanaImportar.hide()
        except:
            print('error cerrar ventana importar')


# EVENTOS PARA EL PANEL DE SERVICIOS

    def on_btnVentanaPrecios_activate(self,widget):
        """
        Evento que permite visualizar la ventana de modificacion de precios
        :return: Void
        """
        try:
            variables.ventanPreciosServicios.show()
            conexion.cur.execute("select * from precios")
            precios = conexion.cur.fetchall()
            variables.listaPrecios[0].set_text(str(precios[0][0]))
            variables.listaPrecios[1].set_text(str(precios[0][1]))
            variables.listaPrecios[2].set_text(str(precios[0][2]))
        except Exception as e:
            print(e)
            print("Error al lanzar ventana de precios")

    def on_btnSalirPrecios_clicked(self, widget):
        """
        Evento que finaliza la venta de modificacion de precios
        :return: Void
        """
        try:
            variables.ventanPreciosServicios.connect('delete-event', lambda w, e: w.hide() or True)
            variables.ventanPreciosServicios.hide()
        except:
            print('error cerrar ventana precios de servicios')

    def on_btnGuardarPrecios_clicked(self,widget):
        """
        Evento que guarda los cambios en los precios
        :return: Void
        """
        try:
            precioDesayuno = variables.listaPrecios[0].get_text()
            precioComida = variables.listaPrecios[1].get_text()
            precioParking = variables.listaPrecios[2].get_text()
            precios = (precioDesayuno, precioComida, precioParking)

            funcionesServicios.modificarPrecios(precios)

            variables.ventanPreciosServicios.connect('delete-event', lambda w, e: w.hide() or True)
            variables.ventanPreciosServicios.hide()
        except Exception as e:
            print(e)
            print("Error al guardar los valores de precios")

    def on_btnAltaServicioBasico_clicked(self,widget):
        """
        Evento que da de alta los servicios seleccionados
        :return: Void
        """
        try:
            conexion.cur.execute("select * from precios")
            precios = conexion.cur.fetchall()
            codigoReserva = variables.lblCodigoReservaServicio.get_text()
            if(variables.rbDesayuno.get_active()):
                existeDesayuno = False
                for registro in variables.listaServicios:
                     if registro[1] == "Desayuno":
                         existeDesayuno = True
                if existeDesayuno == False:
                    conceptoDesayuno = "Desayuno"
                    precioDesayuno = precios[0][0]
                    filaDesayuno = (codigoReserva,conceptoDesayuno,precioDesayuno)
                    funcionesServicios.insertarServicio(filaDesayuno)
                else:
                    print("Ya hay un servicio Desayuno")

            elif(variables.rbComida.get_active()):
                existeComida = False
                for registro in variables.listaServicios:
                     if registro[1] == "Comida":
                         existeComida = True
                if existeComida == False:
                    conceptoComida = "Comida"
                    precioComida = precios[0][1]
                    filaComida = (codigoReserva, conceptoComida, precioComida)
                    funcionesServicios.insertarServicio(filaComida)
                else:
                    print("Ya hay un servicio Comida")

            if(variables.chkParking.get_active()):
                existeParking = False
                for registro in variables.listaServicios:
                     if registro[1] == "Parking":
                         existeParking = True
                if existeParking == False:
                    conceptoParking = "Parking"
                    precioParking = precios[0][2]
                    filaParking = (codigoReserva, conceptoParking, precioParking)
                    funcionesServicios.insertarServicio(filaParking)
                else:
                    print("Ya hay un servicio de Parking")

            funcionesServicios.listadoServicio(variables.listaServicios,codigoReserva)
            funcionesServicios.calcularPrecioServicios()
            variables.rbNinguno.set_active(True)
            variables.chkParking.set_active(False)

        except Exception as e:
            print(e)

    def on_btnAltaOtroServicio_clicked(self,widget):
        """
        Evento que da de alta los servicios creados por el usuario
        :return: Void
        """
        try:
            codigoReserva = variables.lblCodigoReservaServicio.get_text()
            tipo = variables.entradaTipoServicio.get_text()
            precio = variables.entradaPrecioServicio.get_text()
            precio = float(precio)
            existeServicio = False
            for registro in variables.listaServicios:
                if registro[1] == tipo:
                    existeServicio = True
            if existeServicio == False:
                filaOtroServicio = (codigoReserva, tipo, precio)
                funcionesServicios.insertarServicio(filaOtroServicio)
                funcionesServicios.listadoServicio(variables.listaServicios,codigoReserva)
                funcionesServicios.calcularPrecioServicios()
                variables.entradaTipoServicio.set_text("")
                variables.entradaPrecioServicio.set_text("")
            else:
                print("Ya existe ese Servicio")
                variables.entradaTipoServicio.set_text("")
                variables.entradaPrecioServicio.set_text("")
        except Exception as e:
            print(e)

    def on_btnEliminarServicio_clicked(self,widget):
        try:
            codigoReserva = variables.lblCodigoReservaServicio.get_text()
            funcionesServicios.eliminarServicio(variables.codigoServicio)
            funcionesServicios.listadoServicio(variables.listaServicios, codigoReserva)

            funcionesServicios.calcularPrecioServicios()
        except:
            print("error en botón baja servicio")


    def on_treeServicios_cursor_changed(self, widget):
        """
        Evento que selecciona un servicio en el treeView
        :return: Void
        """
        try:
            model, iter = variables.treeServicios.get_selection().get_selected()
            # model es el modelo de la tabla de datos
            # iter es el número que identifica a la fila que marcamos

            if iter != None:
                variables.codigoServicio = model.get_value(iter, 0)

        except Exception as e:
            print(e)
            print("error carga servicios")