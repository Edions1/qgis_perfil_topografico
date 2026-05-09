from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand
from qgis.core import (
    QgsProject,
    QgsCoordinateTransform,
    QgsRaster,
    QgsDistanceArea,
    QgsWkbTypes
)

from PyQt5.QtGui import QColor


class ClickAltitudeTool(QgsMapToolEmitPoint):

    def __init__(self, canvas, raster, plotter):
        super().__init__(canvas)

        self.canvas = canvas
        self.raster = raster
        self.plotter = plotter

        self.prev_point = None
        self.prev_alt = None
        self.total_dist = 0

        self.rubber = QgsRubberBand(self.canvas, QgsWkbTypes.LineGeometry)
        self.rubber.setColor(QColor(0, 255, 65))
        self.rubber.setWidth(2)

        self.dist_calc = QgsDistanceArea()
        self.dist_calc.setSourceCrs(
            QgsProject.instance().crs(),
            QgsProject.instance().transformContext()
        )
        self.dist_calc.setEllipsoid("WGS84")

        self.transform = QgsCoordinateTransform(
            self.canvas.mapSettings().destinationCrs(),
            QgsProject.instance().crs(),
            QgsProject.instance()
        )

    # ==========================================
    def reset(self):
        self.prev_point = None
        self.prev_alt = None
        self.total_dist = 0

        self.plotter.reset()
        self.rubber.reset(QgsWkbTypes.LineGeometry)

    # ==========================================
    def get_altitude(self, point):
        ident = self.raster.dataProvider().identify(
            point,
            QgsRaster.IdentifyFormatValue
        )
        if ident.isValid():
            res = ident.results()
            if res:
                return next(iter(res.values()))
        return 0

    # ==========================================
    def canvasPressEvent(self, event):
        if event.button() == 2:
            self.reset()

    # ==========================================
    def canvasReleaseEvent(self, event):

        point = self.toMapCoordinates(event.pos())
        point_proj = self.transform.transform(point)
        altitude = self.get_altitude(point)

        if self.prev_point is None:
            self.prev_point = point_proj
            self.prev_alt = altitude

            self.plotter.add_point(point_proj.x(), point_proj.y(), 0, altitude)
            self.rubber.addPoint(point)
            self.plotter.update()
            return

        dist = self.dist_calc.measureLine(self.prev_point, point_proj)
        self.total_dist += dist

        self.plotter.add_point(
            point_proj.x(),
            point_proj.y(),
            self.total_dist,
            altitude
        )

        self.rubber.addPoint(point)
        self.plotter.update()

        self.prev_point = point_proj
        self.prev_alt = altitude