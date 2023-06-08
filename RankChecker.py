import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QLineEdit, QPushButton, QVBoxLayout, QMainWindow
from PyQt6.QtCore import Qt
from riotwatcher import LolWatcher, ApiError

lol = LolWatcher("RGAPI-8b6f7996-c460-4a33-8d55-e946c27239d3")
region = "na1"
me = lol.summoner.by_name(region, "tortwig")
print(me)
rank = lol.league.by_summoner(region, me["id"])
print(rank)
ret = None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bruh")

        self.title = QLabel("Find Solo Queue Rank", self)
        self.title.setGeometry(10, 10, 200, 30)

        self.input_field = QLineEdit(self)
        self.input_field.setGeometry(10, 50, 200, 30)

        button = QPushButton("Find Summoner", self)
        button.setGeometry(10, 90, 200, 30)
        button.clicked.connect(self.button_clicked)

        self.display_label = QLabel(self)
        self.display_label.setGeometry(10, 130, 200, 30)

    def button_clicked(self):
        name = self.input_field.text()
        try:
            user = lol.summoner.by_name(region, name)
            rank = lol.league.by_summoner(region, user["id"])
            for x in rank:
                if x["queueType"] == "RANKED_SOLO_5x5":
                    self.display_label.setText("Your rank is: " + x["tier"] + " " + str(x["leaguePoints"]) + "LP")
                    return
            self.display_label.setText("No Ranked Solo games found")
            
        except ApiError as err:
            self.display_label.setText("Summoner not found")
        
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())