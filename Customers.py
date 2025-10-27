from PyQt6 import QtCore
from Connection import *
import Globals
import re

class Customers:

    @staticmethod
    def checkDni():
        try:
            Globals.ui.txt_DNICliente.editingFinished.disconnect()
            dni = Globals.ui.txt_DNICliente.text()
            dni = str(dni).upper()
            Globals.ui.txt_DNICliente.setText(dni)
            dniCharacters = "TRWAGMYFPDXBNJZSQVHLCKE"
            nieCharacters = "XYZ"
            reempNieCharacters = {"X": "0", "Y": "1", "Z": "2"}
            validDigits = "1234567890"

            if len(dni) == 9:
                digitControl = dni[8]
                dni = dni[:8]

                if dni[0] in nieCharacters:
                    dni = dni.replace(dni[0], reempNieCharacters[dni[0]])

                if len(dni) == len([n for n in dni if n in validDigits]) and dniCharacters[int(dni) % 23] == digitControl:
                    Globals.ui.txt_DNICliente.setStyleSheet("background-color: rgb(255, 255, 220);")

                else:
                    Globals.ui.txt_DNICliente.setStyleSheet("background-color: #FFC0CB;")
                    Globals.ui.txt_DNICliente.setText(None)

            else:
                Globals.ui.txt_DNICliente.setStyleSheet("background-color: #FFC0CB;")
                Globals.ui.txt_DNICliente.setText(None)
                Globals.ui.txt_DNICliente.setPlaceholderText("Invalid DNI")

        except Exception as error:
            print("There was an error while checking dni: ", error)

        finally:
            Globals.ui.txt_DNICliente.editingFinished.connect(Customers.checkDni)


    @staticmethod
    def checkMail(email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        try:
            if re.match(pattern, email):
                Globals.ui.txt_emailCliente.setStyleSheet("background-color: rgb(255, 255, 220); color black")

            else:
                Globals.ui.txt_emailCliente.setStyleSheet("background-color: #FFC0CB; color black")
                Globals.ui.txt_emailCliente.setText(None)
                Globals.ui.txt_emailCliente.setPlaceholderText("Invalid email")

        except Exception as error:
            print("There was an error while checking email: ", error)


    @staticmethod
    def capitalize(text, widget):   ###capitalizar
        try:
            text = text.title()
            widget.setText(text)

        except Exception as error:
            print("There was an error while capitalizing: ", error)


    @staticmethod
    def checkMobile(number):   ###checkMobil
        pattern = r'^[67]\d{8}$'

        if re.match(pattern, number):
            Globals.ui.txt_numeroTelefono.setStyleSheet("background-color: rgb(255, 255, 220); color black")

        else:
            Globals.ui.txt_numeroTelefono.setStyleSheet("background-color: #FFC0CB; color black")
            Globals.ui.txt_numeroTelefono.setText(None)
            Globals.ui.txt_numeroTelefono.setPlaceholderText("Invalid number")


# surname, name, mobile, province, city invoice
    @staticmethod
    def loadCustomerTable(historicalOnly = True):   #loadTableCli
        try:
            customers = Connection.getCustomers(historicalOnly)

            index = 0
            uiTable = Globals.ui.tbl_customerList

            for customer in customers:
                uiTable.setRowCount(index + 1)
                uiTable.setItem(index, 0, QtWidgets.QTableWidgetItem(str(customer[2])))
                uiTable.setItem(index, 1, QtWidgets.QTableWidgetItem(str(customer[3])))
                uiTable.setItem(index, 2, QtWidgets.QTableWidgetItem(str(customer[5])))
                uiTable.setItem(index, 3, QtWidgets.QTableWidgetItem(str(customer[7])))
                uiTable.setItem(index, 4, QtWidgets.QTableWidgetItem(str(customer[8])))
                uiTable.setItem(index, 5, QtWidgets.QTableWidgetItem(str(customer[9])))

                uiTable.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                uiTable.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                uiTable.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                uiTable.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                uiTable.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                uiTable.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
                index += 1

        except Exception as error:
            print("There was an error while loading customer table: ", error)


    @staticmethod
    def showCustomerInfo():   ###selectCustomer
        try:
            selectedRow = Globals.ui.tbl_customerList.selectedItems()
            selectedCustomerPhone = selectedRow[2].text()
            customerData = Connection.getCustomerInfo(str(selectedCustomerPhone))

            allDataBoxes = [Globals.ui.txt_DNICliente, Globals.ui.txt_fechaAlta, Globals.ui.txt_apellidosCliente, Globals.ui.txt_nombresCliente,
                            Globals.ui.txt_emailCliente, Globals.ui.txt_numeroTelefono, Globals.ui.txt_dirCliente]

            for i in range(len(allDataBoxes)):
                allDataBoxes[i].setText(str(customerData[i]))

            Globals.ui.cmb_provinciaCliente.setCurrentText(str(customerData[7]))
            Globals.ui.cmb_ciudadCliente.setCurrentText(str(customerData[8]))

            if str(customerData[9]) == "paper":
                Globals.ui.rb_paperBiling.setChecked(True)
            else:
                Globals.ui.rb_eInvoice.setChecked(True)

            Globals.status = customerData[10]

            if Globals.status == "True":
                Globals.ui.lbl_status.setText("Active customer")
            else:
                Globals.ui.lbl_status.setText("Inactive customer")

        except Exception as error:
            print("There was an error while showing customer info: ", error)


    @staticmethod
    def deleteSelectedCustomer():   ###delCliente
        try:
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Warning")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            mbox.setText("Delete Customer?")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
            dni = Globals.ui.txt_DNICliente.text()

            if Connection.deleteCustomer(dni):
                successMbox = QtWidgets.QMessageBox()
                successMbox.setWindowTitle("Information")
                successMbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                successMbox.setText("The customer has been deleted.")
                successMbox.exec()
                Customers.loadCustomerTable()

            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Error")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            mbox.setText("An error has occurred while deleting the customer.")

        except Exception as error:
            print("There was an error while deleting the customer: ", error)


    @staticmethod
    def saveNewCustomer():   ###saveCli
        try:
            allDataBoxes = [Globals.ui.txt_DNICliente, Globals.ui.txt_fechaAlta, Globals.ui.txt_apellidosCliente, Globals.ui.txt_nombresCliente, Globals.ui.txt_emailCliente,
                            Globals.ui.txt_numeroTelefono, Globals.ui.txt_dirCliente, Globals.ui.cmb_provinciaCliente, Globals.ui.cmb_ciudadCliente]

            invoiceType = ""
            if Globals.ui.rb_eInvoice.isChecked():
                invoiceType = "electronic"
            elif Globals.ui.rb_paperBiling.isChecked():
                invoiceType = "paper"
            allDataBoxes.append(invoiceType)

            if Connection.addCustomer(allDataBoxes):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("The customer has been added.")
                mbox.exec()
                Customers.loadCustomerTable()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Error")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setText("An error has occurred while adding the customer.")
                mbox.exec()


        except Exception as error:
            print("There was an error while adding the customer: ", error)


    @staticmethod
    def modifyCustomer():   ###modifyCli
        try:
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Modify")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
            mbox.setText("Do you want to modify the customer's data?")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)

            if not mbox.exec():
                mbox.hide()
                return

            allDataBoxes = [Globals.ui.txt_DNICliente, Globals.ui.txt_fechaAlta, Globals.ui.txt_apellidosCliente, Globals.ui.txt_nombresCliente, Globals.ui.txt_emailCliente,
                            Globals.ui.txt_numeroTelefono, Globals.ui.txt_dirCliente, Globals.ui.cmb_provinciaCliente, Globals.ui.cmb_ciudadCliente]
            invoiceType = ""

            if Globals.ui.rb_eInvoice.isChecked():
                invoiceType = "electronic"
            elif Globals.ui.rb_paperBiling.isChecked():
                invoiceType = "paper"

            allDataBoxes.append(invoiceType)

            if Globals.status == "False":
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("Customer inactive. Do you want to activate it?")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)

                if mbox.exec():
                    Globals.status = "True"

            allDataBoxes.append(Globals.status)

            if Connection.modifyCustomerData(allDataBoxes):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("The customer has been modified.")
                mbox.exec()
                Customers.loadCustomerTable()

            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Error")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setText("An error has occurred while trying to modify the customer's data.")
                mbox.exec()

        except Exception as error:
            print("There was an error while modifying the customer's data: ", error)


    @staticmethod
    def searchCustomer():   ###buscaCli
        try:
            customerPhone = Globals.ui.txt_numeroTelefono.text()
            customerData = Connection.getCustomerInfo(customerPhone)

            if not customerData:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Error")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setText("The customer could not be found.")
                mbox.exec()

            allDataBoxes = [Globals.ui.txt_DNICliente, Globals.ui.txt_fechaAlta, Globals.ui.txt_apellidosCliente, Globals.ui.txt_nombresCliente, Globals.ui.txt_emailCliente,
                            Globals.ui.txt_numeroTelefono, Globals.ui.txt_dirCliente, Globals.ui.cmb_provinciaCliente, Globals.ui.cmb_ciudadCliente]

            for i in range(len(allDataBoxes)):
                allDataBoxes[i].setText(customerData[i])

            Globals.ui.cmb_provinciaCliente.setCurrentText(str(customerData[7]))
            Globals.ui.cmb_ciudadCliente.setText(str(customerData[8]))

            if str(customerData[9]) == "paper":
                Globals.ui.rb_paperBiling.setChecked(True)
            else:
                Globals.ui.rb_eInvoice.setChecked(True)

            Globals.status = customerData[10]

            if Globals.status == "True":
                Globals.ui.lbl_status.setText("Active customer")
            else:
                Globals.ui.lbl_status.setText("Inactive customer")

        except Exception as error:
            print("There was an error while searching for the customer: ", error)


    @staticmethod
    def customersHistorical():   ###HistoricoCli
        try:
            checkedHistorical = Globals.ui.chk_historico.isChecked()
            Customers.loadCustomerTable(checkedHistorical)

        except Exception as error:
            print("There was an error in customerhistorical: ", error)