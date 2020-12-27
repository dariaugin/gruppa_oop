from tkinter import *
import tkinter as tk
from tkinter import ttk
from Map import Map
import Animal
import Simulation
from Statistics import Statistics
import os, pickle
from tkinter import messagebox
from tkinter.tix import *


class interface(Frame):
    def __init__(self,parent):
        self.parent = parent
        self.frame = Frame(self.parent,  background = "white")
        self.parent.title("program")
        self.frame.pack(expand = True, fill = "both")
        interface_op.centerWindow(self, 400, 450)
        self.create_menu(self.frame)

    def create_menu(self,frame):
        self.header_menu = Label(frame,text="Меню", bg = "white", font="Georgia 28")
        self.header_menu.pack( pady = 35)
        commands = [self.open_maps_w, self.open_statistics_w, self.open_new_map_mode ]
        labels = ["Карти","Статистика","Створити нову карту"]
        for i in range(len(commands)):
            Button(frame,text=labels[i], font = "Georgia 16", bg = "#6ae596",  activebackground = "white" ,command = commands[i]).pack(pady = 20)
    def open_statistics_w(self):
        self.new = Toplevel(self.parent)
        program = statistics_info(self.new)
    def open_maps_w(self):
        self.new_m = Toplevel(self.parent)
        program = maps_window(self.new_m)
    def open_new_map_mode(self):
        self.new_m_mode = Toplevel(self.parent)
        program = new_map(self.new_m_mode)

class statistics_info:
    def __init__(self,parent):
        self.parent = parent
        self.frame = Frame(self.parent,  background = "white")
        self.parent.title("statistics")
        self.frame.pack(expand = True, fill = X)
        interface_op.centerWindow(self, 700,400)
        self.parent.resizable(width=False, height=False)
        self.statistics_menu(self.frame)

    def statistics_menu(self, frame):
        interface_op.add_go_back(self, self.parent)
       
        new_frame = Frame(frame, bg = "#edeff4")
        
        self.list_box = Listbox(new_frame,width = 25, height = 15 , bg = "white", highlightcolor = "pink", font = "Georgia 9",bd = 3,selectbackground = "#81a7ee")
        self.list_box_2 = Listbox(new_frame,width = 40, height = 15 , bg = "white",highlightcolor = "pink", font = "Georgia 9",bd = 3,selectbackground = "#81a7ee")
        
        i_f = Frame(frame, background = "white")
        i_f.pack(expand = True, fill = X)
        Button(i_f, text = "Інформація", bg = "#89d77e", font="Georgia 13", command = self.fill_second_table).pack(side = RIGHT , pady = 5, padx = 25)
        Label(i_f, text = "- Оберіть файл:", bg = "white",  font="Georgia 15").pack(padx = 13,side = LEFT)
        
        new_frame.pack(pady = 1)
        self.list_box.pack(side = LEFT ,padx = 10)
        self.list_box_2.pack(side = RIGHT, padx = 10)
        
        Label(frame, text = "Оберіть тип статистики:",bg = "white", font="Georgia 13").pack(padx = 25)

        frame_s = Frame(frame, bg = "white")
        frame_s.pack(pady = 4)
        frame_k = Frame(frame, bg = "white")
        frame_k.pack(pady = 4)
        statistics = ["1 - Кількість травоядних/час ", "2 - Кількіть хижаків/час", "3 - Хижаки та травоядні/час", "4 - Відношення хиж. до тр./ час" , "5 - Кількість хижаків/день у обраний день :"]
        commands = [ lambda: self.fill_second_table(1), lambda: self.fill_second_table(2),  lambda: self.fill_second_table(3), lambda: self.fill_second_table(4), lambda: self.fill_second_table(5) ]

        for i in range(len(commands)):
            if i < 3:
                Button(frame_s, text =statistics[i], bg = "#d5fac8",  font="Georgia 10", command = commands[i]).pack(padx = 5,side = LEFT)
            
            else:
                Button(frame_k, text =statistics[i], bg = "#d5fac8",  font="Georgia 10", command = commands[i]).pack(padx = 5, side = LEFT)
        Label(frame_k, text = "День:",bg = "white",  font="Georgia 10").pack(padx = 3, pady = 2, side = LEFT)
        
        self.combbox = ttk.Combobox(frame_k,width =  3, values = [i for i in range(101)])
        self.combbox.current(0)
        self.combbox.pack( padx = 3, side = LEFT)
        try:
            elements = os.listdir("statistics_directory")
            interface_op.fill_table(elements, self.list_box)
        except:
            messagebox.showerror("Нема файлів", "У вас ще нема жодної статистики. Створіть нову симуляцію.", parent= self.parent)

    def fill_second_table(self, type = 0):
        s = self.list_box.curselection()
        if s:
            choise = self.get_stat()
            self.last_choise = choise
            self.list_box_2.delete(0, 'end')
            
            for i in reversed(range(len(choise.simulationsData))):  
                self.list_box_2.insert(0,"> Симуляція "+ str(i+1))

        elif self.list_box_2.curselection():
            s2 = self.list_box_2.curselection()
            if ">" in self.list_box_2.get(s2[0]):
                    num_of_sim = s2[0]
                    if type == 0:
                        self.show_info_about_simul(self.last_choise,num_of_sim)
                    elif type == 1:
                        self.last_choise.PreyPerTime(num_of_sim+1)
                    elif type == 2:
                        self.last_choise.HuntersPerTime(num_of_sim+1)
                    elif type == 3:
                        self.last_choise.HuntAndPreyPerTime(num_of_sim+1)
                    elif type == 4:
                        self.last_choise.HuntToPreyPerTime(num_of_sim+1)
                    elif type == 5:
                       
                        try:
                            self.last_choise.BarDiagramHunters(int(self.combbox.get()))
                        except:
                            self.combbox["foreground"] = "red"
                            messagebox.showerror("Кількість днів", "У обраний вами день информації про симуляцію нема. Оберіть інший день.", parent=self.parent)
                
    def get_stat(self):
        s = self.list_box.curselection()
        if s:
            selection = self.list_box.get(s[0])
            
            sm = Statistics.loadStatistics(selection)
            return sm
    
    def show_info_about_simul(self, obj, num_of_sim):
        self.list_box_2.delete(0, 'end')
        
        array_map = ["Висота карти: ", "Ширина карти: ", "Вода: ", "Каміння: ", "Трава: "]
        types_1 = ["Миша: ", "Жаба: ","Нелітаючий птах: "]
        types = ["Їжак: ", "Змія: ","Ласка: "]
        array_sim = ["Кількість тварин: ", "Відсоток тварин відносно площі: ", "Співвідношення хиж. до трав. : "] 
        object_m = obj.mapData

        object_s = obj.startSimulationsData[num_of_sim+1]
        for i in reversed(range(3)):
            self.list_box_2.insert(0, types_1[i]+ str(object_s[4][i]))

        self.list_box_2.insert(0, "Відсоток травоядних: ")

        for i in reversed(range(3)):
            self.list_box_2.insert(0, types[i]+ str(object_s[3][i]))
        self.list_box_2.insert(0, "Відсоток хижаків: ")
        for i in reversed(range(3)):
            self.list_box_2.insert(0, array_sim[i]+ str(object_s[i]))    

        self.list_box_2.insert(0, "Інформація про симуляцію: ")

        for i in reversed(range(3)):
            self.list_box_2.insert(0, array_map[i + 2]+ str(object_m[2][i]))

        self.list_box_2.insert(0, "Співвідношення фрагментів карти: ")

        for i in reversed(range(2)):
            self.list_box_2.insert(0, array_map[i]+ str(object_m[i]))

    def create_labels(self, frame):

        self.m = Label(frame, text = "Інформация про карту: ")

        self.h = Label(frame, text = "Висота:")
        self.height = Label(frame, text = "")

        self.w =Label(frame, text = "Ширина:")
        self.width = Label(frame, text = "")

        self.ratio = Label(frame, text = "Співвідношення фрагментив карти:")
        self.water_l = Label(frame, text = "")
        self.grass_l = Label(frame, text = "")
        self.rock_l = Label(frame, text = "")

        self.m.pack(pady =0.2, side ="left", fill = "x" )
        self.h.pack(pady =0.2, side ="left", fill = "x" )
        self.height.pack(pady = 0.2)
        self.w.pack(pady = 0.2)
        self.width.pack(pady = 0.2)
        self.ratio.pack(pady = 0.2)
        self.water_l.pack(pady = 0.2)
        self.grass_l.pack(pady = 0.2)
        self.rock_l.pack(pady = 0.2)

class maps_window():
    def __init__(self,parent):
        self.parent = parent
        self.frame = Frame(self.parent,  background = "white")
        self.parent.title("maps")
        self.frame.pack(expand = True, fill = "both")
        interface_op.centerWindow(self, 600, 350)
        self.parent.resizable(width=False, height=False)
        self.maps(self.frame)
    def maps(self,frame):
        interface_op.add_go_back(self, self.parent)
        Label(frame, text = " - Оберіть файл з картою:", bg = "white" , font="Georgia 12 bold").pack()
        new_frame = Frame(frame, bg = "white")
        new_frame.pack(pady = 10)
        self.list_box_map = Listbox(new_frame,width = 30, height = 10 ,highlightcolor = "#81a7ee",bd = 3,selectbackground = "#81a7ee", font ="Georgia 9")
        self.list_box_map.pack(padx = 5, side = LEFT)
        try:
            elements = os.listdir("maps_directory")
            interface_op.fill_table(elements, self.list_box_map)
        except:
            messagebox.showerror("Нема файлів", "У вас ще нема жодної карти. Створіть нову.", parent= self.parent)

        self.list_box_map_2 = Listbox(new_frame,width = 30, height = 10  , font = "Georgia 9" ,highlightcolor = "blue",bd = 5,selectbackground = "#81a7ee")
        self.list_box_map_2.pack( padx = 5, side = RIGHT)

        names = ["Інформація", "Показати", "Обрати" ]
        commands = [self.fill_second_table_map,self.show_map, self.choose_map]
        frame_butt = Frame(frame, bg = "white")
        frame_butt.pack(pady = 5)
        for i in range(len(names)):
            Button(frame_butt, text = names[i], font="Georgia 12",  bg = "#d5fac8", command = commands[i]).pack(side = LEFT, padx = 5)
            
    def choose_map(self):
        if self.list_box_map.curselection():
            interface_op.create_simulation_on_map(self, self.get_map())
            
    def get_map(self):
        s = self.list_box_map.curselection()
        if self.list_box_map.curselection():
            selection = self.list_box_map.get(s[0])
            sm = Map.loadMap(selection)
            return sm
    def fill_second_table_map(self):
        if self.list_box_map.curselection():
            self.list_box_map_2.delete(0, 'end')
            info = self.get_map()
            mas = ["Висота: "+str(info.height), "Ширина: "+str(info.width), "Частка водного простору: "+ str(info.terrainRatio[0]),  "Частка кам'яного простору: "+ str(info.terrainRatio[1]),  "Частка трав'яного простору: "+ str(info.terrainRatio[2])]
            
            for i in reversed(range(len(mas))):
                self.list_box_map_2.insert(0, mas[i] )
            
    def show_map(self):
        if self.list_box_map.curselection():
            map = self.get_map()
            map.showMapGraphic()
    
class new_map():
    def __init__(self,parent):
        self.parent = parent
        self.frame = Frame(self.parent,  background = "white")
        self.parent.title("new map")
        self.parent.resizable(width=False, height=False)
        self.frame.pack(expand = True, fill = "both")
        interface_op.centerWindow(self, 400, 550)
        self.show_options(self.frame)

    def show_options(self, frame):
        interface_op.add_go_back(self, self.parent)
        self.ctreate_entrys(frame)
        
    def ctreate_entrys(self,frame_init):    
        frame = Frame(frame_init, bg = "white")
        frame.pack(pady = 20)
        
        headers = ["Визначимо особливості карти:", "Визначимо частки складових карти: " ]
        text = [ "Висота:", " Ширина: ", "-Частка водного простору: ", "-Частка кам'яного простору:", "-Частка трав'яного простору:" ]

        label_h = []
        label = []

        entry = []
        self.entry_str = []

        for i in headers:
            label_h.append(Label(frame, text = i, font ="Georgia 12 bold", foreground = "#364834", bg = "#d5fac8"))
        for i in range(len(text)):
            label.append(Label(frame, text = text[i], font ="Georgia 11", bg = "white"))
            self.entry_str.append(StringVar())
            entry.append(Entry(frame,bg = "#e8ecda", textvariable = self.entry_str[-1]))

        i_h = 0
        i_t = 0
              
        for i in range(len(headers)+ len(text)):
            if i == 0 or i ==3:
                
                label_h[i_h].pack(pady = 10)
                i_h+=1
            else:
                
                label[i_t].pack(pady = 3)
                entry[i_t].pack(pady = 3)
                i_t +=1
        Button(frame, bg = "#cccdce", foreground = "#383b3a", font ="Georgia 11 bold", text = "Готово" ,command=self.create_map).pack(pady = 20)  
    
    def compose_data(self, data, parent):
        if interface_op.validation(data, parent):
            result_data = [ int(num) for num in data]
            result_data[2] = [result_data[2],result_data[3], result_data[4]]
            self.result_data = result_data[:3]
            return True
    
    def create_map(self):
        data = [el.get() for el in self.entry_str]  
        if self.compose_data(data, self.parent):
            map = self.create_map_obj()
            map.saveMap()
            self.ask_to_show_map(map)
            interface_op.create_simulation_on_map(self, map)

    def create_map_obj(self):
        MapObj =  Map(self.result_data[0],self.result_data[1],self.result_data[2])
        return MapObj

    def show_map(self, map):
            map.showMapGraphic()
    
    def ask_to_show_map(self, map):
            answer = messagebox.askyesno("Успіх!","Чи хочете ви побачити карту?")  
            if answer:
                self.show_map(map)

class new_simulation():
    def __init__(self,parent, map,b):
        self.b = b
        self.map = map
        self.data_sim =[]
        self.parent = parent
        self.parent.resizable(width=False, height=False)
        self.frame = Frame(self.parent,  background = "white")
        self.parent.title("new simulation")
        self.frame.pack(expand = True, fill = "both")
        interface_op.centerWindow(self, 400, 800)
        self.create_mode(self.frame)
        
    def create_mode(self, frame):
        interface_op.add_go_back(self, self.b.parent)
        self.create_elements(frame)
        
    def create_elements(self,frame):
        self.entry_string = []
        self.entrys = []
        for i in range(11):
            self.entry_string.append(StringVar())
            self.entrys.append(Entry(frame,bg = "#e8ecda", textvariable = self.entry_string[-1]))

        headers = ["Визначимо особливості симуляції:", "Процент хижаків та травоїдних : ","Частка хижаків:",  "Частка травоїдних:",  ]
        text = [ " Відсоток тварин:", "-Хижаки: ", "-Травоїдні: ", "-Hedgehog", "-Snake" , "-Weasel", "-Mouse", "-Frog", "-FlightlessBird", "Максимальна кількість днів симуляції: ", "Кількість циклів за один день: "]
        self.labels_h = []
        self.labels = []
        for i in headers:
            self.labels_h.append(Label(frame, text = i, font ="Georgia 12 bold", foreground = "#364834", bg = "#d5fac8"))
        for i in text:
            self.labels.append(Label(frame, text = i, font ="Georgia 11", bg = "white"))

        i_h = 0
        i_t = 0
        for i in range(len(headers)+len(text)):
            if i == 0 or i == 2 or i == 5 or i == 9:
                self.labels_h[i_h].pack(pady = 3)
                i_h+= 1
            else:
                self.labels[i_t].pack(pady = 1) 
                self.entrys[i_t].pack(pady = 1)
                i_t += 1

        j = Frame(frame)
        Label(j,text ="Візуалізувати процес симуляції?", font ="Georgia 9").pack(side = LEFT)
        self.r_var = BooleanVar()
        self.r_var.set(0)
        self.r1 = Radiobutton(j,text='Ні', font ="Georgia 9",
                 variable=self.r_var, value=False)
        self.r2 = Radiobutton(j,text='Так', font ="Georgia 9",
                 variable=self.r_var, value=True)   
        j.pack(pady = 9)
        self.r1.pack(side = LEFT)
        self.r2.pack(side = LEFT)

        k = Frame(frame,  background = "white")
        k.pack(pady = 5)
        Button(k, text = "Готово", bg = "#d5fac8",  font ="Georgia 10", command = self.end_of_creation).pack(side = LEFT, padx = 15)
        Button(k, text = "Додати ще одну симуляцію", bg = "#d5fac8",  font ="Georgia 10", command = self.add_new_sim).pack(side = LEFT, padx = 15)

    def compose_data(self):
        data = [el.get() for el in self.entry_string]
      
        if interface_op.validation(data, self.parent, 1):
            data = [int(el) for el in data]
            data[1] = [data[1],data[2]]
            data[2] = [data[3],data[4], data[5]]
            data[3] = [data[6],data[7], data[8]]
            data[4] = self.r_var.get()
            data[5] = data[9]
            data[6] = data[10]
            self.data_sim.append(data[:7])
            
            return True
        else:
            False
            
    def clear_fields(self):
            for el in self.entrys:
                el.delete(0, tk.END)
        
    def add_new_sim(self):
        if self.compose_data():
            self.clear_fields()

    def end_of_creation(self):
        if self.compose_data():
            a = fasad(self.map,self.data_sim)
            a.start_simulation()
            interface_op.close(self.parent)
            
class fasad:
    def __init__(self,map,sim_data):
        self.map = map
        self.sim_data = sim_data
        self.amount_of_sim = len(self.sim_data)
    
    def start_simulation(self):
        self.new_statistics = Statistics()
        
        for i in range(self.amount_of_sim):
            self.new_simulation = Simulation.Simulation(i+1, self.new_statistics, self.map, self.sim_data[i][0], self.sim_data[i][1], self.sim_data[i][2], self.sim_data[i][3], self.sim_data[i][4], self.sim_data[i][5],  self.sim_data[i][6])
            self.new_simulation.run()
        
        self.new_statistics.saveStatistics()

class interface_op:
    @staticmethod
    def validation(data_array, parent, mode = False):
        if mode:
            for i in range(len(data_array)):
                if data_array[i].isdigit() and int(data_array[i]) >= 0:
                    if i == 2 and (int(data_array[i-1])+int(data_array[i])) != 100:
                        messagebox.showerror("Невірно введені дані", "Значення мають у сумі дорівнювати 100. Введить значення ще раз", parent=parent)
                        return False
                    if (i == 5 or i == 8)  and (int(data_array[i-1])+int(data_array[i - 2])+int(data_array[i])) != 100:
                        messagebox.showerror("Невірно введені дані", "Значення мають у сумі дорівнювати 100. Введить значення ще раз", parent=parent)
                        return False
                    if (i == 9 or i == 10) and (int(data_array[i]) > 100 or int(data_array[i]) == 0):
                        messagebox.showerror("Невірно введені дані", "Кількість днів та ціклив не мають бути вищими за 100 та дорівнувати 0", parent=parent)
                        return False
                else:
                    messagebox.showerror("Невірно введені дані", "Значення мають бути цілими числа та більші за 0. Введіть значення ще раз", parent=parent)    
                    return False

            return True
        
        else:
            for i in range(len(data_array)):
                if data_array[i].isdigit() == False or int(data_array[i]) < 0:
                    messagebox.showerror("Невірно введені дані", "Значення мають бути цілими числами та більшими за 0. Введіть значення ще раз.", parent= parent)
                    return False
            if int(data_array[2]) + int(data_array[3]) +int(data_array[4]) != 100:
                messagebox.showerror("Невірно введені дані", "Частка води, землі та трави у сумі мають дорівнувати 100. Введіть значення ще раз.", parent= parent)
                return False
            if int(data_array[0]) > 10 and int(data_array[1]) > 10:
                    
                return True
            messagebox.showerror("Невірно введені дані", "Висота та ширина карти мають бути більші за 10.", parent= parent)
            return False

    @staticmethod
    def create_simulation_on_map(sel, map):
        sel.parent.withdraw()
        sel.new_s_mode = Toplevel(sel.parent)
        program = new_simulation(sel.new_s_mode, map, sel)   
        
    @staticmethod
    def add_go_back(window, parent):
        Button(window.frame, text = "назад", font = "Georgia 12 bold" , bg = "#71ed74", foreground = "white", width = 3, command = lambda: interface_op.close(parent)).pack(side = LEFT)

    @staticmethod
    def close(window):
        window.destroy() 
          
    @staticmethod
    def fill_table(files, list_box):
        for i in files:
            list_box.insert(0,i)

    @staticmethod
    def centerWindow(self, width, height):
        w = self.parent.winfo_screenwidth()//2-(width//2)
        h = self.parent.winfo_screenheight()//2-(height//2)
        self.parent.geometry('{}x{}+{}+{}'.format(width,height, w, h))


def main():
    root = Tk()
    root.configure(bg = "#d5fac8")
    root.resizable(width=False, height=False)
    program = interface(root)
    root.mainloop()

main()