
import random

# ////////////-------- INIT -----------//////////////////

class GamePlay:
    def __init__(self, first_num, second_num): # first and second number are randomed
        self.first_num = first_num 
        self.second_num = second_num

# ////////////-------- ADD -----------//////////////////

class Addition(GamePlay): # Plus operator.
    def __init__(self, first_num, second_num):
        super().__init__(first_num, second_num)  # from Class GamePlay.
        self.real_answer = first_num + second_num # the answer.
    
    def checker(self, user_answer):
        if user_answer == self.real_answer: # check user's answer = real answer or not?
            return True
        else:
            return False
        
    def __str__(self): 
        return f"{self.first_num} + {self.second_num} = ?"  # display the question.
    
    def randomanswer(self):
        random_number = set() # set,list of choices.
        while True: # Use a loop to ensure each choice in the list is not the same.

            num_make_close_realanswer = random.randint(1, 3) # Used to random a number in order to plus, minus or multiply with real answer to make a choice as closely as possible to the real answer.
            
            choice1 = self.real_answer - num_make_close_realanswer # Used to define each choice in the list as closely as possible to the real answer, make users hesitate before answering.
            choice2 = self.real_answer + num_make_close_realanswer 
            choice3 = self.first_num * self.second_num 

            if choice1 != choice2 and choice1 != choice3  and choice2 != choice3: # chek each choice in the list is not the same. it's reson why we use while loop.
                random_number.add(choice1) # if each choice in the list is not the same, add all choice into the list,set.
                random_number.add(choice2)
                random_number.add(choice3)
                random_number.add(self.real_answer)
                break
        return f"{' '.join(map(str, random_number))}" # display the list,set of choices.

# ////////////-------- SUBTRACTION -----------//////////////////

class Subtraction(GamePlay): # Same as class Addition.
    def __init__(self, first_num, second_num):
        super().__init__(first_num, second_num)
        self.real_answer = first_num - second_num

    def checker(self, user_answer):
        if user_answer == self.real_answer:
            return True
        else:
            return False
            
    def __str__(self):
        return f"{self.first_num} - {self.second_num} = ?"

    
    def randomanswer(self):
        random_num = set()
        while True:

            num_make_close_realanswer = random.randint(1, 3)
            
            choice1 = self.real_answer - num_make_close_realanswer
            choice2 = self.real_answer + num_make_close_realanswer
            choice3 = self.first_num * self.second_num

            if choice1 != choice2 and choice1 != choice3  and choice2 != choice3:
                random_num.add(choice1)
                random_num.add(choice2)
                random_num.add(choice3)
                random_num.add(self.real_answer)
                break
        return f"{' '.join(map(str, random_num))}"
    
# ////////////-------- MULTIPLICATION -----------//////////////////

class Multiplication(GamePlay): # Same as class Addition.
    def __init__(self, first_num, second_num):
        super().__init__(first_num, second_num)
        self.real_answer = first_num * second_num

    def checker(self, user_answer):
        if user_answer == self.real_answer:
            return True
        else:
            return False
            
    def __str__(self):
        return f"{self.first_num} x {self.second_num} = ?"

    
    def randomanswer(self):
        random_num = set()
        while True:

            num_make_close_realanswer1 = random.randint(1, 2)
            num_make_close_realanswer2 = random.randint(3, 9)
            
            choice1 = self.first_num * (self.second_num + num_make_close_realanswer1)
            choice2 = self.first_num * (self.second_num - num_make_close_realanswer1)
            choice3 = self.real_answer + num_make_close_realanswer2

            if choice1 != choice2 and choice1 != choice3  and choice2 != choice3:
                random_num.add(choice1)
                random_num.add(choice2)
                random_num.add(choice3)
                random_num.add(self.real_answer)
                break
        return f"{' '.join(map(str, random_num))}"
    
# ////////////-------- DIVISION -----------//////////////////

class Division(GamePlay):
    def __init__(self, first_num, second_num): ###second number can't be 0 because it is randomed since 1 - 10, So we don't need to check zero divition error ro not.
        super().__init__(first_num, second_num)
        self.real_answer = round(first_num / second_num, 2) # define the answer as 2 decimal

    def checker(self, user_answer):
        if user_answer == self.real_answer:
            return True
        else:
            return False
            
    def __str__(self):
        return f"{self.first_num} ÷ {self.second_num} = ?"
    
    def randomanswer(self):
        random_num = set()
        while True:
                num_make_close_realanswer1 = random.randint(1, 2) # Used to define each choice in the list as closely as possible to the real answer, make users hesitate before answering.
                num_make_close_realanswer2 = random.random()
                
                choice1 = round(self.first_num / (self.second_num + num_make_close_realanswer1), 2)
                choice2 = round(self.real_answer - num_make_close_realanswer2, 2)
                choice3 = round(self.real_answer + num_make_close_realanswer2, 2)

                if choice1 != choice2 and choice1 != choice3  and choice2 != choice3:
                    random_num.add(choice1)
                    random_num.add(choice2)
                    random_num.add(choice3)
                    random_num.add(self.real_answer)
                    break
            
        return f"{' '.join(map(str, random_num))}"
    

# ////////////-------- Maingame -----------//////////////////


def main():
    user_name = input("What is your name: ") # Ark user's name.
    point = 0  # define user's points as default.
    chance = 3  # define user's chance as default.
    while True: 
        operator = Division(random.randint(1,10), random.randint(1,10)) #Operation, For Multiplication uses random.radint(1,12), Others operator use random.radint(1,10).
        print(operator) # display the questions.
        print(operator.randomanswer()) # display the choices.
        userAns = float(input("Enter your answer: ")) # get user's answer.
        if operator.checker(userAns) == True: # check user's answer.
            point += 1
            print("---------------------------------------------------------------------------------")
            print("corrcet")
            print(f"Your corrent point = {point}")
            print("---------------------------------------------------------------------------------\n")
        else:  # check user's answer.
            chance -= 1
            if chance == 0: # check user's chance, If user's chance = 0, write user's point in scoreboard.
                print("\n---------------------------------------------------------------------------------")
                print("Incorrect")
                print(f"Your total point = {point}")
                print("Game over!!")
                print("---------------------------------------------------------------------------------")

                with open("Scoreboard" , "a") as user_point:
                    user_point.write(f"{user_name} of ponts = {point}\n")
                
                with open("Scoreboard" , "r") as user_points:
                    for i in user_points.readline():
                        print(i)
                break

            else: # check user's chance, If user's chance != 0, continue.
                print("\n---------------------------------------------------------------------------------")
                print("Incorrect")
                print(f"Your corrent point = {point}")
                print(f"Your chance = {chance}")
                print("---------------------------------------------------------------------------------")           

if __name__ == "__main__":
    main()