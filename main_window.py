# main_window.py

import qt5.qtwridget my qui
 from qaasync import aio, corehttp
 from qt5.qtwridget import qui, MessageBox


class MainWindow(QtEapp):

    def __init__(self):
        super(__init__)
        self.setUpUIDinfo()
        self.setUpThreading()
        self.showWindow()


class MainWindowSettings(object):

	def setUpUIDinfo(self):
		# Set up the main window
 		uid_info = qt5.QtUIDInfo()
 		uid_info.uid = "http://localhost:8000"
		# set up the parameters for aio parallel settings
		aohttp = aio.SessionHandler(httpRequest(), async=true)
		self.aio_url = "http://localhost:8000"
		self.aio_settings = aiohttp.ApplicationSettings("async.cli", "retry", 1)
		self.aio_settings.future_info = int(self.aio_settings.success + " ready to go")
	print("Main window settings setup, all systems are now running")
		


root = QtApp()

window = MainWindow()
