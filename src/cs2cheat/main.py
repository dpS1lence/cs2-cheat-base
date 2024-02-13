from PyQt5.QtWidgets import QApplication
import sys
import threading
from overlay import Overlay
from triggerbot import TriggerBot
import time


def run_overlay():
    app = QApplication(sys.argv)
    game_title = "Counter-Strike 2"
    overlay = Overlay(game_title)
    overlay.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    """overlay_thread = threading.Thread(target=run_overlay, daemon=True)
    overlay_thread.start()"""

    trigger_bot = TriggerBot(trigger_key="shift")
    trigger_bot.start()
    try:
        while True:
            """enemy_positions = get_enemy_positions()
            overlay_thread.set_enemy_positions(enemy_positions)"""

            time.sleep(0.1)
    except KeyboardInterrupt:
        trigger_bot.stop()
