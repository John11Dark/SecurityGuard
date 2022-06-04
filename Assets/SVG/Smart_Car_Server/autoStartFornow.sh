#!/bin/sh
# wait 10 seconds to make sure that they system has loaded 
sleep 10
# go to directory where the file is located 
cd "/home/JohnMuller/Documents/Smart_Car_Server/"
# list working directory 
pwd
# wait 5 seconds to make sure that the system reaches the distancion 
sleep 5
# run the server sudo is not reqired becasue i gave the file permission 
#to run by using chmod 777 /app.py and also for the bash script autoStart  
sudo python app.py 
