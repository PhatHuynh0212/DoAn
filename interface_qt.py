import sys
import random
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from TSP_Backtracking import TSPBacktracking

class TSPSolverApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TSP Solver Python")

        # Tọa độ ngẫu nhiên cho các điểm
        self.num_locations = 6
        self.x_coordinates = [random.uniform(0, 10) for _ in range(self.num_locations)]
        self.y_coordinates = [random.uniform(0, 10) for _ in range(self.num_locations)]

        # Khoảng cách giữa các điểm
        self.locations = []
        for i in range(self.num_locations):
            row = []
            for j in range(self.num_locations):
                distance = np.sqrt((self.x_coordinates[i] - self.x_coordinates[j]) ** 2 + (self.y_coordinates[i] - self.y_coordinates[j]) ** 2)
                row.append(distance)
            self.locations.append(row)

        self.solver = TSPBacktracking(self.locations)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QFormLayout()

        # Đặt biểu tượng cho ứng dụng
        app_icon = QIcon("icon.png")
        app.setWindowIcon(app_icon)

        # Label chủ đề đồ án
        self.label = QLabel("Travelling Saleman Problem with Backtracking", self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 14, QFont.Bold))
        self.label.setStyleSheet("color: red")
        layout.addWidget(self.label)

        # Label chọn vị trí
        self.label_location = QLabel("Chọn vị trí (điểm) đầu tiên:", self)
        self.label_location.setFont(QFont("Arial", 10))
        layout.addWidget(self.label_location)

        # Combobox để chọn vị trí bắt đầu
        self.combo_box = QComboBox(self)
        self.combo_box.setFixedSize(120, 30)
        self.combo_box.setFont(QFont("Arial", 10))
        self.combo_box.addItems([f"Điểm {i + 1}" for i in range(self.num_locations)])
        layout.addWidget(self.combo_box)

        # Nút thực thi
        self.solve_button = QPushButton("Thực thi", self)
        self.solve_button.mapFrom
        self.solve_button.setFixedSize(120, 40)
        self.solve_button.setFont(QFont("Arial", 10))
        self.solve_button.setStyleSheet("background-color: #008CBA; color: white; border-radius: 20px;")
        self.solve_button.clicked.connect(self.solve_tsp)
        layout.addWidget(self.solve_button)

        # Label để hiển thị kết quả
        self.result_label = QLabel("Kết quả:",self)
        self.result_label.setFont(QFont("Arial", 10))
        layout.addWidget(self.result_label)

        # Vẽ đồ thị
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)
        central_widget.setLayout(layout)
        self.plot_graph([])

    def solve_tsp(self):
        start = self.combo_box.currentIndex()
        path, distance = self.solver.solve_tsp(start)
        best_path = [i + 1 for i in path]
        self.result_label.setText(f"Kết quả:\n- Thứ tự đường đi ngắn nhất: {best_path}\n- Khoảng cách ngắn nhất: {distance:.2f}")
        self.plot_graph(path)

    def plot_graph(self, path):
        self.ax.clear()
        scatter = self.ax.scatter(self.x_coordinates, self.y_coordinates, c='red', s=40)

        for i in range(len(path) - 1):
            start = path[i]
            end = path[i + 1]
            self.ax.annotate("", xy=(self.x_coordinates[end], self.y_coordinates[end]),
                xytext=(self.x_coordinates[start], self.y_coordinates[start]),
                arrowprops=dict(arrowstyle="->", color="blue"))

        for i in range(self.num_locations):
            for j in range(i + 1, self.num_locations):
                x_start = self.x_coordinates[i]
                y_start = self.y_coordinates[i]
                x_end = self.x_coordinates[j]
                y_end = self.y_coordinates[j]
                distance = self.locations[i][j]
                place_names = [f"Điểm {k + 1}" for k in range(self.num_locations)]
                self.ax.plot([x_start, x_end], [y_start, y_end], 'k--', alpha=0.2)
                self.ax.text((x_start + x_end) / 2, (y_start + y_end) / 2, f"{distance:.2f}", ha='center', va='center')
                if j == self.num_locations - 1:
                    self.ax.text(x_end, y_end, place_names[j], ha='left', va='bottom')
                self.ax.text(self.x_coordinates[i], self.y_coordinates[i], place_names[i], ha='right', va='top')

        if path:
            start_index = path[0]
            scatter.set_facecolors(['cyan' if i == start_index else 'red' for i in range(self.num_locations)])

        self.ax.set_aspect('equal', adjustable='datalim')
        self.canvas.draw()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = TSPSolverApp()
    window.show()
    sys.exit(app.exec_())