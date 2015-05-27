# -*- coding: utf-8 -*-
"""
/***************************************************************************
 WCSViewer
                                 A QGIS plugin
 WCSViewer for wcs 2.0
                             -------------------
        begin                : 2015-05-27
        copyright            : (C) 2015 by Raphael Willian da Costa - INPE
        email                : raphael.costa5@dpi.inpe.br
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load WCSViewer class from file WCSViewer.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .wcs_viewer import WCSViewer
    return WCSViewer(iface)
