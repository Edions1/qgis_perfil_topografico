from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsProject, QgsMapLayer, QgsRaster

from .tool import ClickAltitudeTool
from .plotter import ProfilePlotter


class PerfilTopograficoPlugin:

    def __init__(self, iface):
        self.iface = iface
        self.canvas = iface.mapCanvas()

        self.action = None
        self.tool = None
        self.plotter = None

    def initGui(self):
        self.action = QAction("Perfil Topográfico 3D", self.iface.mainWindow())
        self.action.triggered.connect(self.run)

        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&Perfil Topográfico", self.action)

    def unload(self):
        if self.action:
            self.iface.removeToolBarIcon(self.action)
            self.iface.removePluginMenu("&Perfil Topográfico", self.action)

    def run(self):
        raster = self.get_dem()

        if not raster:
            raise Exception("Nenhum DEM válido encontrado!")

        self.plotter = ProfilePlotter()
        self.tool = ClickAltitudeTool(self.canvas, raster, self.plotter)

        self.canvas.setMapTool(self.tool)

        print("✔ Plugin ativo")

    def get_dem(self):
        for layer in QgsProject.instance().mapLayers().values():
            if layer.type() == QgsMapLayer.RasterLayer:
                provider = layer.dataProvider()
                try:
                    sample = provider.identify(
                        layer.extent().center(),
                        QgsRaster.IdentifyFormatValue
                    )
                    if sample.isValid() and sample.results():
                        return layer
                except:
                    pass

        return None