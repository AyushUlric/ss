from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.utils import platform
if platform=='android':
	from android.context import Context
	from android.support.v7.app import AppCompatActivity
	from android.os import Bundle
	from android.view import WindowManager

class Test(MDApp):

	def build(self):
		if platform=='android':
			getWindow().setFlags(WindowManager.LayoutParams.FLAG_SECURE,
					WindowManager.LayoutParams.FLAG_SECURE)

Test().run()