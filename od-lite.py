import os
import curses
import json
import uuid


#------------------Functions----------------
def safeprint(screen, y, x, text, attr):
    try:
        screen.addstr(y, x, text, attr)
    except:
        pass

def printbottom(screen, text, attr):
    try:
        screen.move(curses.LINES - 1, 0)
        screen.clrtoeol()
        screen.addstr(curses.LINES -1, 0, text, attr)
    except:
        pass

def inputwrapper(screen):
    command = stdscr.getkey()
    if command == "KEY_MOUSE":
        printbottom(screen, str(curses.getmouse()), curses.color_pair(2))
        return 0
    if command == "KEY_RESIZE":
        curses.update_lines_cols()
        screen.clear()
        screen.refresh()
        printbottom(screen, "Terminal Size Change", curses.color_pair(2))
        return 0
    if command == "`":
        escapemenu(screen)
        return 0
    else:
        return command

def easygetstr(screen):
    output = screen.getstr().decode(encoding="utf-8")
    return output

#----------------Interface tree stuff--------
def escapemenu(screen):
    screen.clear()
    while True:
        safeprint(screen, 0, 0, "Escape Menu:", curses.color_pair(1))
        safeprint(screen, 2, 0, "(S)save Station", curses.color_pair(1))
        safeprint(screen, 3, 0, "(L)oad Station", curses.color_pair(1))
        safeprint(screen, 4, 0, "(Q)uit to previous menu", curses.color_pair(1))
        command = inputwrapper(screen)
        if command == 0:
            continue
        elif command == "q":
            screen.clear()
            return
        elif command == "s":
            stationdata = json.dumps(initialstation, sort_keys = True, indent = 4, cls=StationEncoder)
            file = open("station.json", 'w')
            file.write(stationdata)
            file.close()
        else:
            printbottom(screen, "Invalid input or not yet implemenented!", curses.color_pair(3))


def commandcenter(screen): 
    screen.clear()
    while True:
        safeprint(screen, 0, 0, "Command Center:", curses.color_pair(1))
        safeprint(screen, 1, 0, "(B)uild Queue", curses.color_pair(1))
        safeprint(screen, 2, 0, "(A)ssemble and launch", curses.color_pair(1))
        safeprint(screen, 3, 0, "(Q)uit to Main Menu", curses.color_pair(1))
        command = inputwrapper(screen)
        if command == 0:
            continue
        if command == "q":
            screen.clear()
            return
        elif command == "b":
            screen.clear()
            buildqueue(screen)
            continue
        elif command == "a":
            screen.clear()
            assembler(screen)
            continue
        else:
            printbottom(screen,"Invalid input or not yet implemenenented!", curses.color_pair(3))
def buildqueue(screen):
    screen.clear()
    while True:
        safeprint(screen, 0, 0, "Build Queue:", curses.color_pair(1))
        safeprint(screen, 1, 0, "Build (L)aunch Vehicle", curses.color_pair(1))
        safeprint(screen, 2, 0, "Build (M)odule", curses.color_pair(1))
        safeprint(screen, 3, 0, "Build (S)hip", curses.color_pair(1))
        safeprint(screen, 4, 0, "(Q)uit to previous menu", curses.color_pair(1))
        command = screen.getkey()
        if command == "q":
            screen.clear()
            return
        elif command == "m":
            safeprint(screen, curses.LINES - 1, 0, "Is this a CORE module? Y/N", curses.color_pair(1))
            command = screen.getkey()
            if command == "y":
                printbottom(screen, "Enter a NAME for this module: ", curses.color_pair(2))
                curses.echo()
                newname = easygetstr(screen)
                newmodule = Craft(newname, "Core")
                mainreadylist.list.append(newmodule)
                printbottom(screen, "Module created!", curses.color_pair(2))
                curses.noecho()
            else:
                printbottom(screen, "Enter a NAME for this module: ", curses.color_pair(2))
                curses.echo()
                newname = easygetstr(screen)
                newmodule = Module(newname, "Module")
                mainreadylist.list.append(newmodule)
                printbottom(screen, "Module created!", curses.color_pair(2))
                curses.noecho()
        elif command == "l":
            printbottom(screen, "Enter a NAME for this launch vehicle: ", curses.color_pair(2))
            curses.echo()
            newname = easygetstr(screen)
            newlv = LV(newname)
            mainlvlist.list.append(newlv)
            printbottom(screen, "Module created!", curses.color_pair(2))
            curses.noecho()
        else:
            safeprint(screen, curses.LINES - 1, 0, "Invalid input or not yet implemenenented!",
                      curses.color_pair(3))

def assembler(screen):
    while True:
        safeprint(screen, 0, 0, "Assemble and Launch:", curses.color_pair(1))
        safeprint(screen, 2, 0, "Select a craft to launch:", curses.color_pair(1))
        i = 4
        for each in mainreadylist.list:
            output = str(i - 3) + ") " + each.name
            if each.kind == "Core":
                output += " - Core Module"
            safeprint(screen, i, 0, output, curses.color_pair(1))
            i += 1
        i += 1

        safeprint(screen, i, 0, "Available launch vehicles:", curses.color_pair(1))
        i += 1
        for each in mainlvlist.list:
            output = str(i - 3) + ") " + each.name
            safeprint(screen, i, 0, output, curses.color_pair(1))
            i += 1
        i += 1
        
        command = inputwrapper(screen)
        if command == "q":
            screen.clear()
            return
        else:
            return
        
def stationview(screen):
    screen.clear()
    while True:
        safeprint(screen, 0, 0, "Station View", curses.color_pair(2))
   
        modulelist = initialstation.listModules()
        i = 2
        for each in modulelist:
            safeprint(screen, i, each.treedepth, each.name, curses.color_pair(1))
            i += 1

        command = inputwrapper(screen)
        if command == 0:
            continue
        if command == "q":
            screen.clear()
            return

def quitprompt(screen):
    printbottom(screen, "Press (Y) to confirm exit", curses.color_pair(3))
    command = screen.getkey()
    if command == "y":
        return True
    else:
        return False

#-------------Classes-------------
class SpaceCenter:
    def __init__(self, name):
        self.name = name
        self.buildqueue = []
        self.lvlist = []
        self.craftlist = []

class Station:
    def __init__(self, name):
        self.uuid = str(uuid.uuid4())
        self.name = name
        self.core = None

    def listModules(self):
        output = []
        core = self.core
        output.append(core)
        core.listChildrenRecursive(output)
        return output

class StationEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Station):
            output1 = {"Station Name" : o.name}
            output1["uuid"] = o.uuid
            output1["Core"] = o.core.uuid

            modulelist = [o.core]
            o.core.listChildrenRecursive(modulelist)
            
            output2 = []
            output3 = []
            for each in modulelist:
                moduleoutput = {"Module Name" : each.name}
                moduleoutput["Tree Depth"] = each.treedepth
                moduleoutput["uuid"] = each.uuid
                moduleoutput["Kind"] = each.kind
                moduleoutput["Ports"] = []
                for each2 in each.portlist:
                    moduleoutput["Ports"].append(each2.uuid)
                if each.parent is not None:
                    moduleoutput["Parent"] = each.parent.uuid
                else:
                    moduleoutput["Parent"] = None
                moduleoutput["Children"] = []
                for each2 in each.children:
                    moduleoutput["Children"].append(each2.uuid)
                output2.append(moduleoutput)

            for each in modulelist:
                for each2 in each.portlist:
                    portoutput = {}
                    portoutput["Port Name"] = each2.name
                    portoutput["uuid"] = each2.uuid
                    portoutput["Root"] = each2.root.uuid
                    portoutput["Side"] = each2.side
                    if each2.connection is None:
                        portoutput["Connection"] = "None"
                    else:
                        portoutput["Connection"] = each2.connection.uuid
   
                    output3.append(portoutput)

            return (output1, output2, output3)
        else:
            return super().default(o)

def decodestation(json, craftlist):
    station = Station(json[0]["Station Name"])

    i = 0
    for each in json[1]:
        if i >= len(json[1]):
            break
        else:
            craftlist.append(Craft(each["Module Name"], each["Kind"]))
            craftlist[i].uuid = each["uuid"]
            craftlist[i].treedepth = each["Tree Depth"]
            i += 1
    for each in craftlist:
        if each.kind == "Core":
            station.core = each
            break


    i = 0
    for craft in craftlist:
        for dic in json[1]:
            if craft.uuid == dic["uuid"]:
                search = dic["Parent"]
                if search != "None":
                    for each in craftlist:
                        if each.uuid == search:
                            craft.parent = each
    for craft in craftlist:
        for dic in json[1]:
            if craft.uuid == dic["uuid"]:
                if dic["Children"] != "None":
                    for each in dic["Children"]:
                       for each2 in craftlist:
                           if each2.uuid == each:
                               craft.children.append(each2)
    return station

class Port:
    def __init__(self, name, side, root):
        self.uuid = str(uuid.uuid4())
        self.name = name
        self.side = side
        self.root = root
        self.connection = None

class Craft:
    def __init__(self, name, kind):
        self.uuid = str(uuid.uuid4())
        self.name = name
        self.kind = kind
        self.status = ""
        self.location = ""
        self.portlist = []
        self.parent = None
        self.children = []
        self.treedepth = 0
    
    def addPort(self, name, side):
        newport = Port(name, side, self)
        self.portlist.append(newport)

    def dock(self, srcportname, tgtmodule, tgtportname):
        srcport = None
        for each in self.portlist:
            if each.name == srcportname:
                srcport = each
                break
        tgtport = None
        for each in tgtmodule.portlist:
            if each.name == tgtportname:
                tgtport = each
                break

        srcport.connection = tgtport
        tgtport.connection = srcport
        self.parent = tgtmodule
        self.treedepth = self.parent.treedepth + 1
        tgtmodule.children.append(self)

    def listChildrenRecursive(self, output):
        if self.children is not []:
            for each in self.children:
                output.append(each)
                each.listChildrenRecursive(output)

#class CraftEncoder(json.JSONEncoder):
#    def default(self, o):
#        if isinstance(o, Craft):
#            portlist = []
#            for each in o.portlist:
#                
#            return (o.uuid, o.name, o.kind)
#        else:
#            return super().default(o)



class LV:
    def __init__(self, name):
        self.name = name

class ReadyList:
    def __init__(self):
        self.list = []


#--------------------------------------
print("Welcome to Orbital Dawn Lite! Create your station and guide it to self\n"\
    "sustainability and success.")
command = input("Press Enter to begin.")
stdscr = curses.initscr()
curses.start_color()
curses.noecho()
curses.cbreak()
curses.mousemask(curses.REPORT_MOUSE_POSITION | curses.ALL_MOUSE_EVENTS)
stdscr.keypad(True)


curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)


kinnison = SpaceCenter("Kinnison Space Center")

initialstation = Station("Joint Space Station")

luna = Craft("Luna", "Core")
luna.addPort("A", "Fore")
luna.addPort("B", "Aft")

initialstation.core = luna

fgb = Craft("FGB", "Module")
fgb.addPort("A", "Fore")
fgb.addPort("B", "Aft")
fgb.addPort("C", "Port")
fgb.addPort("D", "Starboard")

fgb.dock("A", luna, "A")

module2 = Craft("Module 2", "Module")
module2.addPort("A", "Fore")
module2.dock("A", fgb, "B")

module3 = Craft("Module 3", "Module")
module3.addPort("A", "Fore")
module3.dock("A", fgb, "C")

module4 = Craft("Module 4", "Module")
module4.addPort("A", "Fore")
module4.dock("A", fgb, "D")

file = open("station.json", 'r')


initialcraftlist = []
initialstation = decodestation(json.loads(file.read()), initialcraftlist)
        


running = True
while(running == True):
    safeprint(stdscr, 0,0,"Main menu:", curses.color_pair(1))
    safeprint(stdscr, 1,0,"(C)ommand Center", curses.color_pair(1))
    safeprint(stdscr, 2,0,"(S)tation View", curses.color_pair(1))
    safeprint(stdscr, 3,0,"(Q)uit game", curses.color_pair(1))
    command = inputwrapper(stdscr)
    if command == 0:
        continue
    if command == "q":
        if quitprompt(stdscr):
            running = False
        else:
            stdscr.clear()
            continue
    if command == "c":
        commandcenter(stdscr)
    if command == "s":
        stationview(stdscr)
    else:
        safeprint(stdscr, curses.LINES - 1, 0, command + "Invalid input or not yet implemenenented!", curses.color_pair(3))
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()

