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

# 中文版使用指南
首先需要说明的是，训练和评估智能体，不需要传入任何参数，其中的超参数由config实例定义，config实例在`main,py`内。 

## 如果修改训练和评估环境
请对`road_network_doc`中的`Metro_Intersection.rou.xml`进行修改，你可以使用现实交叉口的车辆数据。  
但是当你重新定义route文件之后请重新生成`Metro_Intersection.sumocfg`文件，因为在环境交互的过程中，我们主要依赖的是这个文件。  

## 交叉口真实数据接口
在我们这个项目中，我们是通过仿真软件实现强化学习的训练与评估的，但是如果你有实际交叉口的实时检测数据，并且想要应用到此算法中，请对`utilities`中的`demand_modeling.py`进行修改。  
遗憾的是，我们并没有为实际的观测数据预留接口，因此，很大可能，你需要自己在`Demand_Modeling`这个class下面自己编写适合你数据的method。  

## 对于`demand_modeling.py`的一点补充说明
在`demand_modeling.py`下的`Demand_Modeling`这个class中，我们定义了几个method。  
method`get_veh_id`的目的是获取每辆汽车的id；  
method`get_veh_position_type`的目的是根据先前的id获取每辆车的类型（左转、直行、右转）以及位置（方便后续的需求追述）
method`get_absolute_demand`的目的是获取交叉口进口道车辆的绝对需求；  
method`get_relative_demand`的目的是获取交叉口进口道车辆的相对需求，相对需求由blame模块决定，其主要目的是表征排队溢出现象。  

## 对于blame模块的一点解释
当车辆在交叉口之前发生排队溢出时，我们认为交叉口实际的放行需求与单纯的排队长度之间存在一定的区别，为了表征这种实际放行需求与排队长度之间的矛盾，我们引入了blame模块，其主要目的是将排队位置较后的车辆的方向需求转移至队首的一系列车辆，至于需求转移的程度，完全由系数blame决定，同时，这种需求转移的追述距离由retrospective_length决定

## 如何修改训练过程中的超参数
我们在最终的`Train_and_Evaluate`这个class中传入了`config=Config()`实例，通过修改`config`你可以更新网路训练过程中的一些参数

## 如何修改SAC的网络结构
很遗憾，我们并没有将SAC的网络结构的一系列参数（例如隐藏层的大小、全连接层的大小）归入到`config`实例中；因此，如果你想修改网络结构参数，请到`sac.py`中的`__init__(self)`内进行修改。  
例如`self.gamma = 0.99`。  


## @Author
Wolfie 2021.08.25.   
Enjoy！


