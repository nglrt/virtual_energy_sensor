#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
from ui.SettingsDialog import Ui_SettingsDialog
from ui.DeviceInformation import Ui_DeviceInformation
import os
import tasks
from blinker import signal
import logging
from backend import CollectDataAndUploadWorker
import sys
import signal as sig
from config import Configuration
import random
from benchmark.cpu import run_benchmark as run_cpu_benchmark
from benchmark.network import run_benchmark as run_network_benchmark
from benchmark.testdisk import run_benchmark as run_disk_benchmark
from benchmark.backlight import run_benchmark as run_backlight_benchmark
import threading
import time

sig.signal(sig.SIGINT, sig.SIG_DFL)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.realpath(__file__))
        
    return os.path.join(base_path, relative_path)


class SettingsDialog(QtGui.QWidget):
    def __init__(self, config):
        QtGui.QWidget.__init__(self)
        self.config = config

        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)

        self._init_values(self.config)

        self.ui.btSelectPath.clicked.connect(self._on_path_select)
        self.ui.btSave.clicked.connect(self._on_save)
        self.ui.btCancel.clicked.connect(self.hide)
        self.setWindowTitle("Einstellungen")

    def _init_values(self, config):
        assert isinstance(self.ui, Ui_SettingsDialog)
        self.ui.cbActivateDataCollection.setChecked(config.activated)
        self.ui.cbActivateLocalStorage.setChecked(config.local_storage_activated)
        self.ui.lPlugwiseHost.setText(config.plugwise_server)
        self.ui.lUpstreamHost.setText(config.upstream_server)
        self.ui.lLocalStorage.setText(config.local_storage)
        self.ui.lMacAddress.setText(config.plugwise_mac_address)
        self.ui.lComputerName.setText(config.computer_name)

    def _on_path_select(self):
        dir_ = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
        if os.path.isdir(dir_):
            self.ui.lLocalStorage.setText(dir_)

    def closeEvent(self,event):
        logging.info( "Caught close event. Do nothing... ")
        event.ignore()
        self.hide()

    def _on_save(self):
        self.config.local_storage = str(self.ui.lLocalStorage.text())
        self.config.activated = self.ui.cbActivateDataCollection.isChecked()
        self.config.local_storage_activated = self.ui.cbActivateLocalStorage.isChecked()
        self.config.plugwise_server = str(self.ui.lPlugwiseHost.text())
        self.config.upstream_server = str(self.ui.lUpstreamHost.text())
        self.config.plugwise_mac_address = str(self.ui.lMacAddress.text())
        self.config.computer_name = str(self.ui.lComputerName.text())

        self.config.save()
        signal("config.changed").send()

        self.hide()

class InfoDialog(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.ui = Ui_DeviceInformation()
        self.ui.setupUi(self)
        info = tasks.DeviceInfoTask()
        self.ui.teInfo.setText(info())
        self.ui.btClose.clicked.connect(self.hide)
        self.setWindowTitle(u"Geräteinformationen")

    def closeEvent(self,event):
        logging.debug("Caught close event. Do nothing... ")
        event.ignore()
        self.hide()

class SystemTrayIcon(QtGui.QSystemTrayIcon):
    plugwise_status_change = QtCore.pyqtSignal([str])
    uploader_status_change = QtCore.pyqtSignal([str])

    def _add_tag(self, tag_name, verbose_name):
        self.tags[tag_name] = self.tag_action_group.addAction(QtGui.QAction(verbose_name, None, checkable=True))
        self.tag_menu.addAction(self.tags[tag_name])
        self.tags[tag_name].setData(tag_name)
        self.tags[tag_name].triggered.connect(self._on_tag_change)
    
    def __init__(self, icon, config, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        self.menu = QtGui.QMenu(parent)
        self.config = config
        
        self.tag_menu = self.menu.addMenu("Tag")
        self.tag_action_group = QtGui.QActionGroup(parent, exclusive=True)
        
        self.tags = {}
        
        self._add_tag("default", "Default")
        self._add_tag("training", "Training")
        self._add_tag("training2", "Training 2")
        self._add_tag("training3", "Training 3")
        self._add_tag("training4", "Training 4")
        self._add_tag("training5", "Training 5")
        self._add_tag("long_term", "Long Term")
        self._add_tag("long_term2", "Long Term2")
        self._add_tag("training2", "Training 2")
        
        self.tags[config.tag].setChecked(True)
        
        self.benchmark = self.menu.addAction(u"Benchmark durchführen")
        self.benchmark.triggered.connect(self.on_benchmark)        
        
        self.menu.addSeparator()
        
        self.deviceInfo = self.menu.addAction(u"Geräteinformationen")
        self.deviceInfo.triggered.connect(self.on_info_click)

        self.settings = self.menu.addAction("Einstellungen")
        self.settings.triggered.connect(self.on_settings_edit)
        
        self.menu.addSeparator()
        
        self.plugwiseStatusAction = self.menu.addAction("Plugwise: unbekannt")
        
        self.upstreamServerStatus = self.menu.addAction("Upload: unbekannt")
        
        self.menu.addSeparator()
        
        self.exitAction = self.menu.addAction("Beenden")
        self.exitAction.triggered.connect( QtGui.qApp.quit )
        
        self.setContextMenu(self.menu)

        self.plugwise_status = signal("plugwise.status")
        self.plugwise_status.connect(self.on_plugwise_status_change_async)
        self.plugwise_status_change.connect(self.on_plugwise_status_change)

        self.uploader_status = signal("uploader.status")
        self.uploader_status.connect(self.on_uploader_status_change_async)
        self.uploader_status_change.connect(self.on_uploader_status_change)

    def on_benchmark(self):
        self.old_tag = self.config.tag
        
        self.config.tag = "benchmark_%s" % random.randint(0, 1000)
        signal("config.changed").send()
        
        logging.info("Tag is %s" % self.config.tag)        
        print("Tag is %s" % self.config.tag) 
        
        self.benchmark_thread = threading.Thread(target=self.run_benchmark)
        self.benchmark_thread.start()
                
    def run_benchmark(self):
        
        self.benchmark.setText(u"Benchmark läuft")
        
        logging.info("Idle 60s benchmark")
        time.sleep(60)        
        
        logging.info("Running CPU benchmark")
        run_cpu_benchmark()
        
        logging.info("Running Network benchmark")        
        run_network_benchmark()
        
        logging.info("Running Disk benchmark") 
        run_disk_benchmark()        
        
        logging.info("Running Backlight benchmark")
        run_backlight_benchmark()
        
        logging.info("Idle 60s benchmark")
        time.sleep(60)  
        
        logging.info("Benchmarks done")
        self.benchmark.setText("Benchmark abgeschlossen")
        
        self.config.tag = self.old_tag
        self.config.save()
        signal("config.changed").send()
    
    def _on_tag_change(self, *args, **kwargs):
        tag = self.sender().data().toPyObject()
        self.config.tag = str(tag)
        self.config.save()
        signal("config.changed").send()
    
    def on_uploader_status_change_async(self, msg):
        self.uploader_status_change.emit(msg)

    def on_uploader_status_change(self, msg):
        self.upstreamServerStatus.setText("Upload: {0}".format(msg))

    def on_plugwise_status_change_async(self, msg):
        self.plugwise_status_change.emit(msg)

    def on_plugwise_status_change(self, msg):
        self.plugwiseStatusAction.setText("Plugwise: {0}".format(msg))

    def on_info_click(self):
        self.info_dialog = InfoDialog()
        self.info_dialog.show()

    def on_settings_edit(self):
        self.settingsDialog = SettingsDialog(self.config)
        self.settingsDialog.show()

class App(object):    
    
    def __init__(self):
        self.config = Configuration.load()

                
        
        self.app = QtGui.QApplication(sys.argv)
        self.style = self.app.style()
        #self.icon = QtGui.QIcon(self.style.standardPixmap(QtGui.QStyle.SP_FileIcon))
        
        self.icon = QtGui.QIcon(resource_path("ui/icon.png"))
        self.trayIcon = SystemTrayIcon(self.icon, self.config)

        self.trayIcon.show()
        self.worker = CollectDataAndUploadWorker(self.config)

    def __enter__(self):
        pass
        
    def __exit__(self, *args, **kwargs):
        logging.info("Exiting")
        self.trayIcon.hide()
        self.worker.__exit__()

    def run(self):
        return self.app.exec_()

path = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(
filename = os.path.join(path, "data_collector_gui.log"),
level = logging.DEBUG,
format = '[collector-gui] %(levelname)-7.7s %(message)s'
)

if __name__ == '__main__':
    logging.info("  **   Data Collector is starting   **")    
    
    m = App()
    with m:
        result = m.run()
    
    exit(0)
