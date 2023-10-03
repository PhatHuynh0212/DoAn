import sys
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from TSP_Solver import TSPSolver

class TSPSolverApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TSP Solver With Backtracking")

        # Tạo tọa độ ngẫu nhiên cho các vị trí
        self.num_locations = 6
        self.x_coordinates = [random.uniform(0, 10) for _ in range(self.num_locations)]
        self.y_coordinates = [random.uniform(0, 10) for _ in range(self.num_locations)]

        # Tạo khoảng cách giữa các vị trí
        self.locations = []
        for i in range(self.num_locations):
            row = []
            for j in range(self.num_locations):
                distance = np.sqrt((self.x_coordinates[i] - self.x_coordinates[j]) ** 2 + (self.y_coordinates[i] - self.y_coordinates[j]) ** 2)
                row.append(distance)
            self.locations.append(row)

        # Create the TSP solver instance
        self.solver = TSPSolver(self.locations)

        # Tạo giao diện
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QFormLayout()

        # Tạo label chủ đề đồ án
        self.label = QLabel("Travelling Saleman Problem with Backtracking", self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.label)

        # Tạo label chọn vị trí
        self.label_location = QLabel("Chọn vị trí (điểm) đầu tiên:", self)
        layout.addWidget(self.label_location)

        # Tạo Combobox để chọn vị trí bắt đầu
        self.combo_box = QComboBox(self)
        self.combo_box.setFixedSize(100, 30)
        self.combo_box.addItems([f"Điểm {i + 1}" for i in range(self.num_locations)])
        layout.addWidget(self.combo_box)

        # Tạo nút Solve
        self.solve_button = QPushButton("Thực thi", self)
        self.solve_button.setFixedSize(100, 30)
        self.solve_button.clicked.connect(self.solve_tsp)
        layout.addWidget(self.solve_button)

        # Tạo label để hiển thị kết quả
        self.result_label = QLabel("Kết quả:",self)
        #self.result_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.result_label)

        # Tạo hình và trục cho đồ thị
        self.fig, self.ax = plt.subplots(figsize=(8, 8))

        # Tạo canvas để hiển thị biểu đồ
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        # Thiết lập layout
        central_widget.setLayout(layout)

        # Đồ thị ban đầu của đồ thị
        self.plot_graph([])

    def solve_tsp(self):
        start = self.combo_box.currentIndex()
        path, distance = self.solver.solve_tsp(start)
        best_path = [i + 1 for i in path]
        self.result_label.setText(f"Kết quả:\n- Thứ tự đường đi ngắn nhất: {best_path}\n- Khoảng cách ngắn nhất: {distance:.2f}")
        self.plot_graph(path)

    def plot_graph(self, path):
        self.ax.clear()

        # Vẽ các vị trí dưới dạng điểm
        scatter = self.ax.scatter(self.x_coordinates, self.y_coordinates, c='red', s=50)

        # Vẽ đường dẫn dưới dạng các đường có dấu mũi tên
        for i in range(len(path) - 1):
            start = path[i]
            end = path[i + 1]
            self.ax.annotate("", xy=(self.x_coordinates[end], self.y_coordinates[end]),
                xytext=(self.x_coordinates[start], self.y_coordinates[start]),
                arrowprops=dict(arrowstyle="->", color="blue"))

        # Kết nối tất cả các điểm với các đường đi
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

        # Đặt màu khác cho điểm bắt đầu đã chọn
        if path:
            start_index = path[0]
            scatter.set_facecolors(['cyan' if i == start_index else 'red' for i in range(self.num_locations)])

        # Refresh lại biểu đồ
        self.ax.set_aspect('equal', adjustable='datalim')
        self.canvas.draw()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = TSPSolverApp()
    window.show()
    sys.exit(app.exec_())