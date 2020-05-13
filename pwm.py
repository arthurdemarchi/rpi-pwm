import pins as PIN
import RPi.GPIO as GPIO
import time

FREQUENCY = 25

def init():
    #SET HOW TO REFER TO PINS (GPIO VS PIN)
    GPIO.setmode(GPIO.BOARD)

    #INIT PWMS
    pwmAp = init_pwm(PIN.CEL_A_1)
    pwmAn = init_pwm(PIN.CEL_A_2)
    pwmBp = init_pwm(PIN.CEL_B_1)
    pwmBn = init_pwm(PIN.CEL_B_2)
    pwmCp = init_pwm(PIN.CEL_C_1)
    pwmCn = init_pwm(PIN.CEL_C_2)
    pwmDp = init_pwm(PIN.CEL_D_1)
    pwmDn = init_pwm(PIN.CEL_D_2)
    
    ## return dictionary withh al PWM
    return {"A" : [pwmAp, pwmAn], "B" : [pwmBp, pwmBn], "C" : [pwmCp, pwmCn], "D" : [pwmDp, pwmDn]}

def init_pwm(pin):
    #SET PWM PINS AS OUTPUT
    GPIO.setup(pin, GPIO.OUT)

    #CREATE PWM INSTANCE ON SAID PINS
    pwm = GPIO.PWM(pin, FREQUENCY)
    pwm.stop()

    #RETURN REFERENCE
    return pwm

def stop(pwm):
    pwm["A"][0].stop
    pwm["A"][1].stop
    pwm["B"][0].stop
    pwm["B"][1].stop
    pwm["C"][0].stop
    pwm["C"][1].stop
    pwm["D"][0].stop
    pwm["D"][1].stop
    GPIO.cleanup()
    return
    
def heat(cell, duty_cicle):
    
    # stops negative, starts positive with correct dc
    cell[1].stop()
    cell[0].start(duty_cicle)

    # must return because out of scope pwms are auto stopped
    return cell

def cool(cell, duty_cicle):
    # stops negative, starts positive with correct dc
    cell[0].stop()
    cell[1].start(duty_cicle)

    # must return because out of scope pwms are auto stopped
    return cell

def main():
    
    pwm = init()

    while():

        cell = input("Wich cell do you want to modify?")
        if not(cell == 'A' or cell == 'B' or cell == 'C' or cell == 'D'):
            break           

        action = input("Do you want to heat(h) or cool (c) the cell?")
        if action == 'h':
            action = 0
        elif action == 'c':
            action = 1
        else:
            break

        duty_cicle = input("choose heating/coolding rate from 0 to 100")
        if duty_cicle < 0 or duty_cicle > 100:
            break

        if action == 0:
            pwm[cell] = heat(pwm[cell], duty_cicle)

        if action == 1:
            pwm[cell] = cool(pwm[cell], duty_cicle)

    stop(pwm)
    return 0