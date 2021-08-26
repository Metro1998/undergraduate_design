# Metro_Plan_V0
This is my undergraduate design in ZheJiang University.  
This research is about the application of reinforecement learning ,specifically soft actor and critic algorithm, in traffic signal control. 

## Env
The Env is engined by **sumo**, a software excuted in windows system, but is not encapsulated as an env which could be regared as a benchmark.  
A relative Env is defined by all xml docs in dic package `road_net_doc` and excuted in `train_and_evaluate.py`.   
I'm sorry there is no expression like **env.step()** and  __env.render()__ at present, but the packaging is on my schedule.   

## Agent
The agent is based on the **SAC**(soft actor and critic). 
The basic model is defined in `model.py` and a SAC class is in `sac.py`. 

## How to excute
I'm sorry there is no api in terminal, and if you wanna to change the hyparameters, just change the config instance which is in `main.py`.  
Just excute `main.py`, and the instance trainer_and_evaluater will train and evaluate automately.  
 
## Result
The comparison is so complicated that I just upload one pic to demonstrate the performance of the algorithm.  
It's the result when the blame = 0.6.  
![image](https://user-images.githubusercontent.com/51565689/130783094-bac2858c-8eb7-4f18-bc41-08c2df452097.png)

## To Do List  
* Env pakaging.  
* hybrid action space.  
* model of state space. 

## @Author
Wolfie 2021.08.25. 


