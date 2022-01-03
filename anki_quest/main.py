# Main puppy image setup.
from . import puppies

import aqt
from aqt import qt
from aqt import utils as aqt_utils
from aqt import gui_hooks

# Create puppy quest management.
puppy_quest = puppies.PuppyQuest()

# Create action
puppy_stats_action = qt.QAction("Check Puppies", aqt.mw)
# Wire action into puppy quest.
puppy_stats_action.triggered.connect(puppy_quest.puppy_stats)
# Make new menu entry
quest_menu = qt.QMenu('&AnkiQuest', aqt.mw)
quest_menu.addAction(puppy_stats_action)
aqt.mw.form.menubar.addMenu(quest_menu)
aqt.mw.quest_menu = quest_menu

# Wire puppy quest into Anki's review completed event hook
gui_hooks.reviewer_did_answer_card.append(puppy_quest.maybe_check_puppies)
