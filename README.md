cluster commander
=================
Cluster commander is a utility that aims to be the simplest cluster
management tool possible. It allows you to describe a cluster of machines and
then contains a script that will run in a single location and will execute
commands on your cluster.

Installation
------------
You can download the code and install it via setup.py
```
sudo python setup.py install
```

Alternatively you can download the code, don't install it at all and run the various make targets.

Commander
---------
The main component of cluster commander is the ```Commander``` daemon that
has a single configuration file and runs on a single machine. This machine
must have access to all the machines that you plan to execute commands on.

Not Another Cluster Management Tool
-----------------------------------
Everything else I've found is really complicated (Mesos, etc ...). Just
trying to figure out if I can solve the problem with good old ssh and some
interfaces.

Testing
-------
```
python -m pytest tests
```
