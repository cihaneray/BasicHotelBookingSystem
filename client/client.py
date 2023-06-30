from socket import socket, AF_INET, SOCK_STREAM  # pip install sockets
from hashlib import sha256
from time import sleep
import os
import matplotlib.pyplot as plt  # pip install matplotlib
from pickle import loads
import sys

client = socket(AF_INET, SOCK_STREAM)
client.connect(("IP ADDRESS", 8000))  # Enter Ip Address

permission = {"0": ["create_admin", "change_password", "change_permission", "get_graphic", "change_price"],
              "1": ["get_graphic", "change_price"],
              "2": ["get_graphic"]}  # Permission for admin


def clear_cmd():
    return os.system('cls' if os.name == 'nt' else 'clear')


def loading_screen(x, what):
    animation = "|/-\\"
    for i in range(x):
        sleep(0.1)
        sys.stdout.write("\r" + what + animation[i % len(animation)])
        sys.stdout.flush()


def user_booking():  # Booking
    clear_cmd()
    client.send("user".encode())
    date = input("Please enter first date [For example (01/01/2023)]\n> ")  # First Day
    days = input("Please enter last date [For example (01/01/2023)]\n> ")  # Last Day
    dates = date + "-" + days  # Combine to send to server
    client.send(dates.encode())  # Send to server
    available = client.recv(1024).decode()  # Receive
    if date != days:
        if available == "NotRoom":
            print("Sorry, there are no available rooms.")
            return loading_screen(20, "Returning to the menu ")
        else:
            print("Available room types: ", available)
            room_type = input(f"Please choose the room type\n{available} ").capitalize()
            if room_type == "":
                room_type = "noRoom"
            else:
                pass
            client.send(room_type.encode())  # Sent to server
            checking = client.recv(1024).decode()  # Receive
            if int(checking):
                print("Room type have not be empty!")
                return
            breakfast = input("Want you breakfast? [(1) for Yes] [(0) for No]: ")
            client.send(breakfast.encode("utf-8"))  # Send to server
            price = client.recv(1024).decode()  # Receive
            print(f"Total price is {price} TL")
            name_surname = input("Please enter name and surname: ")
            id_ = input("Please enter your id: ")
            phone_number = input("Please enter your phone number: ")
            while True:
                con_choice_1 = input(f"How do you want to pay?\n[(1) for Online] or [(2) for Hotel] ")
                if con_choice_1 == "1":
                    cc_number = input("Please enter your credit card number: ")
                    cc_vt = input("Please enter your credit card valid thru: ")
                    cc_cvv = input("Please enter your credit card cvv: ")
                    personal_info = "{0}-{1}-{2}-{3}-{4}-{5}\n".format(name_surname, id_,
                                                                       phone_number, cc_number,
                                                                       cc_vt, cc_cvv)
                    client.send(personal_info.encode("utf-8"))  # Send to server
                    break
                elif con_choice_1 == "2":
                    personal_info = "{0}-{1}-{2}-{3}\n".format(name_surname, id_, phone_number, "On Hotel")
                    break
                else:
                    print("Invalid value")
            client.send(personal_info.encode("utf-8"))  # Send to server
            print("Reservation successful!\nThanks for booking!")
            exit()
    else:
        print("Please enter different day")
        sleep(1)


class Admin:
    @staticmethod
    def login():
        clear_cmd()
        client.send("admin".encode())  # Send to server
        admin_name = input("Please enter your admin name: ")
        admin_password = sha256((input("Please enter your password: ")).encode("utf-8")).hexdigest()
        client.send((admin_name + "-" + admin_password).encode())  # Send to server
        login = client.recv(1024).decode()  # Receive
        if login == "1":
            return admin_name, True
        else:
            return None, False

    @staticmethod
    def new_password():
        clear_cmd()
        client.send("change_password".encode())  # Send to server
        old_password = sha256((input("Please enter current password: ")).encode("utf-8")).hexdigest()  # Hashing process
        new_password = input("Please enter new password: ")
        new_password_2 = input("Please enter new Password again: ")
        if new_password == new_password_2:
            new_password_cred = old_password + '-' + sha256(new_password.encode("utf-8")).hexdigest()
            client.send(new_password_cred.encode())  # Send to server
            if client.recv(1024).decode() == '1':  # Receive
                print("Your password has been changed!")
                sleep(1)
            else:
                print("Your current password is wrong!")
                sleep(1)
        else:
            print("New passwords is not same!")
            sleep(1)

    def change_permission(self):
        clear_cmd()
        client.send("change_permission".encode())  # Send to server
        change_user = input("Please enter admin name that do you want to change: ")
        change_level = input("Please enter authority level that do you want to change: ")
        change_ = change_user + "-" + change_level
        client.send(change_.encode())  # Send to server
        msg = client.recv(1024).decode()  # Receive
        if msg == "No username":
            print("Admin name not found")
            sleep(1)
            return self.change_permission()
        else:
            print(msg)
            sleep(1)

    @staticmethod
    def create_admin():
        clear_cmd()
        client.send("create_admin".encode())  # Send to server
        new_admin_name = input("Please enter new admin name: ")
        new_admin_password = sha256(input("Please enter new admin password: ").encode("utf-8")).hexdigest()  # Hashing
        new_admin_permission = input("Please enter new admin permission\n(0) or (1) or (2): ")
        new_admin_cred = new_admin_name + "-" + new_admin_password + "-" + new_admin_permission
        client.send(new_admin_cred.encode())  # Send to server
        if client.recv(1024).decode() == "1":  # Receive
            print(f"{new_admin_name} has been added as admin.")
            sleep(1)

    @staticmethod
    def change_price():
        clear_cmd()
        client.send("change_price".encode())  # Send to server
        breakfast_or_room = input(
            "What do you want to change?\n[(B) for breakfast price] [(R) for room price]: ").capitalize()
        if breakfast_or_room == "B":
            client.send("breakfast".encode())  # Send to server
            temp_breakfast_price = client.recv(1024).decode()  # Receive
            breakfast_changed_price = input(f"Breakfast price is {temp_breakfast_price}.\nPlease enter breakfast price "
                                            f"that do you want change\n[If you want to cancel, type (-1)]: ")
            client.send(breakfast_changed_price.encode())  # Send to server
            if breakfast_changed_price == "-1":
                print("Process is canceled!")
                return sleep(1)
            else:
                sleep(0.15)
                print(client.recv(1024).decode())  # Receive and print

        elif breakfast_or_room == "R":
            client.send("room".encode())  # Send to server
            room_changed_type = input("Please enter room type that do you want change\n"
                                      "[Economic] [Suit] [King]: ").capitalize()
            client.send(room_changed_type.encode())  # Send to server
            temp_room_type_price = client.recv(1024).decode()  # Receive
            room_changed_price = input(f"{room_changed_type} price is {temp_room_type_price}. \nPlease enter room "
                                       f"price that do you want change\n[If you want to cancel, type (-1)]: ")
            client.send(room_changed_price.encode())  # Send to server
            if room_changed_price == "-1":
                print("Process is canceled!")
                return sleep(1)
            else:
                print(client.recv(1024).decode())  # Receive and print
                sleep(1)

    @staticmethod
    def get_graphic():
        clear_cmd()
        client.send("get_graphic".encode())  # Send to server
        choice_1 = input("Income graph [1]\nOccupation ratio graph [2]\n> ")
        client.send(choice_1.encode())  # Send to server
        sleep(0.15)
        x, y = loads(client.recv(4096))  # Data loads with pickle library
        plt.figure(figsize=(12, 6))
        plt.plot(x, y, "b-.")
        plt.xticks(rotation=45)
        plt.xlabel('Months', )
        if choice_1 == "1":
            plt.ylabel('Total income in TL')
            plt.title('Excepted İncome Graphic In A Year')
        elif choice_1 == "2":
            plt.ylabel('Occupation ratio')
            plt.title('Occupation ratio in a year for months')
        plt.tight_layout()
        plt.show()


while True:
    clear_cmd()
    profile = input("Admin ---> [A]\nBooking -> [B]\nQuit ----> [Q]\n> ").capitalize()
    if profile == "B":
        user_booking()
    elif profile == "A":
        admin = Admin()
        name_admin, admin_result = admin.login()
        if admin_result:
            authority_level = client.recv(1024).decode()  # Receive
            while True:
                clear_cmd()
                choice = input(
                    f"Welcome {name_admin.capitalize()},"
                    " what would you like to do?\n"
                    "Change password -----------> [1]\n"
                    "Add new admin -------------> [2]\n"
                    "Change price --------------> [3]\n"
                    "Change admins permissions -> [4]\n"
                    "Get graphic ---------------> [5]\n"
                    "Close the session ---------> [6]\n> ")
                if choice == "1":
                    admin.new_password()
                elif choice == "2":
                    if "create_admin" in permission[authority_level]:
                        admin.create_admin()
                    else:
                        print("Invalid authorization level")
                        sleep(1)
                elif choice == "3":
                    if "change_price" in permission[authority_level]:
                        admin.change_price()
                    else:
                        print("Invalid authorization level")
                        sleep(1)
                elif choice == "4":
                    if "change_permission" in permission[authority_level]:
                        admin.change_permission()
                        if int(client.recv(1024)):  # Receive
                            break
                    else:
                        print("Invalid authorization level")
                        sleep(1)
                elif choice == "5":
                    if "get_graphic" in permission[authority_level]:
                        admin.get_graphic()
                    else:
                        print("Invalid authorization level")
                        sleep(1)
                elif choice == "6":
                    client.send("quit".encode())  # Send to server
                    loading_screen(15, "Closing the session ")
                    break
                else:
                    print("Invalid value")
                    sleep(1)
        else:
            print("Admin name or password is invalid!")
            sleep(1)
    elif profile == "Q":
        clear_cmd()
        client.send("quit".encode())  # Send to server
        break
    else:
        print("Invalid value")
        sleep(1)
