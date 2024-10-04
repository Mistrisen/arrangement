import pandas
from datetime import datetime
import datetime as dt
import csv

today = (dt.datetime.today()).date()

if (datetime.now()).day == 1:
    f = open('workload.csv','r+', newline = '')
    workload = list(csv.reader(f))
    w = csv.writer(f)
    for i in workload:
        i[1] = '0'
    f.seek(0,0)
    w.writerows(workload)
    f.close()

def timetable():
    if today.weekday() == 0:
        teachers_timetable = pandas.read_csv("./timetable/mon.csv")
    elif today.weekday() == 1:
        teachers_timetable = pandas.read_csv("./timetable/tue.csv")
    elif today.weekday() == 2:
        teachers_timetable = pandas.read_csv("./timetable/wed.csv")
    elif today.weekday() == 3:
        teachers_timetable = pandas.read_csv("./timetable/fri.csv") #Thursday timetable not available
    elif today.weekday() == 4:
        teachers_timetable = pandas.read_csv("./timetable/fri.csv")
    elif today.weekday() == 5:
        teachers_timetable = pandas.read_csv("./timetable/sat.csv")
    elif today.weekday() == 6:
        teachers_timetable = "Timetable not available for Sunday."

    return teachers_timetable

def select(teachers_available):
    hours = []
    f = open('workload.csv','r+', newline = '')
    workload = list(csv.reader(f))

    for i in teachers_available:
        for j in workload:
            if j[0] == i:
                hours.append(j[1])
            else:
                continue
    
    sub = teachers_available[hours.index(min(hours))]
    w = csv.writer(f)
    for i in workload:
        if i[0] == sub:
            i[1] = int(i[1]) + 1
    
    f.seek(0,0)
    w.writerows(workload)
    f.close()
    return sub

def individual_timetable(absent_teachers):
    individual_teachers_timetable = []
    indttvar = timetable().values.tolist()

    for i in absent_teachers:
        for j in range(0,len(indttvar)):
            if indttvar[j][0] == i:
                individual_teachers_timetable.append(indttvar[j])
            else:
                continue
    return individual_teachers_timetable

def check(abs):
    listt = []
    f = open('workload.csv','r+', newline = '')
    workload = list(csv.reader(f))
    for i in workload:
        listt.append(i[0])
    f.close()
    if all(i in listt for i in abs):
        return True
    else:
        return False

def generate(absent_teachers):
    arrangement = individual_timetable(absent_teachers)

    for spec_teacher_abs in arrangement:
        periods_required = []
        teachers_available = []

        for j in range(1,9):
            if (spec_teacher_abs[j] != '-') and (j not in periods_required):
                periods_required.append(j)
            else:
                continue

        for j in periods_required:
            for row in timetable().itertuples(): 
                if (row[j+1] == '-') and (row.Teachers not in absent_teachers):
                    teachers_available.append(row.Teachers)
                else:
                    continue
            
            if len(teachers_available) != 0:
                arrangement[arrangement.index(spec_teacher_abs)][periods_required[periods_required.index(j)]] = str(arrangement[arrangement.index(spec_teacher_abs)][periods_required[periods_required.index(j)]]) + ' - ' + str(select(teachers_available))
            else:
                arrangement[arrangement.index(spec_teacher_abs)][periods_required[periods_required.index(j)]] = str(arrangement[arrangement.index(spec_teacher_abs)][periods_required[periods_required.index(j)]]) + ' - ' + 'PT/Yoga'

    return pandas.DataFrame(arrangement)

while True:

    func = input("Enter the command associated with the function you would like to perform. \n")
    
    if func == 'help':
        print('''
    The following are the list of functions:

    timetable - prints today's timetable
    teachers - prints the names of the teachers and the respective abbreviation used for them
    generate - given the abbreviations of teachers absent on a day, generates an arrangement
    exit - closes the program
        ''')

    elif func == 'exit':
        exit()
    
    elif func == 'timetable':
        print(timetable())

    elif func == 'teachers':
        print(" S NIRMALA - SN \n G SUGANTHI - GS \n D SREELATHA - DS \n JAL SMITH - JS \n G RAVI - GR \n AJITHA - AJ \n PGT CHEM - PGTC \n PGT BIO - PGTB \n SHIPRA DIXIT - SD \n CHANDA - CH \n R K SHUKL - RKS \n BENITA PON - BP \n T KALYANI - TK \n SHIVANI VERMA - SV \n ALKA - AL \n VIJAY KUMAR - VK \n SUNITA - SUN \n TGT SKT - TGTS \n POONAM RANI - PR \n HARSHIL - HAR \n THARANI - THA \n ANJALI YADAV - AY \n UMMED SINGH - US \n NATHURAM SAINI - NS \n NITHESH KUMARI - NK \n MARIA JOY - MJ \n KOMAL - KOM \n PET (COACH) - PET \n P JEGANNATH - PJ \n NISHA - NIS \n RUCHI - RUC \n RAJESH - RAJ \n COMPUTER - COMP \n GERMAN/TAMIL - G/T \n ")

    elif func == 'generate':
        while True:
            abs = (input("Enter the abbreviations of the teachers absent, separated with commas. ")).split(',')
            
            if check(abs) == True:
                tts = generate(abs)
                print(tts)
                while True:
                    prompt = input("Would you like to save this arrangement to the folder? (Y/N)\n")
                    if prompt == 'Y':
                        tts.to_excel(str(today) +".xlsx",)
                        break
                    elif prompt == 'N':
                        break
                    else:
                        print("Please enter only Y or N.")
                break
            else:
                print("Teachers could not be found.")
                
    else:
        print("Enter a valid function. Input 'help' for a list of the possible functions.")