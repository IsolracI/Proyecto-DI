import Events
from window import Ui_MainWindow
from AuxiliaryWindow import *
from PyQt6 import QtWidgets
from Connection import *
from Customers import *
from Events import *
import Globals
import sys


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        Globals.ui = Ui_MainWindow()
        Globals.ui.setupUi(self)

        # instances
        Globals.vencal = Calendar()
        Globals.ui.about = About()
        Globals.dlgOpen = FileDialogOpen()

        # load StyleSheet


        # DB Connection:
        historicalOnly = False
        Connection.dbConnection()
        Customers.loadCustomerTable(historicalOnly)
        Events.resizeCustomerTable()

        # menu bar Functions:
        Globals.ui.menuAbout.triggered.connect(Events.aboutMessage)
        Globals.ui.actionAbout.triggered.connect(Events.exitMessage)
        Globals.ui.actionBackup.triggered.connect(Events.saveBackup)
        Globals.ui.actionRestore_Backup.triggered.connect(Events.restoreBackup)
        Globals.ui.actionCustomers.triggered.connect(Events.exportCsvCustomers)


        # lineEdit Functions:
        Globals.ui.txt_DNICliente.editingFinished.connect(Customers.checkDni)
        Globals.ui.txt_emailCliente.editingFinished.connect(lambda: Customers.checkMail(Globals.ui.txt_emailCliente.text()))
        Globals.ui.txt_nombresCliente.editingFinished.connect(lambda: Customers.capitalize(Globals.ui.txt_nombresCliente.text(), Globals.ui.txt_nombresCliente))
        Globals.ui.txt_apellidosCliente.editingFinished.connect(lambda: Customers.capitalize(Globals.ui.txt_apellidosCliente.text(), Globals.ui.txt_apellidosCliente))
        Globals.ui.txt_numeroTelefono.editingFinished.connect(lambda: Customers.checkMobile(Globals.ui.txt_numeroTelefono.text()))

        # comboBox Funtions:
        Events.loadProvinces()
        Globals.ui.cmb_provinciaCliente.currentIndexChanged.connect(Events.loadCities)

        # button Functions:
        Globals.ui.btn_fechaAltaCliente.clicked.connect(Events.openCalendar)
        Globals.ui.btn_delete.clicked.connect(Customers.deleteSelectedCustomer)
        Globals.ui.btn_save.clicked.connect(Customers.saveNewCustomer)
        Globals.ui.btn_modif.clicked.connect(Customers.modifyCustomer)
#        Globals.ui.btn_search.clicked.connect(Customers.searchCustomer)   aún no tengo el botón de busqueda
#        Globals.ui.btn_clean.clicked.connect(Customers.cleanCli)   aún no tengo el botón de limpieza

        # table Functions
        Globals.ui.tbl_customerList.clicked.connect(Customers.showCustomerInfo)

        # check Historical
        Globals.ui.chk_historico.setChecked(True)
        Globals.ui.chk_historico.stateChanged.connect(Customers.customersHistorical)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())