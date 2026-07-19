from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QScrollArea, QLabel, QVBoxLayout, QFrame
import pyqtgraph as pg

class Statistics(QWidget):
    def __init__(self, analytics):
        super().__init__()

        self.analytics = analytics
        
        self.initUI()
    
    def initUI(self):
        outer_layout = QVBoxLayout()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        self.layout = QVBoxLayout()   
        container.setLayout(self.layout)

        scroll.setWidget(container)
        outer_layout.addWidget(scroll)

        top_div = QFrame()
        top_div.setMaximumHeight(70)
        top_div.setObjectName("topStats")
        top_div.setStyleSheet("QFrame#topStats {background-color: #242323; border: 1px solid #b0b0b0; border-radius: 5px}")

        top_layout = QVBoxLayout(top_div)

        reviews_today = self.analytics.total_reviews_today()
        label = QLabel(f"Total reviews today (collection-wide): {reviews_today}")
        label.setStyleSheet("font-size: 14px; font-weight: bold; color: #e0e0e0")
        top_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignHCenter)

        daily_streak = self.analytics.calculate_streak()
        label = QLabel(f"Current daily streak 🔥: {daily_streak}")
        label.setStyleSheet("font-size: 12px")
        top_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.layout.addWidget(top_div)

        review_div = QFrame()
        review_div.setObjectName("reviewStats")
        review_div.setStyleSheet("QFrame#reviewStats {background-color: #242323; border: 1px solid #b0b0b0; border-radius: 5px}")

        review_header = QLabel("Review Stats")
        review_header.setStyleSheet("font-size: 16px; font-weight: bold; color: #e0e0e0")

        review_layout = QVBoxLayout(review_div)
        review_layout.addWidget(review_header, alignment=Qt.AlignmentFlag.AlignHCenter)

        reviews_this_week = self.analytics.reviews_this_week()
        label = QLabel(f"Deck reviews this week: {reviews_this_week}")
        review_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignHCenter)

        reviews_this_month = self.analytics.reviews_this_month()
        label = QLabel(f"Deck reviews this month: {reviews_this_month}")
        review_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignHCenter)

        average_time = self.analytics.average_review_time()
        label = QLabel(f"Average review time: {average_time}s")
        review_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignHCenter)

        plot_graph = pg.PlotWidget()
        plot_graph.setFixedSize(500, 400)
        plot_graph.setXRange(1, 12)
        plot_graph.setYRange(0, 100)

        plot_graph.getPlotItem().hideButtons()
        view_box = plot_graph.getPlotItem().getViewBox()
        view_box.setMouseEnabled(x=False, y=False)

        plot_graph.setBackground("#e0e0e0")
        plot_graph.showGrid(x=True, y=True)
        plot_graph.setTitle("Accuracy rate over time", color="#4287f5", size="16px")
        styles = {"color":"black", "font-size": "14px"}
        plot_graph.setLabel("left", "Accuracy", **styles)
        plot_graph.setLabel("bottom", "Month of the year", **styles)
        pen = pg.mkPen(color="#4287f5", width=5, style=Qt.PenStyle.DashLine)

        accuracy_rate = self.analytics.accuracy_rate()
        months = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        rates = [ accuracy_rate[1], accuracy_rate[2], accuracy_rate[3], accuracy_rate[4],
                  accuracy_rate[5], accuracy_rate[6], accuracy_rate[7], accuracy_rate[8],
                  accuracy_rate[9], accuracy_rate[10], accuracy_rate[11], accuracy_rate[12] ]  
        plot_graph.plot(months, rates, pen=pen, symbol="o", symbolSize=8, symbolBrush="k")

        review_layout.addWidget(plot_graph, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        self.layout.addWidget(review_div)

        deck_div = QFrame()
        deck_div.setObjectName("deckStats")
        deck_div.setStyleSheet("QFrame#deckStats {background-color: #242323; border: 1px solid #b0b0b0; border-radius: 5px}")

        deck_header = QLabel("Deck Stats")
        deck_header.setStyleSheet("font-size: 16px; font-weight: bold; color: #e0e0e0")

        deck_layout = QVBoxLayout(deck_div)
        deck_layout.addWidget(deck_header, alignment=Qt.AlignmentFlag.AlignHCenter)

        card_types = self.analytics.card_counts()
        for key, value in card_types.items():
            if key != "deck_id" and key != "name":
                description  = " ".join(key.split("_")).capitalize()
                label = QLabel(f"{description}: {value}")
                deck_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.layout.addWidget(deck_div)

        bottom_div = QFrame()
        bottom_div.setMaximumHeight(50)
        bottom_div.setObjectName("bottomStats")
        bottom_div.setStyleSheet("QFrame#bottomStats {background-color: #4287f5; border-radius: 5px}")

        completion_rate = self.analytics.completion_rate() * 100
        label = QLabel(f"Queue completion rate: {completion_rate}%")
        label.setStyleSheet("font-size: 14px; font-weight: bold; color: #e0e0e0")

        bottom_layout = QVBoxLayout(bottom_div)
        bottom_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.layout.addWidget(bottom_div)
        
        self.setLayout(outer_layout)
        
        

