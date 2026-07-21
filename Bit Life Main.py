'''
So this is my very first simple rough layout of the game Bit Life which I am trying to make in python, 
I will imporve upon as much as possible to get as close as possible to the real game.
This basically the3 foundation/base of the code to show the ideas of what the game will do, how it will work,
what are the attribute, variable, of course these will not stay constant throughout the version further coming versions of this program,
as I will update and improve, all aspect of the program as much as I can, to bring it as close as possible to the real game,
I will add things such as the use of the library tkinter, I will use classes, I will also incorperate file handling, 
I will probably use other libraries like random, and if I can I will try to the JSON library.
Please note that this a very rough version as it it is the first version, so it has no validation or way to end the game instantly
'''


import random

# This is just stating all the basic variables needed for the base version of Bit Life 
name = input("Enter your name: ")
age = 0
health = 100
happiness = 100
money = 0

# Just a welcome Statement for the user after they enter the prefered name 
print(f"\nWelcome, {name}!")

# Simple health above 0 condition to make the following can only be done when the character's health is above 0
while health > 0:
# So what this while block does is, as long as the chracter is alive it will run the life simulation which the game,
#  and after the run through of the code in this ehile loop the players age will go up by one 
    age += 1
    print(f"\n===== Age {age} =====")

    # So as soon as the game starts it will print 1 of the 3 following events to give you context,
    # and make the user feel that they are the charcater, by giving them something to relate to 
    event = random.randint(1, 3)

    if event == 1:
        print("You caught a cold.")
        health -= 10

    elif event == 2:
        print("You found $100.")
        money += 100

    else:
        print("You had a great birthday!")
        happiness += 10

    # This is the main choice for the first version to which is to ask the user to do one of the 4 options below 
    print("\nChoose an action:")
    print("1. Study")
    print("2. Work")
    print("3. Exercise")
    print("4. Relax")

    choice = input("[1-4]: ")
    # And consequently once the user has chose one of the 4 option it will go through the if blocks below to carry out the stat change
    if choice == "1":
        print("You studied.")
        happiness -= 5

    elif choice == "2":
        print("You worked.")
        money += 500
        happiness -= 10

    elif choice == "3":
        print("You exercised.")
        health = min(100, health + 10)

    elif choice == "4":
        print("You relaxed.")
        happiness = min(100, happiness + 10)

    else:
        print("You did nothing.")

    # This is just to prvent the stats from going over 100 just for simplicties sake, and to keep some order in the game 
    health = min(100, health)
    happiness = min(100, happiness)

    # This is just to show all your stats and how they were affected by the actions the user has done
    print("\nStats:")
    print(f"Age: {age}")
    print(f"Health: {health}")
    print(f"Happiness: {happiness}")
    print(f"Money: ${money}")

# Printing the enging of the user's character but most probably they wont or atleast it will take a while 
print(f"\n{name} died at age {age}.")
print(f"Final Money: ${money}")