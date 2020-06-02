# Ceng 435 Term Project 1
```python
#Simge Nur Çankaya 2099554
#Muhammed Süha Demirel 2098911

```
In this project we first calculate the RTT between 5 nodes. After that we are finding the shortest path using Dijkstra Algorithm.

## Installation
Send each script to its respected node via scp.

r1.py -> r1

r2.py -> r2

r3.py, expr0.sh, expr1.sh, expr2.sh, expr3.sh -> r3

s.py , expS.sh -> s

d.py , expD.sh -> d


## How to Find RTT

To calculate the RTT's run files in the following order.

in s node: 
```bash
python s.py
```
in d node: 
```bash
python d.py
```
in r2 node: 
```bash
python r2.py
```
in r1 node: 
```bash
python r1.py
```
in r3 node: 
```bash
python r3.py
```

The RTT txt files are automatically created.

## Experiment
For the experiment part first make each expr*.sh executable.

For resetting the delay:
```bash
chmod +x exp0.sh
```
For 20ms+-5ms delay:
```bash
chmod +x exp1.sh
```
For 40ms+-5ms delay:
```bash
chmod +x exp2.sh
```
For 50ms+-5ms delay:
```bash
chmod +x exp3.sh
```

### Start experiment 1: 
```bash
./exp1.sh
```
To calculate the end-to-end delay between the S-R3-D run files in the following order.

In node d:
```bash
python expD.py
```
In node r3: 
```bash
python expr3.py
```
in node s: 
```bash
python expS.py
```
This calculates the delay, and writes the start, end and difference to the which file is uncommented in the s node, expS.py file.
```
#f = open("expConf0.txt","a")
f = open("expConf1.txt","a")
#f = open("expConf2.txt","a")
#f = open("expConf3.txt","a")
```

For experiments 2 and 3 please follow the steps above by changing exp1 to exp2 and exp3 accordingly.