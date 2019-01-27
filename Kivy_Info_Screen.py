from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button 
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from  kivy.uix.image import Image
from firebase import firebase

url = 'https://dwfirebase.firebaseio.com' # URL to Firebase database
token = 'DPY8XMO2SEGntN2kKInAlDmUNXww5L0qmwjXdYFW' # unique token used for authentication
firebase = firebase.FirebaseApplication(url, token)

class MyLabel(Label):
	def __init__(self,**kwargs):
		Label.__init__(self,**kwargs)
		self.bind(size=self.setter('text_size'))
		self.padding=(20,20)

class Infoscreen(App):
	def build(self):
		layout = GridLayout(rows = 2)
		product_image = Image(source = 'trash1.png')
		self.username_input = TextInput()
		label1 = MyLabel(text = 'Here is the information for this trash', font_size=52,halign='justify',valign='middle')
		label2 = MyLabel(text = 'Congratulations your score is 100', font_size=52,halign='justify',valign='middle')
		label3 = MyLabel(text = 'Please input your username here to record your score',font_size=52,halign='justify',valign='middle')
		layout.add_widget(product_image)
		layout.add_widget(label1)
		layout.add_widget(label2)
		layout.add_widget(self.username_input)
		return layout
	def upload_score(self,instance):
		firebase.put('/','Name Test', instance.text)

def start_screen():
	if __name__=='__main__':
		Infoscreen().run()
start_screen()