---
title: "Step motor control using Raspberry Pi and Raspberry Pico" 
date: 2025-01-01
tags: ["step motors","raspberry pico","raspberry","micropython"]
author: ["Dilly Émilien, Radisson Basile "]
description: " Python code for step motor control with combo Raspberry Pi and Pico to avoid motor stuttering. " 
summary: "Python code for step motor control with combo Raspberry Pi and Pico to avoid motor stuttering.   " 
cover:
    image: "paper1.webp"
    alt: "helix with perversion generated from PyPerv"
    relative: true
editPost:

---


**Title:** Raspberry Pi Pico Stepper Motor Controller  
**Description:**  Python utilities to generate and send MicroPython code to a Raspberry Pi Pico for controlling stepper motors. Supports one, two, or three motors with configurable direction, steps, and delays.  

### Why Raspberry Pi Pico instead of Raspberry Pi only?

Initially, I tried controlling the stepper motors directly from the Raspberry Pi 4.  
However, when using short `time.sleep` (few ms) intervals, the motors started to **stutter and miss steps** due to CPU scheduling delays and background processes on the Pi. I even attempted to increase the process priority, but the problem persisted.  

To solve this, I offloaded the real-time motor control to the **Raspberry Pi Pico**, which runs MicroPython and can generate **stable, low-latency pulses** without OS interruptions.  
The Raspberry Pi 4 now acts as a high-level controller, while the Pico ensures smooth and reliable motor motion.


**Key Features:**  
- Works directly from Raspberry Pi 4  
- Auto-generates and executes Pico scripts  
- Supports single and synchronized multi-motor movement  
---

## 📂 Files

- `pico_motor_control.py` → Main Python utility for generating and sending scripts
- `FULL_DOCUMENTATION.md` → Complete documentation (this file)

---

## 🐍 Python Code (`pico_motor_control.py`)

```python
#!/usr/bin/env python3
"""
Raspberry Pi Pico Stepper Motor Controller
------------------------------------------
This script generates MicroPython code for the Pico, enabling control of
one, two, or three stepper motors. It transfers scripts using `mpremote`.

Author: Emilien Dilly
"""

import os


def create_python_file_for_micropython_one_motor(
    namefile,
    namefilepy,
    direction=0,
    nbr_of_steps=0,
    delay_on=0,
    delay_steps=0,
    whichmotor=0,
    pinpul=0,
    pindir=0,
):
    """Generate a MicroPython script for one stepper motor."""
    with open(namefile, "w") as f:

        def add_line(s):
            f.write(s + "\n")

        add_line("print('Pico script received')")
        add_line("from machine import Pin")
        add_line("import time")
        add_line(f"dirPin = Pin({pindir}, Pin.OUT)")
        add_line(f"pul = Pin({pinpul}, Pin.OUT)")
        add_line(f"dirPin.value({direction})")
        add_line(f"for k in range({nbr_of_steps}):")
        add_line("    pul.value(1)")
        add_line(f"    time.sleep({delay_on})")
        add_line("    pul.value(0)")
        add_line(f"    time.sleep({delay_steps})")

    os.system(f"mv {namefile} {namefilepy}")
    print("Pico Script Successfully written")


def move_one_motor(
    direction=0,
    nbr_of_steps=0,
    delay_on=0,
    delay_steps=0,
    whichmotor=0,
    pinpul=0,
    pindir=0,
):
    """Send one-motor control script to the Pico."""
    namefile = f"pico_code_motor_{whichmotor}.txt"
    namefilepy = f" pico_code_motor_{whichmotor}.py"
    create_python_file_for_micropython_one_motor(
        namefile,
        namefilepy,
        direction=direction,
        nbr_of_steps=nbr_of_steps,
        delay_on=delay_on,
        delay_steps=delay_steps,
        whichmotor=whichmotor,
        pinpul=pinpul,
        pindir=pindir,
    )
    print("Sending Pico Script To Pico")
    cmd = f"mpremote run {namefilepy}"
    try:
        os.system(cmd)
    except Exception:
        print("Error sending script. Ensure Pico is connected and not opened in Thonny.")


def create_python_file_for_micropython_two_motors(namefile, namefilepy, direction1 , direction2 ,nbr_of_steps1 ,nbr_of_steps2 ,delay_on ,delay_steps , pinpul1 , pindir1 , pinpul2 , pindir2 ):
    ### ecrire le .txt
    #print('Writing Pico Script..')
    f = open(namefile, "w") #create the txt file to be compiled
    
    # defines a function to add a line on the txt file. 
    def add_line(stringtoadd, txtfile):
        txtfile.write(stringtoadd + "\n")
        return 1
    add_line("print('Pico script received') \nfrom machine import Pin \nimport time ", f)
    add_line('dirPin = Pin('+str(pindir1)+', Pin.OUT) ', f) ## sets pins
    add_line('pul = Pin('+str(pinpul1)+', Pin.OUT) ', f)
    add_line('dirPin2 = Pin('+str(pindir2)+', Pin.OUT) ', f) ## sets pins
    add_line('pul2 = Pin('+str(pinpul2)+', Pin.OUT) ', f)
    add_line('dirPin.value('+str(direction1)+')' , f) ## sets direction
    add_line('dirPin2.value('+str(direction2)+')' , f) ## sets direction
    add_line('if '+str(nbr_of_steps1)+'>'+str(nbr_of_steps2)+':' , f)  ## for loop for rotation 
    add_line('  for k in range('+str(nbr_of_steps1)+'):' , f)  ## for loop for rotation 
    add_line('      if k <'+str(nbr_of_steps2)+':' , f)  ## for loop for rotation 
    add_line('          pul.value(1)' , f)  ## for loop for rotation 
    add_line('          pul2.value(1)' , f)  ## for loop for rotation 
    add_line('          time.sleep('+str(delay_on)+')' , f)  ## for loop for rotation 
    add_line('          pul.value(0)' , f)  ## for loop for rotation 
    add_line('          pul2.value(0)' , f)  ## for loop for rotation 
    add_line('          time.sleep('+str(delay_steps)+')' , f)  ## for loop for rotation 
    add_line('      else:' , f)  ## for loop for rotation 
    add_line('          pul.value(1)' , f)  ## for loop for rotation 
    add_line('          time.sleep('+str(delay_on)+')' , f)  ## for loop for rotation 
    add_line('          pul.value(0)' , f)  ## for loop for rotation 
    add_line('          time.sleep('+str(delay_steps)+')' , f)  ## for loop for rotation
    add_line('else:' , f)  ## for loop for rotation 
    add_line('  for k in range('+str(nbr_of_steps2)+'):' , f)  ## for loop for rotation 
    add_line('      if k <'+str(nbr_of_steps1)+':' , f)  ## for loop for rotation 
    add_line('          pul.value(1)' , f)  ## for loop for rotation 
    add_line('          pul2.value(1)' , f)  ## for loop for rotation 
    add_line('          time.sleep('+str(delay_on)+')' , f)  ## for loop for rotation 
    add_line('          pul.value(0)' , f)  ## for loop for rotation 
    add_line('          pul2.value(0)' , f)  ## for loop for rotation 
    add_line('          time.sleep('+str(delay_steps)+')' , f)  ## for loop for rotation 
    add_line('      else:' , f)  ## for loop for rotation 
    add_line('          pul2.value(1)' , f)  ## for loop for rotation 
    add_line('          time.sleep('+str(delay_on)+')' , f)  ## for loop for rotation 
    add_line('          pul2.value(0)' , f)  ## for loop for rotation 
    add_line('          time.sleep('+str(delay_steps)+')' , f)  ## for loop for rotation 
    cmd = "mv "+namefile + namefilepy
    os.system(cmd)
    print('Pico Script Successfully writen')




def move_two_motors(direction1 , direction2 ,nbr_of_steps1 ,nbr_of_steps2 ,delay_on ,delay_steps , pinpul1 , pindir1 , pinpul2 , pindir2 , whichmotor ='both_motor'):
    namefile = "pico_code_motor_"+whichmotor+".txt"
    namefilepy = " pico_code_motor_"+whichmotor+".py"
    create_python_file_for_micropython_two_motors(namefile, namefilepy, direction1 =direction1, direction2 =direction2 ,nbr_of_steps1 =nbr_of_steps1,nbr_of_steps2 =nbr_of_steps2,delay_on =delay_on ,delay_steps =delay_steps , pinpul1 =pinpul1, pindir1 =pindir1 , pinpul2 =pinpul2, pindir2 =pindir2 )
    print('Sending Pico Script To Pico')
    cmd = 'mpremote run ' +namefilepy
    try:
        os.system(cmd)
        #print('Pico Script Sent')
    except:
        print('There was en error sending the script, please ensure pico is connected and not opened in thony')     









def create_python_file_for_micropython_three_motors(namefile, namefilepy, direction ,nbr_of_steps1 ,nbr_of_steps2 ,delay_on ,delay_steps , pinpul1 , pindir1 , pinpul2 , pindir2, pinpultrans, dirpintrans ):
    ### ecrire le .txt
    #print('Writing Pico Script..')
    f = open(namefile, "w") #create the txt file to be compiled
    
    # defines a function to add a line on the txt file. 
    def add_line(stringtoadd, txtfile):
        txtfile.write(stringtoadd + "\n")
        return 1
    if direction == 0:
        dir2 = 1
    else:
        dir2 = 0
    add_line("print('Pico script received') \nfrom machine import Pin \nimport time ", f)
    add_line('dirPin = Pin('+str(pindir1)+', Pin.OUT) ', f) ## sets pins
    add_line('pul = Pin('+str(pinpul1)+', Pin.OUT) ', f)
    add_line('dirPin2 = Pin('+str(pindir2)+', Pin.OUT) ', f) ## sets pins
    add_line('pul2 = Pin('+str(pinpul2)+', Pin.OUT) ', f)
    add_line('pultrans = Pin('+str(pinpultrans)+', Pin.OUT) ', f)
    add_line('dirpintrans = Pin('+str(dirpintrans)+', Pin.OUT) ', f)
    add_line('dirPin.value('+str(direction)+')' , f) ## sets direction
    add_line('dirPin2.value('+str(dir2)+')' , f) ## sets direction
    add_line('dirpintrans.value('+str(direction)+')' , f) ## sets direction

    add_line('if '+str(nbr_of_steps1)+'>'+str(nbr_of_steps2)+':' , f)  ## for loop for rotation 
    add_line('  for k in range('+str(nbr_of_steps1)+'):' , f)  ## for loop for rotation 
    add_line('      if k <'+str(nbr_of_steps2)+':' , f)  ## for loop for rotation 
    add_line('          pul.value(1)' , f)  ## for loop for rotation 
    add_line('          pul2.value(1)' , f)  ## for loop for rotation 
    add_line('          pultrans.value(1)' , f)  ## for loop for rotation 
    add_line('          time.sleep('+str(delay_on)+')' , f)  ## for loop for rotation 
    add_line('          pul.value(0)' , f)  ## for loop for rotation 
    add_line('          pul2.value(0)' , f)  ## for loop for rotation 
    add_line('          pultrans.value(0)' , f)  ## for loop for rotation 
    add_line('          time.sleep('+str(delay_steps)+')' , f)  ## for loop for rotation 
    add_line('      else:' , f)  ## for loop for rotation 
    add_line('          pul.value(1)' , f)  ## for loop for rotation 
    add_line('          pul2.value(1)' , f)  ## for loop for rotation 
    add_line('          time.sleep('+str(delay_on)+')' , f)  ## for loop for rotation 
    add_line('          pul.value(0)' , f)  ## for loop for rotation 
    add_line('          pul2.value(0)' , f)  ## for loop for rotation 
    add_line('          time.sleep('+str(delay_steps)+')' , f)  ## for loop for rotation 
    add_line('else:' , f)  ## for loop for rotation 
    add_line('  for k in range('+str(nbr_of_steps2)+'):' , f)  ## for loop for rotation 
    add_line('      if k <'+str(nbr_of_steps1)+':' , f)  ## for loop for rotation 
    add_line('          pul.value(1)' , f)  ## for loop for rotation 
    add_line('          pul2.value(1)' , f)  ## for loop for rotation 
    add_line('          pultrans.value(1)' , f)  ## for loop for rotation 
    add_line('          time.sleep('+str(delay_on)+')' , f)  ## for loop for rotation 
    add_line('          pul.value(0)' , f)  ## for loop for rotation 
    add_line('          pul2.value(0)' , f)  ## for loop for rotation 
    add_line('          pultrans.value(0)' , f)  ## for loop for rotation 
    add_line('          time.sleep('+str(delay_steps)+')' , f)  ## for loop for rotation 
    add_line('      else:' , f)  ## for loop for rotation 
    add_line('          pultrans.value(1)' , f)  ## for loop for rotation 
    add_line('          time.sleep('+str(delay_on)+')' , f)  ## for loop for rotation 
    add_line('          pultrans.value(0)' , f)  ## for loop for rotation 
    add_line('          time.sleep('+str(delay_steps)+')' , f)  ## for loop for rotation 
    cmd = "mv "+namefile + namefilepy
    os.system(cmd)
    print('Pico Script Successfully writen')


def move_three_motors(direction,nbr_of_steps1 ,nbr_of_steps2 ,delay_on ,delay_steps , pinpul1 , pindir1 , pinpul2 , pindir2 , pinpultrans , dirpintrans):
    namefile = "pico_code_motor_3.txt"
    namefilepy = " pico_code_motor_3.py"
    create_python_file_for_micropython_three_motors(namefile, namefilepy, direction =direction, nbr_of_steps1 =nbr_of_steps1,nbr_of_steps2 =nbr_of_steps2,delay_on =delay_on ,delay_steps =delay_steps , pinpul1 =pinpul1, pindir1 =pindir1 , pinpul2 =pinpul2, pindir2 =pindir2 , pinpultrans =pinpultrans, dirpintrans = dirpintrans )
    print('Sending Pico Script To Pico')
    cmd = 'mpremote run ' +namefilepy
    try:
        os.system(cmd)
        #print('Pico Script Sent')
    except:
        print('There was en error sending the script, please ensure pico is connected and not opened in thony')     




```

---

## 🚀 Features
- Control **one, two, or three stepper motors**
- Dynamically generate MicroPython scripts
- Transfer scripts automatically with `mpremote`
- Set direction, steps, and timing delays
- Flexible pin configuration

---

## 📦 Requirements

```bash
sudo apt-get install mpremote
```

Python dependencies (already included in standard library):  
- `os`

---

## Pin Explanation

Each stepper motor driver requires **two GPIO pins** from the Pico:

- **PUL (Pulse):** Generates the step signals to move the motor.
- **DIR (Direction):** Sets the rotation direction (0 = clockwise, 1 = counter-clockwise).

For three motors:

- Motor 1 and Motor 2 move together but in **opposite directions**.
- Transmission Motor (Motor 3) moves with Motor 1.

---

## ⚙️ Usage

### One Motor Example
```python
from pico_motor_control import move_one_motor

# Move one motor forward 200 steps
move_one_motor(
    direction=1,
    nbr_of_steps=200,
    delay_on=0.001,
    delay_steps=0.001,
    whichmotor=1,
    pinpul=15,
    pindir=14,
)
```

### Two Motors Example
```python
from pico_motor_control import move_two_motors

move_two_motors(
    direction1=1, direction2=0,
    nbr_of_steps1=200, nbr_of_steps2=150,
    delay_on=0.001, delay_steps=0.001,
    pinpul1=15, pindir1=14,
    pinpul2=17, pindir2=16
)
```

### Three Motors Example
```python
from pico_motor_control import move_three_motors

move_three_motors(
    direction=1,
    nbr_of_steps1=200, nbr_of_steps2=200,
    delay_on=0.001, delay_steps=0.001,
    pinpul1=15, pindir1=14,
    pinpul2=17, pindir2=16,
    pinpultrans=19, dirpintrans=18
)
```

---

## 📊 Example Output
```
Pico Script Successfully written
Sending Pico Script To Pico
Pico script received
```

---

## 📌 Notes
- Ensure your Raspberry Pi Pico is connected via USB and not in use by Thonny IDE.  
- Pin numbers correspond to Pico GPIO pins.  
- Timing parameters (`delay_on`, `delay_steps`) control motor speed and smoothness.  

---

## 🛠️ Future Improvements
- Add acceleration profiles (ramp-up / ramp-down)
- Provide CSV logging of motor commands
- Implement error handling for disconnected Pico

---

*This page -except the code - was automatically generated by ChatGPT*

