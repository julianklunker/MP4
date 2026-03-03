from Robot.Combined_bot_test import Maxi
from time import time,sleep

if __name__ == "__main__":

    first_con_wait = 1
    first_con_max = 10
    
    n_test = 20
    print(f"Running the test {n_test} times.")

    start_time = time()

    while True:
        if start_time+first_con_max < time():
            print("First con took too long.")
            n_test = 0
            break
        bot = Maxi(False)
        try:
            bot.set_speed(200)
        except:
            print(f"First connection failed: Trying again in {first_con_wait} second(s).")
            sleep(1)
            continue
        print("Succesful First Connection")
        bot.closeCon()
        break

    for n in range(n_test):
        print(f"Test: {n}")
        try:
            bot = Maxi(False)
        except:
            print("Test Failed")
            break
        bot.set_speed(200)
        bot.move(z=100)
        bot.move(z=150)
        done = False
        while not done:
            done = bot.get_response()
        
        bot.closeCon()
    else:
        print("Test Done")

