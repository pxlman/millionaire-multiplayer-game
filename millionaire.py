import socket
import threading
from time import sleep
import random
from rich.console import Console
from rich.prompt import Prompt
from rich.live import Live

# Create a rich console instance
console = Console()

def chooseType():
    printHeader()
    # Options for the menu
    options = ["Create game", "Join game", "Exit"]
    for i, option in enumerate(options):
        console.print(f"[bold cyan]{i+1}[/bold cyan]: {option}")
    selected_i = Prompt.ask("Choose who are you: ", choices=["1", "2", "3"])
    if selected_i == "1": # Create game
        # Create a game
        return "server"
        # console.clear()
        # console.print("Waiting for a player...")
        # pass
    elif selected_i == '2':
        return "client"
    else:
        return "exit"

def getQuestion():
    # This should get the question from the server
    # and return it
    questions = [
        ["What is the derivative of sin(x)",                             "cos(x)", "tan(x)", "cot(x)", "sec(x)"],
        ["What is the integral of sin(x)",                               "-cos(x)", "cos(x)", "tan(x)", "cot(x)"],
        ["What is the derivative of cos(x)",                             "-sin(x)", "sin(x)", "tan(x)", "cot(x)"],
        ["What is the integral of cos(x)",                               "sin(x)", "-sin(x)", "tan(x)", "cot(x)"],
        ["What is the derivative of tan(x)",                             "sec^2(x)", "csc^2(x)", "sec(x)", "csc(x)"],
        ["What is the integral of tan(x)",                               "ln|sec(x)|", "ln|csc(x)|", "ln|sec^2(x)|", "ln|csc^2(x)|"],
        ["What is the derivative of cot(x)",                             "-csc^2(x)", "csc^2(x)", "sec^2(x)", "-sec^2(x)"],
        ["What is the integral of cot(x)",                               "ln|sin(x)|", "ln|cos(x)|", "ln|sin^2(x)|", "ln|cos^2(x)|"],
        ["What is the derivative of sec(x)",                             "sec(x)tan(x)", "sec(x)cot(x)", "csc(x)tan(x)", "csc(x)cot(x)"],
        ["What is the integral of sec(x)",                               "ln|sec(x) + tan(x)|", "ln|sec(x) - tan(x)|", "ln|csc(x) + cot(x)|", "ln|csc(x) - cot(x)|"],
        ["What is the derivative of csc(x)",                             "-csc(x)cot(x)", "csc(x)cot(x)", "-sec(x)tan(x)", "sec(x)tan(x)"],
        ["What is the integral of csc(x)",                               "ln|csc(x) - cot(x)|", "ln|csc(x) + cot(x)|", "ln|sec(x) - tan(x)|", "ln|sec(x) + tan(x)|"],
        ["What is the element with the symbol 'H'",                      "Hydrogen", "Helium", "Hafnium", "Hassium"],
        ["What is the element with the symbol 'He'",                     "Helium", "Hydrogen", "Hafnium", "Hassium"],
        ["What is the element with the symbol 'Li'",                     "Lithium", "Lutetium", "Lawrencium", "Livermorium"],
        ["What is the element with the symbol 'Be'",                     "Beryllium", "Bismuth", "Bohrium", "Boron"],
        ["What is the element with the symbol 'B'",                      "Boron", "Bismuth", "Bohrium", "Beryllium"],
        ["What is the element with the symbol 'C'",                      "Carbon", "Calcium", "Curium", "Copper"],
        ["What is the element with the symbol 'N'",                      "Nitrogen", "Neon", "Nobelium", "Nickel"],
        ["What is the element with the symbol 'O'",                      "Oxygen", "Osmium", "Oganesson", "Osmium"],
        ["What is the symbol for the organic compound 'Methane'",        "CH4", "CO2", "H2O", "NH3"],
        ["What is the symbol for the organic compound 'Ammonia'",        "NH3", "CO2", "H2O", "CH4"],
        ["What is the symbol for the organic compound 'Ethanol'",        "C2H5OH", "CH3OH", "C3H7OH", "C4H9OH"],
        ["What is the symbol for the organic compound 'Methanol'",       "CH3OH", "C2H5OH", "C3H7OH", "C4H9OH"],
        ["What is the symbol for the organic compound 'Propanol'",       "C3H7OH", "CH3OH", "C2H5OH", "C4H9OH"],
        ["What is the symbol for the organic compound 'Butanol'",        "C4H9OH", "CH3OH", "C2H5OH", "C3H7OH"],
        ["What is the symbol for the organic compound 'Acetic Acid'",    "CH3COOH", "HCOOH", "CH3OH", "HCOOH"],
        ["What is the symbol for the organic compound 'Formic Acid'",    "HCOOH", "CH3COOH", "CH3OH", "HCOOH"],
        ["What is the symbol for the organic compound 'Methyl Alcohol'", "CH3OH", "HCOOH", "CH3COOH", "HCOOH"],
        ["What is the symbol for the organic compound 'Ethyl Alcohol'",  "C2H5OH", "HCOOH", "CH3COOH", "CH3OH"],
    ]
    question =  random.choice(list(questions))
    return question

def printHeader():
    console.clear()
    console.print("\n\n##############################################", style="bold magenta")
    console.print("##############################################\n", style="bold magenta")
    console.print("Welcome to the Millionaire Game!", style="bold magenta")
    console.print("\n##############################################", style="bold magenta")
    console.print("##############################################\n", style="bold magenta")

def getReady():
    for i in range(5):
        printHeader()
        console.print(5-i)
        sleep(1)

def showQuestion(question, answers, score, oscore):
    # question, answers = getQuestion()
    right_answer = answers[0]
    console.clear()
    printHeader()
    console.print("Score: ", score)
    console.print("Opponent Score: ", oscore)
    console.print(f"Question: {question}")
    for i, option in enumerate(answers, 1):
        console.print(f"{i} - {option}")
def playerAnswer(answers, player):
    ans = Prompt.ask("Choose wisely", choices=["1", "2", "3", "4"])
    answer = answers[int(ans) - 1]
    console.print(f"Selected: {answer}")
    sleep(1)
    player.answer(answer)
    # This should get the answer from the player
    # and send it to the server
    # and return the result
    # shows the new question

class Player:
    def __init__(self):
        self.score = 0
        self.oscore = 0
        self.first = True

class Client(Player):
    def waitAnswer(self):
        while True:
            qs = self.peer.recv(1024).decode()  # Buffer size
            if qs: # Got a msg
                self.question = qs.split(",")
                self.newQuestion()
            else: # didn't and connection lost
                console.print("Connection closed!")
                # Close the connection
                self.peer.close()
                break
    def connect(self):
        printHeader()
        self.d_ip = Prompt.ask("Please enter the server IP")
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peer_socket.connect((self.d_ip, 12345))
        self.peer = peer_socket
        threading.Thread(target=self.waitAnswer).start()
    def newQuestion(self, mine = False):
        if not mine and not self.first:
            self.oscore += 1
        self.first = False
        answers = self.question[1:5]
        random.shuffle(answers)
        showQuestion(self.question[0], answers, self.score, self.oscore)
        threading.Thread(target=playerAnswer, args=(answers, self)).start()
        # console.print(self.question)
        # console.print(answers)
    def answer(self, ans):
        self.peer.send(ans.encode())
        # result = self.peer.recv(1024).decode()
        if self.question[0] == ans:
            self.score += 1
            self.newQuestion(True)
        else:
            self.newQuestion()

class Server(Player):
    def waitAnswer(self):
        while True:
            ans = self.peer.recv(1024)  # Buffer size
            if ans: # Got a msg
                # if ans == self.question[1]:
                #     self.peer.send(b"1")
                # else:
                #     self.peer.send(b"0")
                self.newQuestion()
                self.peer.send(",".join(self.question).encode())
            else: # didn't and connection lost
                console.print("Connection closed!")
                # Close the connection
                self.peer.close()
                break
    def connect(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # An ipv4/tcp connection
        server_socket.bind(('127.0.0.1', 12345)) # Each socket is a destination ip and a port this called a socket
        server_socket.listen()  # listens to the binded socket
        console.print("Waiting for a player...")
        peer_socket, peer_address = server_socket.accept() # Accept a connection to the socket
        self.peer = peer_socket
        self.newQuestion()
        # Thread that waites the client's answer
        # self.waitAnswer()
        threading.Thread(target=self.waitAnswer).start()
    def newQuestion(self, mine = False):
        if not mine and not self.first:
            self.oscore += 1
        self.first = False
        self.question = getQuestion()
        self.peer.send(",".join(self.question).encode())
        answers = self.question[1:5]
        random.shuffle(answers)
        showQuestion(self.question[0], answers, self.score, self.oscore)
        threading.Thread(target=playerAnswer, args=(answers, self)).start()
        # console.print(self.question)
        # console.print(answers)
    # The server answer
    def answer(self,ans):
        if ans == self.question[1]:
            self.score += 1
            self.newQuestion(True)
        else:
            self.newQuestion()

def main():
    type = chooseType()
    if type == "server":
        player = Server()
        player.connect()
    elif type == "client":
        player = Client()
        player.connect()
    pass
main()
