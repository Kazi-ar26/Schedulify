"""
Schedulify Chart Components

Reusable visualization components.

Uses:
- PyQtGraph

Handles:
- Productivity charts
- Analytics graphs
- Trend visualization
"""


import pyqtgraph as pg


from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout
)



class LineChart(QWidget):


    def __init__(
        self,
        title: str = "Productivity Trend"
    ):

        super().__init__()


        self.title = title


        self.setup_ui()



    # -------------------------------------------------
    # UI Setup
    # -------------------------------------------------

    def setup_ui(
        self
    ):


        layout = QVBoxLayout()


        self.plot_widget = pg.PlotWidget()


        self.plot_widget.setTitle(
            self.title
        )


        self.plot_widget.showGrid(
            x=True,
            y=True
        )


        layout.addWidget(
            self.plot_widget
        )


        self.setLayout(
            layout
        )



    # -------------------------------------------------
    # Update Chart
    # -------------------------------------------------

    def update_data(
        self,
        values: list[int]
    ):


        self.plot_widget.clear()


        self.plot_widget.plot(

            values,

            symbol="o"

        )



class BarChart(QWidget):


    def __init__(
        self,
        title: str = "Analytics"
    ):

        super().__init__()


        self.title = title


        self.setup_ui()



    # -------------------------------------------------
    # UI Setup
    # -------------------------------------------------

    def setup_ui(
        self
    ):


        layout = QVBoxLayout()


        self.plot_widget = pg.PlotWidget()


        self.plot_widget.setTitle(
            self.title
        )


        self.plot_widget.showGrid(
            x=True,
            y=True
        )


        layout.addWidget(
            self.plot_widget
        )


        self.setLayout(
            layout
        )



    # -------------------------------------------------
    # Update Chart
    # -------------------------------------------------

    def update_data(
        self,
        categories: list[str],
        values: list[int]
    ):


        self.plot_widget.clear()


        x_values = list(

            range(
                len(values)
            )

        )


        self.plot_widget.plot(

            x_values,

            values,

            symbol="o"

        )