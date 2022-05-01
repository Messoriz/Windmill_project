"""random modulet bruges til at skabe et tilfældigt password til de nye oprettet bruger"""
import random

"""string modulet gøres brug af i vores randomNumGenerator funktion"""
import string

"""pandas er et datastruktur library som programmet bruger til at holde manipulere vores data. """
import pandas as pd

"""datetime er det module programmet bruger til at få dags dato for fuldført arbejde"""
from datetime import date

"""string variablerne for de csv filer programmet bruger """
windmillCSV = "windmills.csv"
employeesCSV = "employees.csv"
workCSV = "work.csv"
windmill_historyCSV = "windmill-history.csv"

"""Denne funktionen skaber et tilfældigt tal string i længden som bliver givet som argument """


def randomNumGenerator(size):
    temp = random.sample(string.digits, size)
    password = ''.join(temp)
    return password


"""Denne klasse bliver primært brugt til at tilføje ny data til programmets csv filer"""


class Database:
    def __init__(self):
        self.windmills = pd.DataFrame(pd.read_csv(windmillCSV))
        self.employees = pd.DataFrame(pd.read_csv(employeesCSV))
        self.work = pd.DataFrame(pd.read_csv(workCSV))
        self.windmillHistory = pd.DataFrame(pd.read_csv(windmill_historyCSV))

    """Dette er metode der sammensætter den nyoprettet data med den gamle, og opdatere csv filerne"""

    def addnewData(self, type, object):
        try:
            if type == "Windmill":
                oldList = self.windmills
                newList = pd.concat([oldList, object])
                newList.to_csv(windmillCSV, index=False)
                self.windmills = pd.DataFrame(pd.read_csv(windmillCSV))
            elif type == "Work":
                oldList = self.work
                newList = pd.concat([oldList, object])
                newList.to_csv(workCSV, index=False)
                self.work = pd.DataFrame(pd.read_csv(workCSV))
            elif type == "Windmill-history":
                oldList = self.windmillHistory
                newList = pd.concat([oldList, object])
                newList.to_csv(windmill_historyCSV, index=False)
                self.windmillHistory = pd.DataFrame(pd.read_csv(windmill_historyCSV))
            elif type == "Employee":
                oldList = self.employees
                if object.name.values[0] not in oldList.name.values:
                    newList = pd.concat([oldList, object])
                    newList.to_csv(employeesCSV, index=False)
                    self.employees = pd.DataFrame(pd.read_csv(employeesCSV))
                else:
                    print("Already exist in the database")
            else:
                print("Wrong input")
        except:
            print("Something went wrong!")


"""Dette er vindmølle klassen som bliver brugt til at skabe nye vindmøller objekter"""


class Windmill(Database):
    def __init__(self, location):
        Database.__init__(self)
        self.id = max(self.windmills["id"].tolist()) + 1
        self.location = location
        self.status = "working"

    """En prædefineret besked der bliver sendt som en popup besked hvis det lykkes at oprette objektet"""

    def newWindmillMadeMessage(self):
        msg = f"A new windmill has successfully been created with this info:" \
              f"\n\nID:{self.id}" \
              f"\nLocation:{self.location}" \
              f"\nStatus:{self.status}"
        return msg

    """Laver objektet om til en dataframe som kan sammensættes med den gamle liste"""

    def getDF(self):
        info = pd.DataFrame({"id": [self.id], 'location': [self.location], "status": [self.status]})
        return info


"""Dette er WindmillHistory klassen som bliver brugt til at skabe nye fuldført arbejdsopgave objekter"""


class WindmillHistory(Database):
    def __init__(self, wmid, eid, damage):
        Database.__init__(self)
        today = date.today()
        self.date = today.strftime("%d/%m/%Y")
        self.windmillId = wmid
        self.employeeId = eid
        self.damage = damage

    """Laver objektet om til en dataframe som kan sammensættes med den gamle liste"""

    def getDF(self):
        info = pd.DataFrame({"date": [self.date], 'windmill-id': [self.windmillId],
                             "employee-id": [self.employeeId], "damage": [self.damage]})
        return info


"""Dette er Work klassen som bliver brugt til at skabe nye work case objekter"""

class Work(Database):
    def __init__(self, wmid, eid):
        Database.__init__(self)
        list_of_damage = ["motor", "wing", "power"]
        self.id = max(self.work["id"].tolist()) + 1
        self.windmillId = wmid
        self.employeeId = eid
        self.status = "maintenance"
        self.damage = random.choice(list_of_damage)

    """En prædefineret besked der bliver sendt som en popup besked hvis det lykkes at oprette objektet"""

    def newWorkCaseMadeMessage(self):
        msg = f"A new work case has successfully been created with this info:" \
              f"\n\nWindmill ID:{self.windmillId}" \
              f"\nEmployee ID:{self.employeeId}" \
              f"\nStatus:{self.status}\n" \
              f"Damage:{self.damage}"
        return msg

    """Laver objektet om til en dataframe som kan sammensættes med den gamle liste"""

    def getDF(self):
        info = pd.DataFrame({"id": [self.id], 'windmill-id': [self.windmillId], "employee-id": [self.employeeId],
                             "status": [self.status], "damage": [self.damage]})
        return info

"""Dette er Employee klassen som bliver brugt til at skabe nye employee objekter"""

class Employee(Database):
    def __init__(self, role, name):
        Database.__init__(self)
        self.id = max(self.employees["id"].tolist()) + 1
        self.role = role
        self.name = name
        self.username = (name.split()[0][0:2] + name.split()[1][0:3]).lower()
        self.password = randomNumGenerator(4)
        self.cases = 0

    """En prædefineret besked der bliver sendt som en popup besked hvis det lykkes at oprette objektet"""

    def newEmployeeMadeMessage(self):
        msg = f"A new employee has successfully been created with this info:" \
              f"\n\nID:{self.id}" \
              f"\nName:{self.name}" \
              f"\nUsername:{self.username}" \
              f"\nPassword:{self.password}"
        return msg

    """Laver objektet om til en dataframe som kan sammensættes med den gamle liste"""

    def getDF(self):
        info = pd.DataFrame(
            dict(id=[self.id], role=[self.role], name=[self.name], username=[self.username], password=[self.password],
                 cases=[self.cases]))
        return info
