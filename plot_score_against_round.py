"""plot for user n his/her score against the number of rounds played"""

import matplotlib.pyplot as plt
from firebase import firebase

url = "https://dwfirebase.firebaseio.com" # URL to Firebase database
token = "DPY8XMO2SEGntN2kKInAlDmUNXww5L0qmwjXdYFW" # unique token used for authentication
firebase = firebase.FirebaseApplication(url, token)

acc = firebase.get("/Account")
acc_info = list(acc.values())
#print(acc_info)
#print(acc_info)
#print(list(acc_info[0]['Profile'].keys()))

rounds = []
score = []
age = []
Age =[]
ageScore = []
ageAv = []
roundScore = []
x_axis = []
y_axis = []


for i in range(len(acc_info)):
    age.append(int(acc_info[i]['Age']))
    rounds.append(list(acc_info[i]['Profile'].keys()))
    score.append(list(acc_info[i]['Profile'].values()))

for n in range(1): #change number 1 with the number which is the index number of the user to see the progress 
    x_axis = []
    y_axis = []
    for m in range(len(rounds[n])-1):
        x_axis.append(rounds[n][m])
        y_axis.append(score[n][m])

plt.scatter(x_axis,y_axis)
plt.show()
