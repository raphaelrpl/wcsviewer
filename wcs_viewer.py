# -*- coding: utf-8 -*-
"""
/***************************************************************************
 WCSViewer
                                 A QGIS plugin
 WCSViewer for wcs 2.0
                              -------------------
        begin                : 2015-05-27
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Raphael Willian da Costa - INPE
        email                : raphael.costa5@dpi.inpe.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from twisted.internet.tcp import _AbortingMixin
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, SIGNAL
from PyQt4.QtCore import QObject
from PyQt4.QtGui import QAction, QIcon, QMessageBox, QToolTip, QFont
# Initialize Qt resources from file resources.py
from qgis._gui import QgsMapToolEmitPoint

import resources_rc

# Import the code for the dialog
from wcs_viewer_dialog import WCSViewerDialog
import os.path


# LIBS
from libs.pyogc import WCS
from dateutil import parser
from datetime import timedelta

# matplot
import matplotlib.pyplot as plt
from mpldatacursor import datacursor


class WCSViewer:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        self.canvas = self.iface.mapCanvas()
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'WCSViewer_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = WCSViewerDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&WCSViewer')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'WCSViewer')
        self.toolbar.setObjectName(u'WCSViewer')

        self.wcs = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('WCSViewer', message)

    def add_action(self, icon_path, text, callback, enabled_flag=True, add_to_menu=True, add_to_toolbar=True,
                   status_tip=None, whats_this=None, parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/WCSViewer/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'WCSViewer'),
            callback=self.run,
            parent=self.iface.mainWindow())
        self.clickTool = QgsMapToolEmitPoint(self.canvas)

        QObject.connect(self.dlg.sendRequestBtn, SIGNAL("clicked()"), self.start_wcs_request)

        # Connect SciDB GetCoverage
        QObject.connect(self.dlg.sendGetCoverage, SIGNAL("clicked()"), self.get_coverage)

        # Onchange ComboCoverage
        QObject.connect(self.dlg.comboCoverage, SIGNAL("currentIndexChanged(int)"), self.on_change_combo_coverage)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&WCSViewer'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def get_bands(self, coverageID):
        if not self.wcs:
            QMessageBox.information(self.iface.mainWindow(), "Error", "Set configuration on \"Configuration\" tab")
            return
        self.wcs.describe_coverage(coverage_id=coverageID)
        return self.wcs.attributes

    def on_change_combo_coverage(self, obj):
        print("TA AQUI")
        data = self.get_bands(coverageID=self.dlg.comboCoverage.currentText())
        if data:
            for product_dct in data:
                if product_dct.get('name') == self.dlg.comboCoverage.currentText():
                    text = ",".join(product_dct['bands'])
                    self.dlg.bandsInput.setPlaceholderText(text)
                    self.dlg.bandsInput.setToolTip(text)
                    break
        print(data)
        # ADD BANDS TO BANDSINPUT PLACEHOLDER
        self.start_date = self.wcs.start_date
        self.end_date = self.wcs.end_date
        self.dlg.startDateInput.setPlaceholderText(self.wcs.start_date)
        self.dlg.endDateInput.setPlaceholderText(self.wcs.end_date)

    def start_wcs_request(self):
        self.dlg.textOutput.setText("")
        self.dlg.textOutput.append("Trying connect on \"%s\"" % self.dlg.lineEdit.text())
        self.wcs = WCS(url=self.dlg.lineEdit.text(), version="2.0.1")
        self.wcs.get_capabilities()
        self.dlg.textOutput.append("Connection established.")
        self.dlg.capabilitiesOutput.setText("")
        self.dlg.capabilitiesOutput.append(self.wcs.data.content)
        self.dlg.comboCoverage.clear()
        if self.wcs.xml:
            coverages = self.wcs.xml.xpath(".//wcs:CoverageId", namespaces=self.wcs.xml.nsmap)
        else:
            coverages = []
        for coverage in coverages:
            self.dlg.comboCoverage.addItem(coverage.text)
        # QMessageBox.information(self.iface.mainWindow(), "DEBUG:", )

    def get_coverage(self):
        if not self.wcs:
            QMessageBox.information(self.iface.mainWindow(), "Error", "Set configuration on \"Configuration\" tab")
            return
        wcs_params = {}
        rangesubset = self.dlg.bandsInput.text()
        if rangesubset:
            wcs_params['rangesubset'] = rangesubset
            # self.wcs.get_coverage(coverage_id=self.dlg.comboCoverage.currentText(), rangesubset=rangesubset)
        start_date = self.dlg.startDateInput.text() or self.start_date
        end_date = self.dlg.endDateInput.text() or self.end_date

        wcs_params['subset'] = "time_id(%s,%s)" % (str(start_date), str(end_date))

        self.wcs.get_coverage(coverage_id=self.dlg.comboCoverage.currentText(), **wcs_params)
        self.dlg.dataOutput.setText("")
        self.dlg.dataOutput.append(self.wcs.values)

        data_strings = ""

        elements = self.wcs.values.split(',')
        bands_values = [e.lstrip().split(' ') for e in elements]

        bands_it = len(elements[0].split(' '))

        # plot (use with subplot)
        # figure = plt.figure()

        begin_date = parser.parse(start_date)
        final_date = parser.parse(end_date)
        dates = []
        period = int(self.wcs.period)

        while begin_date <= final_date:
            dates.append(begin_date)
            begin_date += timedelta(days=period)

        print(dates)

        for i in xrange(bands_it):
            array = []
            for element in bands_values:
                array.append(int(element[i]))
                data_strings += element[i].lstrip()

            # Uncomment next lines to enable one graph per band
            # ax = figure.add_subplot(bands_it, 1, i)
            # ax.set_title('b1')
            # plt.plot(array)

            plt.plot(array, marker='o')

        datacursor(hover=True)
        self.dlg.dataOutput.setText(data_strings)
        plt.show()

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
