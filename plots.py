"""plot for nth round, score against age group"""

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


for n in range(len(score)):
    roundScore.append(score[n][0])

for o in range(len(age)):
    if [age[o]] not in ageScore:
        ageScore.append([age[o]])
        Age.append(age[o])
    else:
        None

for p in range(len(ageScore)):
    ageScore[p].append([])

for q in range(len(Age)):
    for r in range(len(age)):
        if age[r] == Age[q]:
            ageScore[q][1].append(roundScore[r])
 
           
for s in range(len(ageScore)):
    av = 0
    total = 0
    ageAv.append([ageScore[s][0]])
    for m in range(len(ageScore[s][1])):
        total += ageScore[s][1][m]
    av = total / len(ageScore[s][1])
    ageAv[s].append(av)

for t in range(len(ageAv)):
    x_axis.append(ageAv[t][0])
    y_axis.append(ageAv[t][1])



print(rounds)   
print(score)    #tabulation of score of each user
print(age)  #ages of all users that have played
print(Age)  #list of age group
print(ageScore) #[age group, list of score]
print(ageAv)    #[age group, average score]
print(roundScore)   #score for a specific round
print(x_axis) #age group  
print(y_axis) #average score of that age group
plt.scatter(x_axis, y_axis) 
    

#round_new = []
#score_new = []
#for j in range(len(rounds)):
#    for k in range(len(rounds[j])):
#        if rounds[j][k] != 'Round':
#            round_new.append(rounds[j][k])
#        if score[j][k] != 'score':
#            score_new.append(score[j][k])
#print(age)
#print(score_new)
#print(round_new)