import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QCheckBox, QLabel, QLineEdit, QPushButton
import main  # Assuming main.py contains your PyVISA logic


class CheckBoxExample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 CheckBox Example")
        self.setGeometry(100, 100, 400, 300)

        # Main Widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Layout
        layout = QVBoxLayout()

        # Input for CMW IP
        self.label = QLabel("Enter CMW IP:")
        layout.addWidget(self.label)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("e.g., 192.10.11.12")
        layout.addWidget(self.input_field)

        # Checkboxes for Bands
        self.band_label = QLabel("Select the Band (Frequency):")
        layout.addWidget(self.band_label)

        self.band_checkboxes = {
            "Band1": QCheckBox("Band1"),
            "Band3": QCheckBox("Band3: 1840 MHz"),
            "Band5": QCheckBox("Band5: 880 MHz"),
            "Band8": QCheckBox("Band8: 940 MHz"),
        }
        for checkbox in self.band_checkboxes.values():
            layout.addWidget(checkbox)

        # Checkboxes for Spans
        self.span_label = QLabel("Select the Span (Frequency):")
        layout.addWidget(self.span_label)

        self.span_checkboxes = {
            "Span1": QCheckBox("Span1: 0.1 MHz"),
            "Span2": QCheckBox("Span2: 20 MHz"),
            "Span3": QCheckBox("Span3: 100 MHz"),
            "Span4": QCheckBox("Span4: 200 MHz"),
        }
        for checkbox in self.span_checkboxes.values():
            layout.addWidget(checkbox)

        # Reset Button
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_fields)
        layout.addWidget(self.reset_button)

        # Submit Button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_data)
        layout.addWidget(self.submit_button)

        # Output Label
        self.output_label = QLabel("Output will appear here.")
        layout.addWidget(self.output_label)

        # Set Layout
        main_widget.setLayout(layout)

    def reset_fields(self):
        """Reset all checkboxes and input fields."""
        for checkbox in self.band_checkboxes.values():
            checkbox.setChecked(False)
        for checkbox in self.span_checkboxes.values():
            checkbox.setChecked(False)
        self.input_field.clear()
        self.output_label.setText("Output will appear here.")

    def submit_data(self):
        """Submit the data and call the main logic."""
        selected_bands = [key for key, checkbox in self.band_checkboxes.items() if checkbox.isChecked()]
        selected_spans = [key for key, checkbox in self.span_checkboxes.items() if checkbox.isChecked()]
        cmw_ip = self.input_field.text()

        if not cmw_ip:
            self.output_label.setText("Please enter a valid CMW IP.")
            return

        if not selected_bands and not selected_spans:
            self.output_label.setText("No options selected.")
            return

        self.output_label.setText(f"Selected Bands: {', '.join(selected_bands)} | Spans: {', '.join(selected_spans)}")

        # Call main.py logic
        main.run_main_logic(selected_bands, selected_spans, cmw_ip)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CheckBoxExample()
    window.show()
    sys.exit(app.exec_())
