# Auto Solar
## Automation system for photovoltaic projects up to 75 kW
### Author: Felipe Bogaerts de Mattos

# Introduction

This system is targeted towards anyone who wishes to automate and obtain 
parameters from their small scale photovoltaic power plant. You can create 
custom PV modules and inverters, calculate PV strings, calculate how much 
your system will generate throughtout the year and more. 

# Local installation

In order to download the source code for the project, you must have git 
installed locally. After git is installed, navigate to the desired folder 
and clone the project by running the command below:

```
git clone https://github.com/felipebogaertsm/auto-solar.git
```

The execution of the program can be done through several methods. These are 
explained in the sections below.

## 1. Using Docker Compose

Docker is the recommended way to run Auto Solar locally. Dockerfiles and 
docker-compose files are made available throughout the project. 

```
docker-compose up
```