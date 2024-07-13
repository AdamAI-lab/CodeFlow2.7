import sys
import asyncio
from PyQt5.QtWidgets import QApplication
from qasync import QEventLoop
from gui.main_window import CombinedAgentApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    combined_agent = CombinedAgentApp()
    combined_agent.show()
    with loop:
        loop.run_forever()
