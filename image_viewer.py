from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class ImageViewer(QMainWindow):
    def __init__(self, png_path):
        super().__init__()
        self.setWindowTitle("Image Viewer")
        self.showMaximized()

        self.scene = QGraphicsScene()
        self.view = MyGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        self.pixmap_item = QGraphicsPixmapItem(QPixmap(png_path))
        self.scene.addItem(self.pixmap_item)

        self.view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.view.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.view.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

    def wheelEvent(self, event):
        factor = 1.1 if event.angleDelta().y() > 0 else 0.9
        self.view.scale(factor, factor)
        event.accept()

class MyGraphicsView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)

    def wheelEvent(self, event):
        event.ignore()
    

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    viewer = ImageViewer("star_chart_basic.png")  # Example path
    viewer.show()
    sys.exit(app.exec())