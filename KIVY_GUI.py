from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button 
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from firebase import firebase
from GAME_UI_test import start
from Kivy_Info_Screen import start_screen

url = "https://dwfirebase.firebaseio.com" # URL to Firebase database
token = "DPY8XMO2SEGntN2kKInAlDmUNXww5L0qmwjXdYFW" # unique token used for authentication
firebase = firebase.FirebaseApplication(url, token)
class MyLabel(Label):
    def __init__(self,**kwargs):
        Label.__init__(self,**kwargs)
        self.bind(size=self.setter('text_size'))
        self.padding=(20,20)

class StartScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout = BoxLayout(orientation='vertical')
        Create = Button(text = "Create an account!", on_press = self.change_to_create)
        Exist = Button(text = "I have an account!", on_press = self.change_to_login)
        self.layout.add_widget(Create)
        self.layout.add_widget(Exist)
        self.add_widget(self.layout)
        
    def change_to_create(self,value):
        self.manager.transition.direction = 'left'
        self.manager.current= 'create'

    def change_to_login(self,value):
        self.manager.transition.direction = 'left'
        self.manager.current= 'login'
        
class CreateAccount(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        #Username
        self.layout = GridLayout(cols=2)
        Username = MyLabel(text="Username",font_size=24,halign='center',valign='middle')
        self.Username_inp = TextInput(text='',multiline=False,hint_text="Username")
        self.layout.add_widget(Username)
        self.layout.add_widget(self.Username_inp)
        #Password
        Password = MyLabel(text="Password",font_size=24,halign='center',valign='middle')
        self.Password_inp = TextInput(text='',password=True,multiline=False,hint_text="Password")
        self.layout.add_widget(Password)
        self.layout.add_widget(self.Password_inp)
        #Age
        Age = MyLabel(text="How old are you?",font_size=24,halign='center',valign='middle')
        self.Age_inp = TextInput(text='',multiline=False,hint_text="Age")
        self.layout.add_widget(Age)
        self.layout.add_widget(self.Age_inp)
        #Create Button
        Create = Button(text="Create!",on_press=self.next_screen)
        self.layout.add_widget(Create)
        #Back Button
        Back = Button(text="Back", on_press=self.change_to_start)
        self.layout.add_widget(Back)
        self.add_widget(self.layout)
        
    def next_screen(self,value):
        dct = firebase.get("/Account")
        if self.Username_inp.text in dct:
            self.Username_inp.text = ''
            self.Username_inp.hint_text = 'Username is taken'
        else:
            dct = firebase.get("/Account")
            dct[self.Username_inp.text] = {'Password':self.Password_inp.text, 'Age':self.Age_inp.text}
            firebase.put("/", "/Account", dct)
            self.manager.transition.direction = "left"
            self.manager.current = "created"
        
    def change_to_start(self,value):
        self.manager.transition.direction = "right"
        self.manager.current = "start"
        
class CreatedScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout = BoxLayout()
        Created = Button(text="Account created! Let's Play!",on_press=self.change_to_login)
        self.layout.add_widget(Created)
        self.add_widget(self.layout)
        
    def change_to_login(self,value):
        self.manager.transition.direction = "left"
        self.manager.current = "login"
        
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        #Username
        self.layout = GridLayout(cols=2)
        Username = MyLabel(text="Username",font_size=24,halign='center',valign='middle',size_hint=(0.3,0.2))
        self.Username_inp = TextInput(text='',multiline=False,hint_text="Username")
        self.layout.add_widget(Username)
        self.layout.add_widget(self.Username_inp)
        #Password
        Password = MyLabel(text="Password",font_size=24,halign='center',valign='middle')
        self.Password_inp = TextInput(text='',password=True,multiline=False,hint_text="Password")
        self.layout.add_widget(Password)
        self.layout.add_widget(self.Password_inp)
        #Login Button
        Login = Button(text="Login",on_press=self.play_profile)
        self.layout.add_widget(Login)
        #Quit Button
        Back = Button(text="Back", on_press=self.change_to_start)
        self.layout.add_widget(Back)
        self.add_widget(self.layout)
    
    def play_profile(self,value):
        #Don't allow user to login/create acc if there is no input
        if self.Username_inp.text == '':
            self.Username_inp.text = ''
            self.Username_inp.hint_text="Please enter your username"
        if self.Password_inp.text == '':
            self.Password_inp.text = ''
            self.Password_inp.hint_text="Please enter your password"
        else:
            #Get all the accounts from firebase
            dct = firebase.get("/Account")
            #If account exisit in firebase
            if self.Username_inp.text in dct:
                #If password matches username of the account, allow login
                if self.Password_inp.text == dct[self.Username_inp.text]['Password']:
                    self.manager.transition.direction = 'left'
                    self.manager.current= 'play_profile'
                #If not, reset password input
                else:
                    self.Password_inp.hint_text="Password does not match Username"
                    self.Password_inp.text = ''
            #If account do not exist in firebase, create new account for them
            else:
                self.Username_inp.hint_text="Invalid Username"
                self.Username_inp.text = ''
                
    def change_to_start(self, value):
        self.manager.transition.direction = 'right'
        self.manager.current= 'start'
        
class PlayProfileScreen(Screen):
    
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout=BoxLayout(orientation='vertical')
        Profile = Button(text="Profile", on_press=self.change_to_profile)
        Play = Button(text = 'Play', on_press=self.display_round)
        self.layout.add_widget(Play)
        self.layout.add_widget(Profile)
        Quit = Button(text="Quit", on_press=self.quit_app)
        Back = Button(text="Back", on_press=self.change_to_login)
        self.layout1 = GridLayout(cols=2)
        self.layout1.add_widget(Back)
        self.layout1.add_widget(Quit)
        self.layout_tgt = BoxLayout(orientation='vertical')
        self.layout_tgt.add_widget(self.layout)
        self.layout_tgt.add_widget(self.layout1)
        self.add_widget(self.layout_tgt)

    def change_to_profile(self,value):
        self.manager.transition.direction = 'left'
        self.manager.current= 'profile'
        
    def display_round(self,value):
        self.manager.transition.direction = 'left'
        self.manager.current= 'round'
        
    def quit_app(self, value):
        App.get_running_app().stop()
    
    def change_to_login(self,value):
        self.manager.transition.direction = 'right'
        self.manager.current= 'login'



class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout = BoxLayout(orientation='vertical')
        user_profile = MyLabel(text = 'Display Graph',font_size=24,halign='center',valign='middle')
        self.layout1 = GridLayout(cols=2)
        Back = Button(text = 'Back', on_press = self.play_profile)
        Quit = Button(text="Quit", on_press=self.quit_app)
        self.layout.add_widget(user_profile)
        self.layout1.add_widget(Back)
        self.layout1.add_widget(Quit)
        self.layout.add_widget(self.layout1)
        self.add_widget(self.layout)
        
    def play_profile(self, value):
        self.manager.transition.direction = 'right'
        self.manager.current= 'play_profile'
        
    def quit_app(self, value):
        App.get_running_app().stop()

class RoundScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout = GridLayout(cols=2)
        Round = MyLabel(text="How many times have you played RON? (including this time)",font_size=24,halign='center',valign='middle')
        Back = Button(text="Back",on_press=self.play_profile)
        self.label1 = Label(text = 'Click to start')
        self.label1.bind(on_touch_down = self.alternate)
        self.Round_inp = TextInput(text='',multiline=False)
        self.layout.add_widget(Round)
        self.layout.add_widget(self.Round_inp)
        self.layout.add_widget(Back)
        self.layout.add_widget(self.label1)
        self.add_widget(self.layout)
    
    def play_profile(self, value):
        self.manager.transition.direction = 'left'
        self.manager.current= 'play_profile'
    def alternate(self,instance, touch):
        if instance.text == 'Click to start':
            start()
            start_screen()

        
class SwitchScreenApp(App):
    def build(self):
        sm=ScreenManager()
        ms=LoginScreen(name='login')
        pps=PlayProfileScreen(name='play_profile')
        ps=ProfileScreen(name='profile')
        rs=RoundScreen(name='round')
        ss=StartScreen(name='start')
        cs=CreateAccount(name='create')
        cds=CreatedScreen(name='created')
        sm.add_widget(ss)
        sm.add_widget(cs)
        sm.add_widget(cds)
        sm.add_widget(rs)
        sm.add_widget(ps)
        sm.add_widget(ms)
        sm.add_widget(pps)
        sm.current='start'
        return sm

if __name__=='__main__':
	SwitchScreenApp().run()
