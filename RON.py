import matplotlib.pyplot as plt
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button 
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from firebase import firebase
from kivy.uix.image import Image
from GAME_UI_test import start #import the game file

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
        self.layout = FloatLayout()
        Background=Image(source='background.jpeg',
                           pos_hint={'center_x':.5,'center_y':0.5})
        Create = Button(text = "Create an account!", 
                   font_size=30,
                   background_color = (0,0,0,0.3),
                   font_name='OratorStd.otf',
                   size_hint=(0.25,0.06),
                   markup= True,
                   pos_hint={'center_x':.5,'y':0.2},
                   on_press = self.change_to_create)
        Exist = Button(text = "I have an account!",
                   background_color = (0,0,0,0.3),
                   font_size=30,
                   font_name='OratorStd.otf',
                   size_hint=(0.25,0.06),
                   markup= True,
                   pos_hint={'center_x':0.5,'y':0.125},
                   on_press = self.change_to_login)
        self.layout.add_widget(Background)
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
        self.layout_float = FloatLayout()
        Background=Image(source='createscreen.jpeg')
        #Username
        self.layout = GridLayout(cols=2)
        Username = MyLabel(text="")
        self.Username_inp = TextInput(text='',
                                      font_size=55,
                                      multiline=False,
                                      hint_text="Username",
                                      background_color = (0,0,0,0.4),
                                      font_name='OratorStd.otf')
        self.layout.add_widget(Username)
        self.layout.add_widget(self.Username_inp)
        #Password
        Password = MyLabel(text="")
        self.Password_inp = TextInput(text='',
                                      font_size=55,
                                      password=True,
                                      multiline=False,
                                      hint_text="Password",
                                      background_color = (0,0,0,0.4),
                                      font_name='OratorStd.otf')
        self.layout.add_widget(Password)
        self.layout.add_widget(self.Password_inp)
        #Age
        Age = MyLabel(text="")
        self.Age_inp = TextInput(text='',
                                 font_size=55,
                                 font_name='OratorStd.otf',
                                 multiline=False,
                                 hint_text="Age",
                                 background_color = (0,0,0,0.4))
        self.layout.add_widget(Age)
        self.layout.add_widget(self.Age_inp)
        #Create Button
        Create = Button(text="Create!",
                        font_size=55,
                        font_name='Carson D.otf',on_press=self.change_to_created,
                        background_color = (0,0,0,0.3))
        self.layout.add_widget(Create)
        #Back Button
        Back = Button(text="Back",
                      font_size=55,
                      font_name='Carson D.otf',
                      on_press=self.change_to_start,
                      background_color = (0,0,0,0.3))
        self.layout.add_widget(Back)
        self.layout_float.add_widget(Background)
        self.layout_float.add_widget(self.layout)
        self.add_widget(self.layout_float)
        
    def change_to_created(self,value):
        dct = firebase.get("/Account")
        if self.Username_inp.text == '':
            self.Username_inp.hint_text = 'Enter \n your username'
        else:
            if self.Username_inp.text in dct:
                self.Username_inp.text = ''
                self.Username_inp.hint_text = 'Username \n is taken'

        if self.Password_inp.text == '':
            self.Password_inp.hint_text == 'Enter \n your password'
        
        if self.Age_inp.text.isdigit() != True:
            self.Age_inp.text = ''
            self.Age_inp.hint_text = "Invalid Age"
                
        else:
            if self.Username_inp.text not in dct:
                dct = firebase.get("/Account")
                dct[self.Username_inp.text] = {'Password':self.Password_inp.text, 'Age':self.Age_inp.text, 'Profile' : {'Round':'score'}, 'Round':0}
                firebase.put("/", "/Account", dct)
                self.Username_inp.text = ''
                self.Username_inp.hint_text = 'Username'
                self.Password_inp.text = ''
                self.Password_inp.hint_text = 'Password'
                self.Age_inp.text = ''
                self.Age_inp.hint_text = 'Age'
                self.manager.transition.direction = "left"
                self.manager.current = "created"
        
    def change_to_start(self,value):
        self.Username_inp.text = ''
        self.Username_inp.hint_text = 'Username'
        self.Password_inp.text = ''
        self.Password_inp.hint_text = 'Password'
        self.Age_inp.text = ''
        self.Age_inp.hint_text = 'Age'
        self.manager.transition.direction = "right"
        self.manager.current = "start"
        
class CreatedScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        Background = Image(source = 'backgroundtopright.jpeg')
        self.layout1 = FloatLayout()
        self.layout = BoxLayout(orientation='vertical')
        Created = Button(text="Account created! \n Login and Play!",
                         on_press=self.change_to_login,
                         font_name='Carson D.otf',
                         background_color = (0,0,0,0.3),
                         font_size=100)
        self.layout.add_widget(Created)
        self.layout1.add_widget(Background)
        self.layout1.add_widget(self.layout)
        self.add_widget(self.layout1)
        
    def change_to_login(self,value):
        self.manager.transition.direction = "left"
        self.manager.current = "login"
        
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout1 = FloatLayout()
        Background = Image(source = 'backgroundtopright.jpeg')
        #Username
        self.layout = GridLayout(cols=2)
        Username = MyLabel(text="Username",
                           font_size=55,
                           halign='center',
                           valign='middle',
                           font_name='Carson D.otf')
        self.Username_inp = TextInput(text='',
                                      foreground_color = (1,1,1,0.65),
                                      font_size=55,
                                      multiline=False,
                                      hint_text="Username",
                                      background_color = (0,0,0,0.4),
                                      font_name='OratorStd.otf')
        self.layout.add_widget(Username)
        self.layout.add_widget(self.Username_inp)
        #Password
        Password = MyLabel(text="Password",
                           font_size=55,
                           font_name='Carson D.otf',
                           halign='center',
                           valign='middle')
        self.Password_inp = TextInput(text='',
                                      foreground_color = (1,1,1,0.65),
                                      font_name='OratorStd.otf',
                                      font_size=55,
                                      password=True,
                                      multiline=False,
                                      background_color = (0,0,0,0.4),
                                      hint_text="Password")
        self.layout.add_widget(Password)
        self.layout.add_widget(self.Password_inp)
        #Login Button
        Login = Button(text="Login",
                      font_size=55,
                      font_name='Carson D.otf',
                      on_press=self.play_profile,
                      background_color = (0,0,0,0.3))
        #Back Button
        Back = Button(text="Back to Menu",
                      font_size=55,
                      font_name='Carson D.otf',
                      on_press=self.change_to_start,
                      background_color = (0,0,0,0.3))
        self.layout.add_widget(Back)
        self.layout.add_widget(Login)
        self.layout1.add_widget(Background)
        self.layout1.add_widget(self.layout)
        self.add_widget(self.layout1)
    
    def play_profile(self,value):
        #Don't allow user to login/create acc if there is no input
        if self.Username_inp.text == '':
            self.Username_inp.text = ''
            self.Username_inp.hint_text="\n Enter \n your username"
        if self.Password_inp.text == '':
            self.Password_inp.text = ''
            self.Password_inp.hint_text="\n Enter \n your password"
        else:
            #Get all the accounts from firebase
            dct = firebase.get("/Account")
            #If account exisit in firebase
            if self.Username_inp.text in dct:
                #If password matches username of the account, allow login
                if self.Password_inp.text == dct[self.Username_inp.text]['Password']:
                    self.parent.username = self.Username_inp.text
                    self.Username_inp.text = ''
                    self.Password_inp.text = ''
                    self.manager.transition.direction = 'left'
                    self.manager.current= 'play_profile'
                #If not, reset password input
                else:
                    self.Password_inp.hint_text="Password does not match username"
                    self.Password_inp.text = ''
            #If account do not exist in firebase, create new account for them
            else:
                self.Username_inp.hint_text="Invalid Username"
                self.Username_inp.text = ''
                
    def change_to_start(self, value):
        self.Username_inp.text = ''
        self.Password_inp.text = ''
        self.Username_inp.hint_text= 'Username'
        self.Password_inp.hint_text= 'Password'
        self.manager.transition.direction = 'right'
        self.manager.current= 'start'
        
class PlayProfileScreen(Screen):
    
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout2 = FloatLayout()
        Background = Image(source = 'backgroundtopright.jpeg')
        self.layout=BoxLayout(orientation='vertical')
        Profile = Button(text="Profile", 
                         font_size = 55,
                         on_press=self.change_to_profile,
                         font_name='Carson D.otf',
                         background_color = (0,0,0,0.3))
        Play = Button(text = 'Play', 
                      on_press=self.change_to_game,                      
                      font_size=55,
                      font_name='Carson D.otf',
                      background_color = (0,0,0,0.3)) 
        self.layout.add_widget(Play)
        self.layout.add_widget(Profile)
        Back = Button(text="Back", 
                      font_size = 55,
                      on_press=self.change_to_login,
                      font_name='Carson D.otf',
                      background_color = (0,0,0,0.3))
        self.layout.add_widget(Back)
        self.layout2.add_widget(Background)
        self.layout2.add_widget(self.layout)
        self.add_widget(self.layout2)

    def change_to_profile(self,value):
        self.manager.transition.direction = 'left'
        self.manager.current= 'profile'
        
    def change_to_game(self,value):
        all_acc = firebase.get("/Account")
        all_acc[self.parent.username]['Round'] += 1
        all_acc[self.parent.username]['Profile'][all_acc[self.parent.username]['Round']] = 0 #Replace score with actualscotr
        firebase.put('/','/Account',all_acc)
        #Initiate Game
        start()
    def change_to_login(self,value):
        self.manager.transition.direction = 'right'
        self.manager.current= 'login'



class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        Background = Image(source = 'backgroundtopright.jpeg')
        self.layout1 = FloatLayout()
        Back = Button(text = 'Back', 
                      font_name='Carson D.otf',
                      background_color = (0,0,0,0.3),
                      on_press = self.play_profile,
                      font_size = 55)
        Easy = Button(text = 'Easy', 
                      on_press = self.change_to_easy,
                      font_name='Carson D.otf',
                      background_color = (0,0,0,0.3),
                      font_size = 55)
        Medium = Button(text = 'Medium', 
                        on_press = self.change_to_medium,
                        font_name='Carson D.otf',
                        background_color = (0,0,0,0.3),
                        font_size = 55)
        Advanced = Button(text = 'Advanced', 
                          on_press = self.change_to_advanced,
                          font_name='Carson D.otf',
                          background_color = (0,0,0,0.3),
                          font_size = 55)
        self.layout = GridLayout(cols=1)
        self.layout.add_widget(Easy)
        self.layout.add_widget(Medium)
        self.layout.add_widget(Advanced)
        self.layout.add_widget(Back)
        self.layout1.add_widget(Background)
        self.layout1.add_widget(self.layout)
        self.add_widget(self.layout1)
        
    def play_profile(self,value):
        self.manager.transition.direction = 'right'
        self.manager.current= 'play_profile'
        
    def change_to_easy(self,value):
        self.manager.transition.direction = 'left'
        self.manager.current= 'easy'
        
    def change_to_medium(self,value):
        self.manager.transition.direction = 'left'
        self.manager.current= 'medium'
        
    def change_to_advanced(self,value):
        self.manager.transition.direction = 'left'
        self.manager.current= 'advanced'
        
class EasyScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        Background = Image(source = 'backgroundtopright.jpeg')
        self.image = Image(source = 'red.jpeg')
        self.layout2 = FloatLayout()
        self.user_profile = Button(text="Press to reveal \n your progress!",
                                   on_press=self.show_progress,
                                   font_name='Carson D.otf',
                                   background_color = (0,0,0,0.3),
                                   font_size = 55)
        Back = Button(text = 'Back', 
                      on_press = self.change_to_profile,
                      font_name='Carson D.otf',
                      background_color = (0,0,0,0.3),
                      font_size = 55)
        self.layout = GridLayout(cols=2)
        self.layout.add_widget(Back)
        self.layout.add_widget(self.user_profile)
        self.layout1 = GridLayout(cols=1)
        self.layout1.add_widget(self.image)
        self.layout3 = GridLayout(cols=1)
        self.layout3.add_widget(self.layout1)
        self.layout3.add_widget(self.layout)
        self.layout2.add_widget(Background)
        self.layout2.add_widget(self.layout3)
        self.add_widget(self.layout2)
        
    def show_progress(self,button):
        my_acc = firebase.get("/Account/"+self.parent.username+"/Profile")
        rounds = list(my_acc.keys())
        score = list(my_acc.values())
        for i in range(len(rounds)):
            if rounds[i] == 'Round':
                del rounds[i]
                del score [i]
            else:
                rounds[i] = int(rounds[i])
        if len(rounds) < 2:
            self.image.source = 'Profile Message.png'
            self.image.reload()
        else:
            plt.figure().patch.set_facecolor('xkcd:salmon')
            plt.plot(rounds, score, color = (0, 0, 0, 1.0))
            plt.xlabel('No. of Rounds')
            plt.ylabel('Score')
            plt.title('Progress')
            plt.savefig('graph1.png')
            #plt.show()
            self.image.source = 'graph1.png'
            self.image.reload()
    
    def change_to_profile(self,value):
        self.image.source = 'red.jpeg'
        self.image.reload()
        self.manager.transition.direction = 'right'
        self.manager.current= 'profile'
   
class MediumScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout1 = FloatLayout()
        Background = Image(source = 'backgroundbottomright.jpeg')
        self.layout = BoxLayout(orientation='vertical')
        Error = MyLabel(text="Play more and earn higher score \n to unlock this level!",
                        font_size=55,
                        font_name = 'Carson D.otf',
                        halign='center',
                        valign='middle')
        Back = Button(text='Back', 
                      on_press = self.change_to_profile,
                      font_name = 'Carson D.otf',
                      background_color = (0,0,0,0.3),
                      font_size = 55)
        self.layout.add_widget(Error)
        self.layout.add_widget(Back)
        self.layout1.add_widget(Background)
        self.layout1.add_widget(self.layout)
        self.add_widget(self.layout1)
        
    def change_to_profile(self,value):
        self.manager.transition.direction = 'right'
        self.manager.current= 'profile'

class AdvancedScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.layout1 = FloatLayout()
        Background = Image(source = 'backgroundbottomright.jpeg')
        self.layout = BoxLayout(orientation='vertical')
        Error = MyLabel(text="Play more and earn higher score \n to unlock this level!",
                        font_size=55,
                        font_name = 'Carson D.otf',
                        halign='center',
                        valign='middle')
        Back = Button(text='Back', 
                      on_press = self.change_to_profile,
                      font_name = 'Carson D.otf',
                      background_color = (0,0,0,0.3),
                      font_size = 55)
        self.layout.add_widget(Error)
        self.layout.add_widget(Back)
        self.layout1.add_widget(Background)
        self.layout1.add_widget(self.layout)
        self.add_widget(self.layout1)
        
    def change_to_profile(self,value):
        self.manager.transition.direction = 'right'
        self.manager.current= 'profile'

        
class RON(App):
    def build(self):
        sm=ScreenManager()
        es=EasyScreen(name='easy')
        ms=MediumScreen(name='medium')
        hs=AdvancedScreen(name='advanced')
        ls=LoginScreen(name='login')
        pps=PlayProfileScreen(name='play_profile')
        ps=ProfileScreen(name='profile')
        ss=StartScreen(name='start')
        cs=CreateAccount(name='create')
        cds=CreatedScreen(name='created')
        sm.add_widget(ss)
        sm.add_widget(cs)
        sm.add_widget(cds)
        sm.add_widget(ps)
        sm.add_widget(ls)
        sm.add_widget(pps)
        sm.add_widget(es)
        sm.add_widget(ms)
        sm.add_widget(hs)
        sm.current='start'
        return sm

if __name__=='__main__':
	RON().run()
