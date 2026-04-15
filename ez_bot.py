from Robot.Combined_bot_test import Maxi


def connect():
    port = input("Which COM-port? ")
    port = port.upper()
    bot = Maxi(f"{port}")
    print("Done. Now u can write bot.move(x=0,y=0,z=150)")
    return bot
