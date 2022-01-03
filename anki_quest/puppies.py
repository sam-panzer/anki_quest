# Code for managing puppy image reward at a fixed frequency.

import pathlib
import random

from anki import template
import aqt
from aqt import utils as aqt_utils
from aqt import qt

base_addon_dir = pathlib.Path(__file__).parents[0]
user_data_dir = base_addon_dir / "user_files"
image_dir = user_data_dir / "images"
image_suffixes = ('png', 'jpg', 'jpeg')

def get_config():
    return aqt.mw.addonManager.getConfig(__name__) 

def config_value(key):
    return get_config()[key]

class PuppyQuest:

    def __init__(self):
        self.review_count = 0
        self.review_per_reward = 20
        self.puppy_images = [
            p for p in image_dir.iterdir()
            if p.suffix.lstrip('.') in image_suffixes
        ]

    def reviews_per_puppy(self):
        # Load from config each time, in case the user changed it.
        self.review_per_reward = config_value("reviews_per_search") or self.review_per_reward
        return self.review_per_reward

    def remaining_reviews(self):
        return self.reviews_per_puppy() - self.review_count % self.reviews_per_puppy()

    def get_a_puppy_image(self):
        return random.choice(self.puppy_images)

    def puppy_stats(self):
        # Display a stats window.
        dialog = qt.QDialog(aqt.mw.app.activeWindow())
        dialog.setWindowModality(qt.Qt.WindowModality.WindowModal)
        dialog.setWindowTitle("Puppy stats")
        layout = qt.QVBoxLayout()
        dialog.setLayout(layout)
        buttons = qt.QDialogButtonBox(qt.QDialogButtonBox.StandardButton.Ok)
        label = qt.QLabel(f"""
        <div><b>Puppy stats</b>:</div><br>
        <table>
        <tr><td>Cards reviewed:</td> <td>{self.review_count}</td></tr>
        <tr>
            <td>Reviews until next puppy:</td>
            <td>{self.remaining_reviews()}</td>
        </tr>
        </table>
        """)
        layout.addWidget(label)
        layout.addWidget(buttons)
        qt.qconnect(buttons.button(qt.QDialogButtonBox.StandardButton.Ok).clicked,
                    lambda: qt.QDialog.done(dialog, qt.QDialog.Accepted))
        dialog.open()

    def should_reward(self) -> bool:
        return self.review_count % self.reviews_per_puppy() == 0

    def maybe_check_puppies(self, *args) -> None:
        """Increments review and launches triggers."""
        self.review_count += 1
        if not self.should_reward():
            return

        self.show_puppy_dialog()

    def show_puppy_dialog(self) -> None:
        """Displays the main puppy quest display dialog."""

        image_text = f"""
        <img src="{self.get_a_puppy_image()}" height="200">

        <table>
        <tr><td>Cards reviewed:</td> <td>{self.review_count}</td></tr>
        <tr>
          <td>Reviews until next puppy:</td>
          <td>{self.remaining_reviews()}</td>
        </tr>
        </table>
        """

        dialog = qt.QDialog(aqt.mw.app.activeWindow())
        dialog.setWindowModality(qt.Qt.WindowModality.WindowModal)
        dialog.setWindowTitle("Time to check your puppies!")
        layout = qt.QVBoxLayout()
        dialog.setLayout(layout)
        label = qt.QLabel(image_text)
        layout.addWidget(label)
        # The dialog is a simple display at the moment. When the OK button is clicked,
        # just close the dialog.
        buttons = qt.QDialogButtonBox(qt.QDialogButtonBox.StandardButton.Ok)
        layout.addWidget(buttons)
        qt.qconnect(buttons.button(qt.QDialogButtonBox.StandardButton.Ok).clicked,
                    lambda: qt.QDialog.done(dialog, qt.QDialog.Accepted))
        dialog.open()
