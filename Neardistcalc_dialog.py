from qgis.core import QgsVectorLayer, QgsPointXY, QgsDistanceArea
from qgis.PyQt.QtWidgets import QDialog, QMessageBox
import os
from qgis.PyQt import uic
from qgis.PyQt import QtWidgets

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'Neardistcalc_dialog_base.ui'))

class NeardistcalcDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(NeardistcalcDialog, self).__init__(parent)
        self.setupUi(self)
        
        # Connect the button click event to the function that calculates the distance
        self.button_box.accepted.connect(self.calculate_distance)
        self.button_box.rejected.connect(self.close)

    def calculate_distance(self):
        try:
            # Get paths of the shapefiles selected for Point 1 and Point 2
            shapefile_path1 = self.mQgsFileWidget.filePath()
            shapefile_path2 = self.mQgsFileWidget_2.filePath()

            # Load the shapefiles as vector layers
            layer1 = QgsVectorLayer(shapefile_path1, "Point 1", "ogr")
            layer2 = QgsVectorLayer(shapefile_path2, "Point 2", "ogr")

            # Get the first feature (point) from each layer
            point1 = layer1.getFeatures().__next__().geometry().asPoint()
            point2 = layer2.getFeatures().__next__().geometry().asPoint()

            # Calculate distance
            distance = self.calculate_distance_between_points(point1, point2)

            # Display distance in a message box
            QMessageBox.information(self, "Distance Result", f"The distance between the two points is {distance:.2f} meters.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error calculating distance: {str(e)}")

    def calculate_distance_between_points(self, point1, point2):
        distance_area = QgsDistanceArea()
        distance_area.setEllipsoid('WGS84')
        return distance_area.measureLine(QgsPointXY(point1), QgsPointXY(point2))
