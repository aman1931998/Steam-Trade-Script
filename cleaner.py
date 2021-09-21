import os

def cleaner():    
    # kill csgo processes
    os.system('taskkill /f /im csgo.exe /im steam.exe /im steamwebhelper.exe /im steamservice.exe /im steamerrorreporting.exe')
    
    # # kill steam processes
    # os.system('taskkill /f ')
    
    # # kill steamwebhelper processes
    # os.system('taskkill /f ')
    os.system('taskkill /f /im cmd.exe')
    
    #kill open cmd process
    os.system('taskkill /f /im cmd.exe')

