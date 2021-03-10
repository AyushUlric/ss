import os
import threading
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.spinner import MDSpinner
from kivymd.toast import toast
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.lang import Builder
from kivymd.uix.filemanager import MDFileManager
from kivy.utils import platform

if platform=='android':
	from android.permissions import request_permissions, Permission, check_permission
	from android.storage import primary_external_storage_path
	primary_ext_storage = primary_external_storage_path()
else:
	primary_ext_storage = os.getcwd()

import pyrebase

config = {
  "apiKey": "AIzaSyDrk0fs498an6ECXJvDYql7JMAnNqT6QNs",
  "authDomain": "kali-project-d40fc.firebaseapp.com",
  "databaseURL": "https://kali-project-d40fc-default-rtdb.firebaseio.com",
  "storageBucket": "kali-project-d40fc.appspot.com"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

default_img = './default.png'
class ScreenManager(ScreenManager): pass

class FirstScreen(Screen): pass

class UploadScreen(Screen):

	def update(self):
		self.spinner = MDSpinner(
					size_hint=(None, None),
					pos_hint={'center_x': .5, 'center_y': .5},
					active=True
				)
		self.add_widget(self.spinner)
		update_thread = threading.Thread(target=self.Update)
		toast("uploading files this may take some time.")
		update_thread.start()
	
	def Update(self):
		try:
			for key,val in Test().my_dict.items():
				storage.child(f'Flutter/{key}.png').put(val)
			Test().my_dict = {}
			toast("Files Updated Successfully")
		except Exception as e:
			toast("Error " + e)
		self.spinner.active = False
		

class RemoveScreen(Screen):
	pass
	
class Test(MDApp):
	my_dict = {}
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Window.bind(on_keyboard=self.events)
		self.manager_open = False
		self.file_manager = MDFileManager(
			exit_manager=self.exit_manager,
			select_path=self.select_path)

	def build(self):
		while not check_permission('android.permission.WRITE_EXTERNAL_STORAGE'):
				request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
		self.theme_cls.primary_palette = "Blue"
		master = Builder.load_file('main.kv')
		self.val = 0
		return master

	def file_manager_open(self, val):
		self.val = val
		self.file_manager.show(primary_ext_storage)  # output manager to the screen
		self.manager_open = True

	def select_path(self, path_returned):
		if path_returned.split('.')[-1] in ['png','jpg','jpeg','webp']:
			self.B_G_IMG = path_returned
			path = path_returned
			self.my_dict[self.val] = path
			toast("pages " + (' ,'.join([str(x) for x in self.my_dict.keys()])) + " added!")
		else:
			toast('Invaid file format (file can be of png, jpg, jpeg only)')
		self.exit_manager()
		
	def exit_manager(self, *args):
		self.manager_open = False
		self.file_manager.close()

	def on_pause(self):
		return True

	def events(self, window, key, *args):
		if key==27:
			if self.root.current == 'first_screen':
				self.on_pause()
			elif self.root.current == 'upload_screen':
				self.root.current = 'first_screen'
			elif self.root.current == 'remove_screen':
				self.root.current = 'first_screen'
		return True

	def remove_all(self):
		self.spinner2 = MDSpinner(
					size_hint=(None, None),
					pos_hint={'center_x': .5, 'center_y': .5},
					active=True
				)
		self.root.ids.remove_screen.add_widget(self.spinner2)
		st = threading.Thread(target=self._remove_all, daemon=True)
		toast("Removing all Files.\nPlease wait.")
		st.start()

	def _remove_all(self):
		try:
			for i in range(1,16):
				storage.child(f'Flutter/{i}.png').put(default_img)
			toast("All files deleted Successfuly")
		except Exception as e:
			toast("Error: " + e)
		self.spinner2.active = False

	def remove(self, val):
		self.spinner3 = MDSpinner(
					size_hint=(None, None),
					pos_hint={'center_x': .5, 'center_y': .5},
					active=True
				)
		self.root.ids.remove_screen.add_widget(self.spinner3)
		st = threading.Thread(target=self._remove,args=(val,), daemon=True)
		toast(f"Removing page {val}.\nPlease wait.")
		st.start()

	def _remove(self, val):
		try:
			storage.child(f'Flutter/{val}.png').put(default_img)
			toast(f"Page {val} deleted Successfuly")
		except Exception as e:
			toast("Error: " + e)
		self.spinner3.active = False
	
Test().run()