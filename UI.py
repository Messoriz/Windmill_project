"""tkinter er den package vi bruger til vores GUI(grafical User Interface/Grafisk brugerflade)"""
import tkinter as tk
from tkinter import ttk

"""pandas er et datastruktur library som vi bruger til at holde manipulere vores data. """
import pandas as pd
from pandastable import Table

"""numpy er hvad pandas er bygget på, og har nogle bedre metoder som vi gør brug af """
import numpy as np

"""Data er vores egen package med nogle klasser vi bruger til at styre vores data"""
import Data

"""path bruges til at tjekke filen vi skriver til eksistere"""
from os import path

"""Standard størrelser vi bruger til vores forskellige widgets"""
LARGE_FONT = ("Verdana", 18)
buttonWidth = "30"

"""Popup vindue som bliver brugt til at give en tilpasset besked til brugeren"""


def popupmsg(msg):
    popup = tk.Tk()
    popup.resizable(False, False)
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=LARGE_FONT)
    label.pack(side="top", pady=10)
    b1 = ttk.Button(popup, text="Okay", command=lambda: popup.destroy())
    b1.pack(pady=8, padx=8)
    popup.iconbitmap('wind-turbine.ico')
    popup.mainloop()


"""Opretter en ny vindmølle ved hjælp af klasserne fra Data filen"""


def create_windmill(loc):
    data = Data.Database()
    newWM = Data.Windmill(loc)
    data.addnewData("Windmill", newWM.getDF())
    popupmsg(newWM.newWindmillMadeMessage())


"""Dette en funktion med et popup vindue hvor brugeren giver den nødvendige information,
    til at oprette en ny vindmølle"""


def setupWindmill_Popup():
    popup = tk.Tk()
    popup.resizable(False, False)
    popup.wm_title("Setup new windmill")
    popup.geometry("720x420")
    popup.tk_setPalette(background='#85C1E9')
    label = tk.Label(popup, text="Use the dropdown menu to pick the location\n of the new windmill", font=LARGE_FONT,
                     bg='#85C1E9')
    label.pack(side="top", pady=20)

    label2 = tk.Label(popup, text="Location: ", bg='#85C1E9')
    label2.pack(pady=5, padx=5)
    combobox1 = ttk.Combobox(popup, values=["Anholt", "Avedøre", "Horns Rev 1", "Horns Rev 2", "Nysted"])
    combobox1.pack(pady=5, padx=5)
    combobox1.current(0)

    b1 = ttk.Button(popup, text="Okay", command=lambda: create_windmill(combobox1.get()))
    b1.pack(pady=5, padx=5)
    b2 = ttk.Button(popup, text="Cancel", command=lambda: popup.destroy())
    b2.pack(pady=5, padx=5)

    popup.iconbitmap('wind-turbine.ico')
    popup.mainloop()


"""Denne funktion tager et page-klasse som argument samt en string variable der peger på et csv. fil,
    Med denne information får brugeren den fremvist den nyeste version af den ønskede dataframe"""


def updateList(page, csv):
    try:
        page.table = pt = Table(page.sheetframe, dataframe=pd.read_csv(csv))
        pt.show()
    except:
        popupmsg("Something went wrong")


"""Dette er klassen der nedarver fra interface vinduet og agere som en navigation klassen, 
    da den har en instanse af alle page klasserne i en dictionary variable, 
    og en metode som der gør det muligt at kalde den valgte page op til det øverste lag af hovedvinduet """


class SITEApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        self.iconbitmap("wind-turbine.ico")
        self.wm_title("Group 8 SITE Solution")
        self.geometry("1280x720")

        container = tk.Frame(self)
        container.tk_setPalette(background='#85C1E9')
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, AdminPage, TechnicianPage, WindmillPage, EmployeePage,
                  WorkPage, SetupEmployeePage, SetupWorkPage, TechWorkPage, WindmillHistoryPage):
            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    """Dette er navigation metoden som bliver kaldt, når der en ny side skal bringes frem, den tager navnet på page 
    klassen som argument """

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


"""Dette er startsiden for programmet, den indenholder et login barriere som man skal igennem for at komme videre"""


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.label1 = tk.Label(self, text="Welcome to SITE-Solution 2.0"
                                          "\nA softwareprogram by group 8", font=LARGE_FONT, bg='#85C1E9')
        self.label1.pack(pady=10, padx=10)
        self.label2 = tk.Label(self, text="Please enter details below to login", font=LARGE_FONT, bg='#85C1E9')
        self.label2.pack(pady=30, padx=10)

        self.username_verify = tk.StringVar()
        self.password_verify = tk.StringVar()

        self.label3 = tk.Label(self, text="Username:", bg='#85C1E9')
        self.label3.pack()
        self.username_login_entry = ttk.Entry(self, textvariable=self.username_verify)
        self.username_login_entry.pack()

        self.label4 = tk.Label(self, text="Password:", bg='#85C1E9')
        self.label4.pack()
        self.password_login_entry = ttk.Entry(self, textvariable=self.password_verify, show="*")
        self.password_login_entry.pack()

        self.button1 = tk.Button(self, text="Login", default="active", bd=5, bg="green", width="10",
                                 command=lambda: self.login_verify())
        self.button1.pack(pady=10)

        self.button2 = tk.Button(self, text="Quit", bd=5, bg="red",
                                 command=quit)
        self.button2.pack()

    """Denne metode tager det indtastet argument i username-entry og password-entry, 
        når brugeren trykker på login knappen. Først leder den efter username i employee.csv, 
        og dernæst kontrolere den at det username og password passer sammen"""

    def login_verify(self):
        username1 = self.username_verify.get().lower()
        password1 = self.password_verify.get().lower()
        self.username_login_entry.delete(0, tk.END)
        self.password_login_entry.delete(0, tk.END)

        if path.exists(Data.employeesCSV):
            df = pd.DataFrame(pd.read_csv(Data.employeesCSV))
            usernames = df["username"].values.tolist()
            if username1 in usernames:
                info = df.loc[df["username"] == username1]
                if password1 == str(info["password"].values[0]):
                    self.login_succes(info["role"].values[0])
                else:
                    popupmsg("Password does not match the username!\n\tClick ok and try again")
            else:
                popupmsg("Username not found!\nClick ok and try again")

    """Denne metode bliver kun kørt hvis det lykkes at komme igennem login, og tager brugerens role som argument,
        for derved at navigere hen til den pågældende rolle menu"""

    def login_succes(self, role):
        if role == 'admin':
            self.controller.show_frame(AdminPage)
        elif role == 'technician':
            self.controller.show_frame(TechnicianPage)

    """Dette er admin menuside klassen hvor administratoren har mange valgmuligheder som angivet på knapperne"""


class AdminPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.label1 = tk.Label(self, text="Admin Menu", font=LARGE_FONT)
        self.label1.pack(pady=20, padx=10)

        self.button1 = ttk.Button(self, text="Windmill Overview", width=buttonWidth,
                                  command=lambda: controller.show_frame(WindmillPage))
        self.button1.pack(pady=5, padx=5)

        self.button2 = ttk.Button(self, text="Setup a new Windmill", width=buttonWidth,
                                  command=lambda: setupWindmill_Popup())
        self.button2.pack(pady=5, padx=5)

        self.button3 = ttk.Button(self, text="Work Overview", width=buttonWidth,
                                  command=lambda: controller.show_frame(WorkPage))
        self.button3.pack(pady=5, padx=5)

        self.button4 = ttk.Button(self, text="Setup a new work/repair case", width=buttonWidth,
                                  command=lambda: controller.show_frame(SetupWorkPage))
        self.button4.pack(pady=5, padx=5)

        self.button5 = ttk.Button(self, text="Employee Overview", width=buttonWidth,
                                  command=lambda: controller.show_frame(EmployeePage))
        self.button5.pack(pady=5, padx=5)

        self.button6 = ttk.Button(self, text="Setup a new employee", width=buttonWidth,
                                  command=lambda: controller.show_frame(SetupEmployeePage))
        self.button6.pack(pady=5, padx=5)

        self.button7 = ttk.Button(self, text="Windmill repair history", width=buttonWidth,
                                  command=lambda: controller.show_frame(WindmillHistoryPage))
        self.button7.pack(pady=5, padx=5)

        self.button8 = ttk.Button(self, text="Log out", width=buttonWidth,
                                  command=lambda: controller.show_frame(StartPage))
        self.button8.pack(pady=5, padx=5)


"""Dette tilsvarende teknikerens menu side klassse hvor han kan vælge at få fremvist arbejdsopgaver"""


class TechnicianPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.label1 = tk.Label(self, text="Technician Menu", font=LARGE_FONT)
        self.label1.pack(pady=20, padx=10)

        self.button1 = ttk.Button(self, text="See Work", width=buttonWidth,
                                  command=lambda: controller.show_frame(TechWorkPage))
        self.button1.pack(pady=5, padx=5)

        self.button2 = ttk.Button(self, text="Log out", width=buttonWidth,
                                  command=lambda: controller.show_frame(StartPage))
        self.button2.pack(pady=5, padx=5)


"""Dette er vindmølle oversigt side klasse, hvor det muligt at lave ændringer på vindmøller og oprette nye, 
    det er også her vi gør brug af pandastable til at fremvise dataframe over vindmøllerne"""


class WindmillPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.label1 = tk.Label(self, text="Windmill Overview", font=LARGE_FONT, bg='#85C1E9')
        self.label1.pack(pady=20, padx=10)

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(padx=20, pady=20)

        self.button1 = ttk.Button(self.button_frame
                                  , text="Setup a new Windmill", width=buttonWidth,
                                  command=lambda: setupWindmill_Popup())
        self.button1.pack(pady=5, padx=5)

        self.button2 = ttk.Button(self.button_frame, text="Save changes made", width=buttonWidth,
                                  command=lambda: self.saveChanges())
        self.button2.pack(pady=5, padx=5)

        self.button3 = ttk.Button(self.button_frame, text="Update list", width=buttonWidth,
                                  command=lambda: updateList(self, Data.windmillCSV))
        self.button3.pack(pady=5, padx=5)

        self.button4 = ttk.Button(self.button_frame, text="Back to menu", width=buttonWidth,
                                  command=lambda: controller.show_frame(AdminPage))
        self.button4.pack(pady=5, padx=5)

        self.sheetframe = tk.Frame(self)
        self.sheetframe.pack(ipadx=60, ipady=20)
        self.df = pd.read_csv(Data.windmillCSV)
        self.table = pt = Table(self.sheetframe, dataframe=self.df)
        pt.show()

    """Denne metode gør det muligt at gemme de ændringer der lavet manuelt på pandastable af brugeren"""

    def saveChanges(self):
        self.table.model.df.to_csv(Data.windmillCSV, index=False)


"""Dette er 'Work case' oversigt side klassen, denne side bliver kun vist for admin, 
    da det her er muligt at lave manuelt ændringer, udover dette kan admin også vælge at sætte arbejde 
    som fuldført her og andre ting"""


class WorkPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.label1 = tk.Label(self, text="Work Overview", font=LARGE_FONT, bg='#85C1E9')
        self.label1.pack(pady=10, padx=10)

        self.topbuttonframe = tk.Frame(self)
        self.topbuttonframe.pack(pady=15)

        self.button1 = ttk.Button(self.topbuttonframe, text="Update list", width=buttonWidth,
                                  command=lambda: [updateList(self, Data.workCSV), self.updateDropdown()])
        self.button1.pack(pady=5, padx=5)

        self.button2 = ttk.Button(self.topbuttonframe, text="Save changes made", width=buttonWidth,
                                  command=lambda: self.saveChanges())
        self.button2.pack(pady=5, padx=5)

        self.button3 = ttk.Button(self.topbuttonframe, text="Back to Menu", width=buttonWidth,
                                  command=lambda: self.lower())
        self.button3.pack(pady=5, padx=5)
        self.sheetframe = tk.Frame(self)
        self.sheetframe.pack(side="left", fill="both", expand=True)
        self.df = pd.read_csv(Data.workCSV)
        self.dfr = ""
        self.table = pt = Table(self.sheetframe, dataframe=self.df,
                                showstatusbar=True)
        pt.show()

        self.lowerOptionsFrame = tk.Frame(self)
        self.lowerOptionsFrame.pack(side="left", fill="both", expand=True)

        self.label2 = tk.Label(self.lowerOptionsFrame, text="Choose employee ID from dropdown then click 'Sort ID'",
                               bg='#85C1E9')
        self.label2.pack(pady=10, padx=10)

        self.employeeID = list(set(self.df["employee-id"].tolist()))
        self.dropdown = ttk.Combobox(self.lowerOptionsFrame, values=self.employeeID,
                                     postcommand=lambda: self.dropdown.config(values=self.employeeID))
        self.dropdown.pack(pady=10)
        self.dropdown.current(0)

        self.button4 = ttk.Button(self.lowerOptionsFrame, text="Sort by ID", width=buttonWidth,
                                  command=lambda: self.sortList(self.dropdown.get()))
        self.button4.pack(pady=5, padx=5)

        self.label3 = tk.Label(self.lowerOptionsFrame, text="Click case and then click work completed", bg='#85C1E9')
        self.label3.pack(pady=10, padx=10)

        self.button5 = ttk.Button(self.lowerOptionsFrame, text="Work Completed", width=buttonWidth,
                                  command=lambda: self.workCompleted())
        self.button5.pack(pady=5, padx=5)

    """Denne metode opdatere dropdown menuen hver gang den bliver trykke på, 
        så brugeren altid kan sortere efter den nye data"""

    def updateDropdown(self):
        self.df = pd.read_csv(Data.workCSV)
        self.employeeID = list(set(self.df["employee-id"].tolist()))

    """Denne metode opdatere alt den data som skal lave om efter en work case er fuldført"""

    def workCompleted(self):

        try:
            """Fanger brugerens valg, og gemmer variablerne"""
            workCID = self.table.getSelectedRows().values[0].tolist()[0]
            workCwmID = self.table.getSelectedRows().values[0].tolist()[1]
            workCeID = self.table.getSelectedRows().values[0].tolist()[2]

            """Gemmer brugerens valgte dataframe/workcase, og dropper kolonner 'id' og 'status'"""
            workCdf = self.table.getSelectedRows()
            workCdf = workCdf.drop(labels=["id", "status"], axis=1)
            workCdf = workCdf.values.tolist()[0]

            """Flytter det fuldførte arbejde til windmill-history.csv"""

            newWH = Data.WindmillHistory(workCdf[0], workCdf[1], workCdf[2])
            data = Data.Database()
            data.addnewData("Windmill-history", newWH.getDF())

            """Opdatere vindmøllens status i windmill.csv, da den nu er virker"""

            wmlist = pd.read_csv(Data.windmillCSV)
            pointer = np.where(wmlist["id"] == workCwmID)[0][0]
            wmlist.at[pointer, "status"] = "working"
            wmlist.to_csv(Data.windmillCSV, index=False)

            """Medarbejder har klaret en workcase og får derfor reduceret sit cases antal med 1"""

            wmlist = pd.read_csv(Data.employeesCSV)
            pointer = np.where(wmlist["id"] == workCeID)[0][0]
            wmlist.at[pointer, "cases"] -= 1
            wmlist.to_csv(Data.employeesCSV, index=False)

            """Til sidst fjerner den workcase'en fra work.csv, da den nu virker igen"""

            wlist = pd.read_csv(Data.workCSV)
            pointer = np.where(wlist["id"] == workCID)[0][0]
            wlist = wlist.drop(labels=pointer, axis=0)
            wlist.to_csv(Data.workCSV, index=False)

            """Opdater den viste liste nu uden den fuldførte opgave, samt opdatere dropdownmenuen"""
            updateList(self, Data.workCSV)
            self.updateDropdown()
            self.dropdown.config(values=self.employeeID)
            popupmsg(f"work case with the ID:{workCID} has been remove")

        except:
            popupmsg("Something went wrong")

    """Denne metode gør det muligt at gemme de ændringer der lavet manuelt på pandastable af brugeren"""

    def saveChanges(self):
        self.table.model.df.to_csv(Data.workCSV, index=False)

    """Når denne metode bliver kaldt, bliver en ny side vist med den valgte sortering"""

    def sortList(self, id):
        try:
            self.table.destroy()
            self.df = pd.read_csv(Data.workCSV)
            self.dfr = self.df.loc[self.df["employee-id"] == int(id)]
            self.table = pt = Table(self.sheetframe, dataframe=self.dfr,
                                    showstatusbar=True)
            pt.show()
        except:
            updateList(self, Data.workCSV)
            popupmsg("Wrong input try again!")


"""Dette er klassen med oversigten over employees igen her er muligt for administratoren at have et overblik,
    samt lave de ædringer som der ønskes"""


class EmployeePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.label1 = tk.Label(self, text="Employee Overview", font=LARGE_FONT, bg='#85C1E9')
        self.label1.pack(pady=20, padx=10)

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(padx=20, pady=10)

        self.button1 = ttk.Button(self.button_frame, text="Update list", width=buttonWidth,
                                  command=lambda: updateList(self, Data.employeesCSV))
        self.button1.pack(pady=5, padx=5)

        self.button2 = ttk.Button(self.button_frame, text="Setup a new employee", width=buttonWidth,
                                  command=lambda: controller.show_frame(SetupEmployeePage))
        self.button2.pack(pady=5, padx=5)

        self.button3 = ttk.Button(self.button_frame, text="Save changes made", width=buttonWidth,
                                  command=lambda: self.saveChanges())
        self.button3.pack(pady=5, padx=5)

        self.button4 = ttk.Button(self.button_frame, text="Back to menu", width=buttonWidth,
                                  command=lambda: self.lower())
        self.button4.pack(pady=5, padx=5)

        self.sheetframe = tk.Frame(self)
        self.sheetframe.pack(ipadx=60, ipady=20)

        self.table = pt = Table(self.sheetframe, dataframe=pd.read_csv(Data.employeesCSV))
        pt.show()

    """Denne metode gør det muligt at gemme de ændringer der lavet manuelt på pandastable af brugeren"""

    def saveChanges(self):
        self.table.model.df.to_csv(Data.employeesCSV, index=False)


"""Dette er klassen hvor administratoren har mulighed for at oprette en ny employee til databasen"""


class SetupEmployeePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.label1 = tk.Label(self, text="Setup new employee", font=LARGE_FONT, bg='#85C1E9')
        self.label1.pack(pady=20, padx=10)

        self.label2 = tk.Label(self, text="Please enter details below to setup new employee", font=LARGE_FONT,
                               bg='#85C1E9')
        self.label2.pack(pady=20, padx=10)

        self.label3 = tk.Label(self, text="Role: ", bg='#85C1E9')
        self.label3.pack()
        self.combobox = ttk.Combobox(self, values=["technician", "admin"])
        self.combobox.pack()
        self.combobox.current(0)

        self.name = tk.StringVar()
        self.label4 = tk.Label(self, text="Name: ", bg='#85C1E9')
        self.label4.pack()
        self.entryName = ttk.Entry(self, textvariable=self.name)
        self.entryName.pack()

        self.button1 = ttk.Button(self, text="Okay", width=buttonWidth,
                                  command=lambda: self.create_employee(self.combobox.get()))
        self.button1.pack(pady=5, padx=5)
        self.button2 = ttk.Button(self, text="Cancel", width=buttonWidth, command=lambda: self.lower())
        self.button2.pack(pady=5, padx=5)

    """Denne metode opretter en ny employee når den bliver kaldt med argumentet role og entry name, 
        og hvis det lykkes vil en popup kommer frem med en besked om det"""

    def create_employee(self, role):
        try:
            data = Data.Database()
            newE = Data.Employee(role, self.name.get())
            self.entryName.delete(0, tk.END)
            data.addnewData("Employee", newE.getDF())
            popupmsg(newE.newEmployeeMadeMessage())
        except:
            popupmsg("Missing input!\nPlease enter first and last name please!")


"""Dette er klassen hvor det muligt for administatoren at oprette en ny workcase, 
dette ske ved først at klikke på den vindmølle der skal repareres, 
og dernæst vælge den employee som skal have opgaven"""


class SetupWorkPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.label1 = tk.Label(self, text="Setup a new work case", font=LARGE_FONT, bg='#85C1E9')
        self.label1.pack(pady=20, padx=10)

        self.button1 = ttk.Button(self, text="Update list", width=buttonWidth,
                                  command=lambda: self.updateLists())
        self.button1.pack(pady=5, padx=5)

        self.label2 = tk.Label(self,
                               text="First click on the windmill\nThen click on the employee\nThen press submit button",
                               font=LARGE_FONT, bg='#85C1E9')
        self.label2.pack(pady=20, padx=10)

        self.button2 = ttk.Button(self, text="Submit", width=buttonWidth, command=lambda: self.create_workcase())
        self.button2.pack(pady=5, padx=5)
        self.button3 = ttk.Button(self, text="Cancel", width=buttonWidth, command=lambda: self.lower())
        self.button3.pack(pady=5, padx=5)

        self.wmSheet = tk.Frame(self)
        self.wmSheet.pack(side="left", fill="both", pady=15)
        self.wmTable = pt1 = Table(self.wmSheet, dataframe=pd.read_csv(Data.windmillCSV))
        pt1.show()

        self.empSheet = tk.Frame(self)
        self.empSheet.pack(side="left", fill="both", pady=15, expand=True)
        self.empTable = pt2 = Table(self.empSheet, dataframe=pd.read_csv(Data.employeesCSV))
        pt2.show()

    """Denne metode tager den valgte vindmølle og employee og 
        bruger deres id til at sættte sammen til en ny work case"""

    def create_workcase(self):
        try:
            wmID = self.wmTable.getSelectedRows()["id"].values[0]
            eID = self.empTable.getSelectedRows()["id"].values[0]

            """Her opdatere den status på vindmøllen inden i oversigten til at være under 'maintenance"""
            wmlist = pd.read_csv(Data.windmillCSV)
            pointer = np.where(wmlist["id"] == wmID)[0][0]
            wmlist.at[pointer, "status"] = "maintenance"
            wmlist.to_csv(Data.windmillCSV, index=False)

            """Her bliver den valgte medarbejders 'cases' forøget med 1, da han har fået en ny work case"""
            elist = pd.read_csv(Data.employeesCSV)
            pointer = np.where(elist["id"] == eID)[0][0]
            elist.at[pointer, "cases"] += 1
            elist.to_csv(Data.employeesCSV, index=False)

            """Den nye work case bliver oprettet og gemt"""
            data = Data.Database()
            newWork = Data.Work(wmID, eID)
            data.addnewData("Work", newWork.getDF())
            popupmsg(newWork.newWorkCaseMadeMessage())
        except:
            popupmsg("something went wrong, please try again!")

    """Denne metode er til at opdatere pandastable på denne side med den nyeste version"""

    def updateLists(self):
        self.wmTable = pt1 = Table(self.wmSheet, dataframe=pd.read_csv(Data.windmillCSV))
        pt1.show()
        self.empTable = pt2 = Table(self.empSheet, dataframe=pd.read_csv(Data.employeesCSV))
        pt2.show()


"""Dette er klassen som bruger med rollen tekniker, kan se oversigten over arbejdsopgaver, og angive at en work case 
    er fuldført """


class TechWorkPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.label1 = tk.Label(self, text="Work Overview", font=LARGE_FONT, bg='#85C1E9')
        self.label1.pack(pady=10, padx=10)

        self.topbuttonframe = tk.Frame(self)
        self.topbuttonframe.pack(pady=15)

        self.button1 = ttk.Button(self.topbuttonframe, text="Update list", width=buttonWidth,
                                  command=lambda: [updateList(self, Data.workCSV), self.updateDropdown()])
        self.button1.pack(pady=5, padx=5)

        self.button2 = ttk.Button(self.topbuttonframe, text="Back to Menu", width=buttonWidth,
                                  command=lambda: self.lower())
        self.button2.pack(pady=5, padx=5)

        self.sheetframe = tk.Frame(self)
        self.sheetframe.pack(side="left", fill="both", expand=True)
        self.df = pd.read_csv(Data.workCSV)
        self.dfr = ""
        self.table = pt = Table(self.sheetframe, dataframe=self.df,
                                showstatusbar=True)
        pt.show()

        self.lowerOptionsFrame = tk.Frame(self)
        self.lowerOptionsFrame.pack(side="left", fill="both", expand=True)

        self.label2 = tk.Label(self.lowerOptionsFrame, text="Sort by choosing employee ID from drop down menu",
                               bg='#85C1E9')
        self.label2.pack(pady=10, padx=10)

        self.employeeID = list(set(self.df["employee-id"].tolist()))
        self.dropdown = ttk.Combobox(self.lowerOptionsFrame, values=self.employeeID,
                                     postcommand=lambda: self.dropdown.config(values=self.employeeID))
        self.dropdown.pack(pady=10)
        self.dropdown.current(0)

        self.button3 = ttk.Button(self.lowerOptionsFrame, text="Sort by ID", width=buttonWidth,
                                  command=lambda: self.sortList(self.dropdown.get()))
        self.button3.pack(pady=5, padx=5)

        self.label3 = tk.Label(self.lowerOptionsFrame, text="Click case and then click work completed", bg='#85C1E9')
        self.label3.pack(pady=10, padx=10)

        self.button4 = ttk.Button(self.lowerOptionsFrame, text="Work Completed", width=buttonWidth,
                                  command=lambda: self.workCompleted())
        self.button4.pack(pady=5, padx=5)

    """Denne metode opdatere dropdown menuen hver gang den bliver trykke på,
     så brugeren altid kan sortere efter den nye data"""

    def updateDropdown(self):
        self.df = pd.read_csv(Data.workCSV)
        self.employeeID = list(set(self.df["employee-id"].tolist()))

    """Denne metode opdatere alt den data som skal lave om efter en work case er fuldført"""

    def workCompleted(self):
        try:
            """Fanger brugerens valg, og gemmer variablerne"""
            workCID = self.table.getSelectedRows().values[0].tolist()[0]
            workCwmID = self.table.getSelectedRows().values[0].tolist()[1]
            workCeID = self.table.getSelectedRows().values[0].tolist()[2]

            """Gemmer brugerens valgte dataframe/workcase, og dropper kolonner 'id' og 'status'"""
            workCdf = self.table.getSelectedRows()
            workCdf = workCdf.drop(labels=["id", "status"], axis=1)
            workCdf = workCdf.values.tolist()[0]

            """Flytter det fuldførte arbejde til windmill-history.csv"""
            newWH = Data.WindmillHistory(workCdf[0], workCdf[1], workCdf[2])
            data = Data.Database()
            data.addnewData("Windmill-history", newWH.getDF())

            """Opdatere vindmøllens status i windmill.csv, da den nu er virker"""
            wmlist = pd.read_csv(Data.windmillCSV)
            pointer = np.where(wmlist["id"] == workCwmID)[0][0]
            wmlist.at[pointer, "status"] = "working"
            wmlist.to_csv(Data.windmillCSV, index=False)

            """Medarbejder har klaret en workcase og får derfor reduceret sit cases antal med 1"""
            wmlist = pd.read_csv(Data.employeesCSV)
            pointer = np.where(wmlist["id"] == workCeID)[0][0]
            wmlist.at[pointer, "cases"] -= 1
            wmlist.to_csv(Data.employeesCSV, index=False)

            """Til sidst fjerner den workcase'en fra work.csv, da den nu virker igen"""
            wlist = pd.read_csv(Data.workCSV)
            pointer = np.where(wlist["id"] == workCID)[0][0]
            wlist = wlist.drop(labels=pointer, axis=0)
            wlist.to_csv(Data.workCSV, index=False)

            """Opdater den viste liste nu uden den fuldførte opgave, samt opdatere dropdownmenuen"""
            self.updateDropdown()
            self.dropdown.config(values=self.employeeID)
            updateList(self, Data.workCSV)
            popupmsg(f"Work case with the ID:{workCID} has successfully been remove")

        except:
            popupmsg("Something went wrong")

    """Når denne metode bliver kaldt, bliver en ny side vist med den valgte sortering"""

    def sortList(self, id):
        try:
            self.table.destroy()
            self.df = pd.read_csv(Data.workCSV)
            self.dfr = self.df.loc[self.df["employee-id"] == int(id)]
            self.table = pt = Table(self.sheetframe, dataframe=self.dfr,
                                    showstatusbar=True)
            pt.show()
        except:
            updateList(self, Data.workCSV)
            popupmsg("Wrong input try again!")

"""Dette er klassen hvor det er muligt for bruger med rollen admin, 
    at kunne se historikken over tidligere reparationer, med dato for fuldførelse samt skadesanmeldelse, 
    og hvilken medarbejder der har udført reparationen, alt dette kan bruges senere hen til større analyser"""

class WindmillHistoryPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.label1 = tk.Label(self, text="Windmill repair history Overview", font=LARGE_FONT, bg='#85C1E9')
        self.label1.pack(pady=10, padx=10)

        self.topbuttonframe = tk.Frame(self)
        self.topbuttonframe.pack(pady=15)

        self.button1 = ttk.Button(self.topbuttonframe, text="Update list", width=buttonWidth,
                                  command=lambda: [updateList(self, Data.windmill_historyCSV), self.updateDropdown()])
        self.button1.pack(pady=5, padx=5)

        self.button2 = ttk.Button(self.topbuttonframe, text="Save changes made", width=buttonWidth,
                                  command=lambda: self.saveChanges())
        self.button2.pack(pady=5, padx=5)

        self.button3 = ttk.Button(self.topbuttonframe, text="Back to Menu", width=buttonWidth,
                                  command=lambda: self.lower())
        self.button3.pack(pady=5, padx=5)

        self.sheetframe = tk.Frame(self)
        self.sheetframe.pack(side="left", fill="both", expand=True)
        self.df = pd.read_csv(Data.windmill_historyCSV)
        self.dfr = ""
        self.table = pt = Table(self.sheetframe, dataframe=self.df,
                                showstatusbar=True)
        pt.show()

        self.lowerOptionsFrame = tk.Frame(self)
        self.lowerOptionsFrame.pack(side="left", fill="both", expand=True)

        self.label2 = tk.Label(self.lowerOptionsFrame, text="Choose windmill ID from dropdown then click 'Sort ID'",
                               bg='#85C1E9')
        self.label2.pack(pady=10, padx=10)

        self.wmID = list(set(self.df["windmill-id"].tolist()))
        self.dropdown = ttk.Combobox(self.lowerOptionsFrame, values=self.wmID,
                                     postcommand=lambda: self.dropdown.config(values=self.wmID))
        self.dropdown.pack(pady=10)
        self.dropdown.current(0)

        self.button4 = ttk.Button(self.lowerOptionsFrame, text="Sort ID", width=buttonWidth,
                                  command=lambda: self.sortList(self.dropdown.get()))
        self.button4.pack(pady=5, padx=5)

    """Denne metode opdatere dropdown menuen hver gang den bliver trykke på, 
    så brugeren altid kan sortere efter den nye data"""

    def updateDropdown(self):
        self.df = pd.read_csv(Data.windmill_historyCSV)
        self.wmID = list(set(self.df["windmill-id"].tolist()))

    """Denne metode gør det muligt at gemme de ændringer der lavet manuelt på pandastable af brugeren"""

    def saveChanges(self):
        self.table.model.df.to_csv(Data.windmill_historyCSV, index=False)

    """Når denne metode bliver kaldt, bliver en ny side vist med den valgte sortering"""

    def sortList(self, id):
        try:
            self.table.destroy()
            self.df = pd.read_csv(Data.windmill_historyCSV)
            self.dfr = self.df.loc[self.df["windmill-id"] == int(id)]
            self.table = pt = Table(self.sheetframe, dataframe=self.dfr,
                                    showstatusbar=True)
            pt.show()
        except:
            updateList(self, Data.windmill_historyCSV)
            popupmsg("Wrong input try again!")
