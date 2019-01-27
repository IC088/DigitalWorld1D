from pythymiodw import *
from time import sleep
from firebase import firebase

url = 'https://dwfirebase.firebaseio.com' # URL to Firebase database
token = 'DPY8XMO2SEGntN2kKInAlDmUNXww5L0qmwjXdYFW' # unique token used for authentication
firebase = firebase.FirebaseApplication(url, token)

robot = ThymioReal() # create an eBot object

check = True
while check:
	movement = firebase.get('/movement')
	if  movement == 'up':
		firebase.put('/','movement','')
		print('upload done')
		robot.wheels(250,250)
		print('going')
		sleep(1)
		print('stopping')
		robot.wheels(0,0)
	elif  movement == 'down':
		firebase.put('/','movement','')
		robot.wheels(-250,-250)
		sleep(1)
		robot.wheels(0,0)
	elif  movement == 'left':
		firebase.put('/','movement','')
		robot.wheels(-250, 250)
		sleep(1)
		robot.wheels(250,250)
		sleep(1)
		robot.wheels(250, -250)
		sleep(1)
		robot.wheels(0,0)
	elif  movement == 'right':
		firebase.put('/','movement','')
		robot.wheels(250, -250)
		sleep(1)
		robot.wheels(250,250)
		sleep(1)
		robot.wheels(-250, 250)
		sleep(1)
		robot.wheels(0,0)
	
			

# Write the code to control the eBot here

# 'up' movement => robot.wheels(250, 250)
# 'left' movement => robot.wheels(-250, 250)
# 'right' movement => robot.wheels(250, -250)

