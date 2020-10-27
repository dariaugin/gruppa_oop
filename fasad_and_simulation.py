
import subprocess,platform,time,random

class simulation:

    def __init__(self,map_ground,pr_predators,pr_herbivores,height,width,days):
        self.animals_matrix = [[0 for y in range(width)] for x in range(height)]

        self.pr_herbivores = pr_herbivores
        self.pr_predators = pr_predators
        self.pr_void = 100-(pr_herbivores+pr_predators)

        self.amount = height * width
        self.amount_predators = round(self.amount*pr_predators/100)
        self.amount_herbivores = round(self.amount*pr_herbivores/100)
        self.amount_void = self.amount - self.amount_predators - self.amount_herbivores

        self.statistics_for_sim = [[pr_predators,pr_herbivores,days]]
        self.map_matr = map_ground

        self.array_animals = []

        self.height = height
        self.width = width
        self.days = days
        
        

    def create_animals_matrix(self):
        choise_1 =["p","h","v"]
        choises_p = [snake,weasel,hedgehog]
        choises_h = [frog,mouse,flightless_bird]
        w = [self.pr_predators,self.pr_herbivores,self.pr_void]
        
        


        counter_p = 0
        counter_h = 0
        counter_v = 0

        for y in range(self.height):
            for x in range(self.width):
                w_t = tuple(w)
                ch = random.choices(choise_1, weights = w_t)[0]
                if ch == "p" :
                    
                    
                    if self.map_matr[y][x] == "rock":
                        choise = random.choice(choises_p[:2])

                        
                    elif self.map_matr[y][x] == "water":
                        choise =  choises_p[0]
                        
                    else:
                        choise = random.choice(choises_p)

                    self.animals_matrix[y][x] = choise(x,y)
                    self.array_animals.append(self.animals_matrix[y][x])
                        

                    counter_p += 1
                    if counter_p == self.amount_predators:
                        choise_1.remove("p")
                        w.remove(self.pr_predators)

                elif ch == "h":
                    
                    if self.map_matr[y][x] == "rock":
                        choise = random.choice(choises_h[:2])
                        
                        
                    elif self.map_matr[y][x] == "water":
                        choise =  choises_h[0]
                        
                        
                    else:
                        choise = random.choice(choises_h)
                        
                        
                    self.animals_matrix[y][x] = choise(x,y)
                    self.array_animals.append(self.animals_matrix[y][x])
                    counter_h += 1

                    if counter_h == self.amount_herbivores:
                        choise_1.remove("h")
                        w.remove(self.pr_herbivores)

                else:
                    counter_v +=1
                    if counter_v == self.amount_void:
                        choise_1.remove("v")
                        w.remove(self.pr_void)


    def print_animal_matrix(self):
        
            for i in range(self.height):
                for o in range(self.width): 
                    if self.animals_matrix[i][o] != 0:
                        print('{}{}'.format(self.animals_matrix[i][o].__str__(), (10-len(self.animals_matrix[i][o].__str__()))*" "),end = "")
                    else:
                        print("0{}".format(9*" "),end = "")
                print("\n")

    def visualize_process(self):
                print("simulation.......")
                self.print_animal_matrix()
                time.sleep(0.2)
                print("\033c",end = "")


    def start_simulation(self): 
        self.create_animals_matrix()
        for day in range(1,self.days+1):
            for creature in self.array_animals:
                creature.moving(self,creature)
                self.visualize_process()

            self.statistics_for_sim.append([self.amount_predators,self.amount_herbivores])

        
        
        
class fasad:
    
    def create_map(self):
            h = self.proverka(input("введіть висоту мапи (не менше 10 клітинок): "),"висоту",1)
            w = self.proverka(input("введіть ширину мапи (не менше 10 клітинок): "),"ширину",1)
        

            if input("Якщо ви хочете обрати waterIntervals(у іншому випадку значення буде обрано автоматично),то відправте '+' : ") == '+':
                waterIntervals = self.proverka([int(i) for i in input("введіть waterIntervals(2 цілих числа через проміжок): ").split() if i.isdigit() == True ],"waterIntervals",2)
                print(waterIntervals)
            else:
                waterIntervals = [1,8]
                

            if input("Якщо ви хочете обрати rockIntervals(у іншому випадку значення буде обрано автоматично),то відправте '+' : ") == '+':
                 rockIntervals = self.proverka([int(i) for i in input("введіть rockIntervals(2 цілих числа через проміжок): ").split() if i.isdigit() == True ],"rockIntervals",2)
                 
            else:
                rockIntervals = [0,1]

            if input("Якщо ви хочете обрати grassIntervals(у іншому випадку значення буде обрано автоматично),то відправте '+' : ") == '+':
                 grassIntervals = self.proverka([int(i) for i in input("введіть grassIntervals(2 цілих числа через проміжок): ").split() if i.isdigit() == True ],"grassIntervals",2)
            else:
                grassIntervals = [0,3]
            
            if input("Якщо ви хочете зберегти створену карту, то відправте '+' : ") == '+':
                save = True
            else:
                save = False
            
            print("Інформація про карту:\n висотa: {} \nширина: {}\nwaterIntervals: {}\nrockIntervals: {}\ngrassIntervals: {}\nsave: {}\n".format(h,w,waterIntervals,rockIntervals,grassIntervals,save))
            
            return h, w, waterIntervals,rockIntervals,grassIntervals,save

    def proverka(self,inp,word,action):
            if action == 1:
                while inp.isdigit() != True or int(inp)<10:
                    inp = input( word + " не може бути менше 10 клітинок, а також має бути тільки цілим числом. Введіть значення ще раз: ")
                return int(inp)
            if action == 2:
                    while len(inp) != 2:
                        array = input("введіть "+ word +" ще раз (2 цілих числа через проміжок): ").split()
                        if len(array) == 2:
                            inp = [ int(i) for i in array if i.isdigit() == True]
                            
                    
                    return inp
            if action == 3:
                while not inp.isdigit():
                    inp = input("Введіть відсоток "+word+" відносно загальної території ще раз(ціле додатне число): ")
                return int(inp)
                    



    
    def create_simulation(self):
        array = []
        amount = input("Cкільки симуляцій на заданій карті ви плануєте провести?: ")
        while not amount.isdigit() :
             amount = input("Введіть значення ще раз(ціле додатнє число).Cкільки симуляцій на заданій карті ви плануєте провести?: ")

        for i in range(int(amount)):

            print("Початок введення параметрів для симуляції", i+1, ": ")
            pr_p = self.proverka(input("Введіть відсоток хижаків відносно загальної території: "), "хижаків", 3)
            pr_h = self.proverka(input("Введіть відсоток травоядних відносно загальної території: "), "травоядних", 3)
            while pr_p + pr_h > 100:
                    print("Сума відсотку хижаків та травоядних не має перевищувати 100")
                    pr_p = self.proverka(input("Введіть відсоток хижаків відносно загальної території ще раз (ціле додатне число): "), "хижаків", 3)
                    pr_h = self.proverka(input("Введіть відсоток травоядних відносно загальної території ще раз (ціле додатне число): "), "травоядних", 3)


            days = input("Скільки днів має тривати симуляція?: ")
            while not days.isdigit():
                days = input("Введіть значення ще раз (ціле додатнє число).Скільки днів має тривати симуляція?: ")
            days = int(days)

            array.append([pr_p,pr_h,days])
        
        for el in range(len(array)):
            print("-------------------------------------")
            print("Введена інформація про симуляцію ",el+1)
            print("Процент хижаків: {}\nПроцент травоядних: {}\nКількість днів на дослідження: {}\n".format(array[el][0],array[el][1],array[el][2]))
        return array



    def start(self):
        while True:
            inp = input("Виберіть варіант(введіть число): \n1)Створити симуляцію на основі збереженої мапи\n2)Створити симуляцію на основі нової мапи \n3)Переглянути збережену статистику\n")
            while inp != "1" and inp != "2" and inp != "3" :
                inp = input("Виберіть варіант ще раз(введіть число): \n1)Створити симуляцію на основі збереженої мапи\n2)Створити симуляцію на основі нової мапи \n3)Переглянути збережену статистику\n")
            if inp == "1":
                print("/// показ існуючих наборів карт ///")
            elif inp == "2":
                    info_for_map = [i for i in self.create_map()]
                    st = statistics(info_for_map)
                    our_map = Map(info_for_map[0],info_for_map[1])
                    if info_for_map[-1]:
                        our_map.save_map()
                    if input("Якщо хочете переглянути карту, відправте '+': ") == "+":
                        our_map.show_map()
                    if input("Якщо плануєте продовжувати з цією картою, відправте '+': ") == "+":
                            inf_for_simulation = self.create_simulation()
                            for item in range(len(inf_for_simulation)):
                                s = simulation(our_map.map_matr,inf_for_simulation[item][0],inf_for_simulation[item][1],info_for_map[0],info_for_map[1],inf_for_simulation[item][2])
                                s.start_simulation()
                                st.add_statistics_for_sim(s.statistics_for_sim)
                                print("симуляція ",item+1," завершилася")
                                time.sleep(2)
                            st.print_stat_array()
                            if input("Якщо ви хочете зберегти статистику, введіть '+': ") == "+":
                                st.save()
                            return False
                    else:
                            return False
            elif inp == "3":
                print("///перегляд збереженої статистики///")
                return False



        




        
















# cпрощені в реалізації класи для візуалізації наведених методів та результатів

class animals:
    def __init__(self,x_c,y_c):
        self.x_c = x_c
        self.y_c = y_c
    def moving(self,data,animal):
        moves = ["l","r","f","b"]
        move = random.choice(moves)
        if move == "l":
            if animal.x_c != 0:
                y = animal.y_c
                x = animal.x_c-1
                move_to = data.animals_matrix[y][x]
            else:
                y = animal.y_c
                x = animal.x_c+1
                move_to = data.animals_matrix[y][x]
        if move == "r":
            if animal.x_c +1  != data.width:
                y = animal.y_c
                x = animal.x_c+1
                move_to = data.animals_matrix[y][x]
            else:
                y = animal.y_c
                x = animal.x_c-1
                move_to = data.animals_matrix[y][x]
        if move == "b":
            if animal.y_c  != 0 :
                y = animal.y_c - 1
                x = animal.x_c
                move_to = data.animals_matrix[y][x]
            else:
                y = animal.y_c + 1
                x = animal.x_c
                move_to = data.animals_matrix[y][x]
        if move == "f":
            if animal.y_c +1  != data.height:
                y = animal.y_c + 1
                x = animal.x_c
                move_to = data.animals_matrix[y][x]
            else:
                y = animal.y_c - 1
                x = animal.x_c
                move_to = data.animals_matrix[y][x]

        if move_to == 0:
            
            data.animals_matrix[animal.y_c][animal.x_c] = 0
            data.animals_matrix[y][x] = animal
            animal.x_c = x
            animal.y_c = y

        elif animal.type == "p" and move_to.type == "h":
            
            for el in data.array_animals:
                if el.x_c == move_to.x_c and el.y_c == move_to.y_c:
                    data.array_animals.remove(el)
            data.animals_matrix[move_to.y_c][move_to.x_c] = animal
            data.animals_matrix[animal.y_c][animal.x_c] = 0
            animal.y_c = move_to.y_c
            animal.x_c = move_to.x_c
            data.amount_herbivores -= 1
        
        



class herbivores:
        type = "h"

class mouse(animals,herbivores):
        def __init__(self,x,y):
            self.years = 3
            animals.__init__(self,x,y)
        def __str__(self):
            return "mouse"

class frog(animals,herbivores):
        def __str__(self):
            return "frog"

class flightless_bird(animals,herbivores):
        def __str__(self):
            return "bird"


class predators:
    type = "p"

class hedgehog(animals,predators):
        def __str__(self):
            return "hedgehog"
    
class snake(animals,predators):
        def __str__(self):
            return "snake"


class weasel(animals,predators):
    def __str__(self):
            return "weasel"


class statistics:
        def __init__(self,info_about_map):
            self.data_for_map = [info_about_map]
        def add_statistics_for_sim(self, simulation_statistics):
            self.data_for_map.append(simulation_statistics)
        def print_stat_array(self):
            print("Мапа:", self.data_for_map[0])
            for i in range(1,len(self.data_for_map)):
                print("Cимуляція "+ str(i)+ ": ",self.data_for_map[i])
        def save(self):
            print("//збереження статистики//")


class Map:
    options = ['rock','water','grass']
    def __init__(self,height,width):

        self.map_matr = [[random.choice(self.options) for b in range(width)] for j in range(height)]
    
    def show_map(self):
        print("//перегляд карти//")

    def save_map(self):
        print("//збереження карти//")
    

            





f = fasad()
f.start()

   

