import os, sys, json, base64, subprocess
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from ui import Ui_Dialog
from req_rc import *


class AqHandlerWindow(QtWidgets.QDialog):
    crashExcCodes = {'ServerConnectionError': 'SCF404',
                     'Other': 'UND000'}

    def __init__(self):
        QtWidgets.QDialog.__init__(self)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)


    def handle(self):
        self.crashLocation = sys.argv[1]
        self.crashReportAddress = sys.argv[2]
        self.crashExcCode = sys.argv[3]
        self.crashedSessionLogFileAddr = sys.argv[4]
        self.crashData = sys.argv[5:]

        if self.crashExcCode in self.crashExcCodes.values():
            if self.crashExcCode == self.crashExcCodes['ServerConnectionError']:
                self.setMaximumSize(400, 230)

                self.ui.lnI_lineEdit.show()
                self.ui.lbl_lineEditTitle.show()
                
                self.ui.lbl_ErrorTitle.setText('Не удалось подключиться к серверу')
                self.ui.lbl_ErrorDesc.setText(f'Сервер по адресу {self.crashData[0]} недоступен. Проверьте, что сервер запущен, что он работает без ошибок; '
                                               'попробуйте перезапустить его.\n\n'
                                               'Также, пожауйста, перепровepьте и укажите верный адрес сервера в поле ниже:')
                self.ui.lbl_lineEditTitle.setText('Адрес сервера:')
                self.ui.lnI_lineEdit.setPlaceholderText('{адрес} или {адрес}:{порт}')

                self.accepted.connect( lambda: self.finish(self.crashExcCodes['ServerConnectionError']) )


            elif self.crashExcCode == self.crashExcCodes['Other']:
                self.setMaximumSize(400, 195)
                
                self.ui.lnI_lineEdit.hide()
                self.ui.lbl_lineEditTitle.hide()

                self.ui.lbl_ErrorTitle.setText('Произошла непредвиденная ошибка')
                self.ui.lbl_ErrorDesc.setText(f'Непревиденная ошибка привела к аварийному прекращению работы {self.crashLocation}. Пожалуйста, помогите '
                                               'нам решить эту проблему: отправьте отчёт об ошибке, нажав Отправить.')

                self.ui.btn_OpenCrashReport.clicked.connect( lambda: self.openCrashReport() )
                self.ui.btn_OpenSessionLog.clicked.connect( lambda: self.openSessionLog() )

                self.accepted.connect( lambda: self.finish(self.crashExcCodes['Other']) )
                self.rejected.connect( lambda: sys.exit() )


            try:
                with open(f'{os.getcwd()}/{self.crashedSessionLogFileAddr}', 'r') as log: pass
            except FileNotFoundError: self.ui.btn_OpenSessionLog.setEnabled(False)

        else: sys.exit()

    
    @staticmethod
    def decryptContent(s):
        return (base64.b64decode(s.encode('utf-8'))).decode('utf-8')

    
    @staticmethod
    def encryptContent(s):
        return (base64.b64encode(s.encode('utf-8'))).decode('utf-8')


    def openCrashReport(self):
        os.startfile(f'{os.getcwd()}/{self.crashReportAddress}')


    def openSessionLog(self):
        os.startfile(f'{os.getcwd()}/{self.crashedSessionLogFileAddr}')


    def finish(self, exceptionCode):
        if exceptionCode == self.crashExcCodes['ServerConnectionError']:
            if not self.ui.lnI_lineEdit.text(): sys.exit()
            else:
                with open('data/config/~!serverdata!~.asqd', 'r') as configFile:
                    fileString = self.decryptContent(configFile.read())

                with open('data/config/~!serverdata!~.asqd', 'w') as configFile: 
                    jsonString = json.loads(fileString)
                    address = self.ui.lnI_lineEdit.text().split(':')
                    if len(address) == 2: jsonString['ip'], jsonString['port'] = address[0], int(address[1])
                    else: jsonString['ip'], jsonString['port'] = address[0], None

                    configFile.write(self.encryptContent(json.dumps(jsonString)))

            sys.exit()

        else: sys.exit()


    def mainloop(self, app: QtWidgets.QApplication):
        self.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    handler = AqHandlerWindow()
    handler.handle()
    handler.mainloop(app)
