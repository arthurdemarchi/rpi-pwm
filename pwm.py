import pins as PIN
import RPi.GPIO as GPIO
import time

FREQUENCY = 25

def init():
    # SET HOW TO REFER TO PINS (GPIO VS PIN)
    GPIO.setmode(GPIO.BOARD)

    # INIT PWMS
    pwmAp = init_pwm(PIN.CEL_A_1)
    pwmAn = init_pwm(PIN.CEL_A_2)
    pwmBp = init_pwm(PIN.CEL_B_1)
    pwmBn = init_pwm(PIN.CEL_B_2)
    pwmCp = init_pwm(PIN.CEL_C_1)
    pwmCn = init_pwm(PIN.CEL_C_2)
    pwmDp = init_pwm(PIN.CEL_D_1)
    pwmDn = init_pwm(PIN.CEL_D_2)
    
    # RETURN DICTIONARY WITH ALL PWMS INSTNCES
    return {"A" : [pwmAp, pwmAn], "B" : [pwmBp, pwmBn], "C" : [pwmCp, pwmCn], "D" : [pwmDp, pwmDn]}

def init_pwm(pin):
    # SET PWM PIN AS OUTPUT
    GPIO.setup(pin, GPIO.OUT)

    # CREATE PWM INSTANCE ON SAID PIN
    pwm = GPIO.PWM(pin, FREQUENCY)
    pwm.stop()

    # RETURN INSTANCE
    return pwm

def stop(pwm):
    # STOP ALL PWM INSTANCES
    pwm["A"][0].stop
    pwm["A"][1].stop
    pwm["B"][0].stop
    pwm["B"][1].stop
    pwm["C"][0].stop
    pwm["C"][1].stop
    pwm["D"][0].stop
    pwm["D"][1].stop
    # CLEAN GPIOS
    GPIO.cleanup()
    return
    
def heat(cell, duty_cicle):
    
    # STOP NEGATIVE PWM AND STARTS POSITIVE WITH CORRECT DC
    cell[1].stop()
    cell[0].start(duty_cicle)

    # INSTANCE MUST BE RETURN BECAUSE OUT OF SCOPE INSTANCES ARE STOPPED
    return cell

def cool(cell, duty_cicle):
    #  STOP POSITIVE PWM AND STARTS NEGATIVE WITH CORRECT DC
    cell[0].stop()
    cell[1].start(duty_cicle)

    # INSTANCE MUST BE RETURN BECAUSE OUT OF SCOPE INSTANCES ARE STOPPED
    return cell

def main():
    
    pwm = init()

    # CHANGES DUTY CICLE AND CELL PWM AS YOU WISH
    while():

        #cell = input("Wich cell do you want to modify?")
        cell = 'A'
        if not(cell == 'A' or cell == 'B' or cell == 'C' or cell == 'D'):
            break           

        #action = input("Do you want to heat(h) or cool (c) the cell?")
        action = 'h'
        if action == 'h':
            action = 0
        elif action == 'c':
            action = 1
        else:
            break

        #duty_cicle = input("choose heating/coolding rate from 0 to 100")
        duty_cicle = 10

        if duty_cicle < 0 or duty_cicle > 100:
            break

        if action == 0:
            pwm[cell] = heat(pwm[cell], duty_cicle)

        if action == 1:
            pwm[cell] = cool(pwm[cell], duty_cicle)

        slee(1)

    stop(pwm)
    return 0