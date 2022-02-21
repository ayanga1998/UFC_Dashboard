import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg

class MainWindow(qtw.QWidget):
    # TODO: Create combo box for all fighters in the dataset
    # TODO: Store value entered and pull fighter data from the dataset
    # TODO: Create initial plots for skeleton
    # TODO: Add basic images for background

    def __init__(self):
        super().__init__()
        # Add a title
        self.setWindowTitle("UFC Dashboard")

        # Set vertical layout
        self.setLayout(qtw.QVBoxLayout())

        # Create a label
        my_label = qtw.QLabel("Choose your fighter")
        # Change the font size of label
        my_label.setFont(qtg.QFont('Helvetica', 18))
        self.layout().addWidget(my_label)

        # Create an entry box
        my_entry = qtw.QLineEdit()
        my_entry.setObjectName("name_field")
        my_entry.setText("")
        self.layout().addWidget((my_entry))

        # Create a button
        my_button = qtw.QPushButton("Submit", clicked = lambda: press_it())
        self.layout().addWidget(my_button)

        # show our application
        self.show()

        def press_it():
            my_label.setText(my_entry.text())
            # Clear the entry box
            my_entry.setText("")


if __name__ == "__main__":
    app = qtw.QApplication([])
    mw = MainWindow()
    #print(mw.my_entry)
    app.exec()
