import pins as PIN
from RPIO import PWM

# Set up Frequency in Hertz
FREQUENCY = 1000

# Does using different channels amkes any difference?
MULTI_CHANNEL = False


def init(frequency=FREQUENCY, multi_channel=MULTI_CHANNEL):
    # frequency: frequency in herts
    # multi_channel: true or false

    if multi_channel:
        CHANNEL_A = 0
        CHANNEL_B = 1
        CHANNEL_C = 2
        CHANNEL_D = 3
    else:
        CHANNEL_A = 0
        CHANNEL_B = 0
        CHANNEL_C = 0
        CHANNEL_D = 0

    pwm = {"A": [PIN.CEL_A_1, PIN.CEL_A_2, CHANNEL_A, frequency], "B": [PIN.CEL_B_1, PIN.CEL_B_2, CHANNEL_B, frequency],
           "C": [PIN.CEL_C_1, PIN.CEL_C_2, CHANNEL_C, frequency], "D": [PIN.CEL_D_1, PIN.CEL_D_2, CHANNEL_D, frequency]}

    PWM.setup()
    testing = 0
    testing = testing + init_pwm(pwm['A'][2], pwm['A'][3])
    testing = testing + init_pwm(pwm['B'][2], pwm['B'][3])
    testing = testing + init_pwm(pwm['C'][2], pwm['C'][3])
    testing = testing + init_pwm(pwm['D'][2], pwm['D'][3])

    if not((testing == 4)):
        print("ERROR: Something went wrong while Initializing one or more PWMs")

    return pwm


def init_pwm(channel, frequency):
    # channel_id = 2
    # channel: pwm['A'][channel_id],  pwm['B']channel_id,  pwm['C']channel_id,  pwm['D']channel_id
    # frequency: Frequency in Hz

    subcycle = (1/frequency)*1000000

    # if not already initialized by other pwms initialize channeç
    if not(PWM.is_channel_initialized(channel)):
        PWM.init_channel(channel, subcycle)

    # Test initialization
    if not(PWM.is_channel_initialized(channel)):
        print("ERROR: Channel could not be initialized!")
        return -1

    # Test Frequency
    if not(PWM.get_channel_subcycle_time_us(channel) == subcycle):
        print("ERROR: Frequency could not be setted!")
        return -1

    return 1


def heat(cell, duty_cycle):
    # computes variables based on duty cycle
    subcycle_us = (1/cell[3])*1000000
    width = (subcycle_us/10)*(duty_cycle/100)

    # Stops the pulses on the colding side
    PWM.clear_channel_gpio(cell[2], cell[1])

    # Gerates pulses on heating side
    PWM.add_channel_pulse(cell[2], cell[0], 0, width)


def cool(cell, duty_cycle):
    # computes variables based on duty cycle
    subcycle_us = (1/cell[3])*1000000
    width = (subcycle_us/10)*(duty_cycle/100)

    # Stops the pulses on the colding side
    PWM.clear_channel_gpio(cell[2], cell[0])

    # Gerates pulses on heating side
    PWM.add_channel_pulse(cell[2], cell[1], 0, width)


def stop(pwm):
    # stops cells individually
    stop_cell(pwm['A'])
    stop_cell(pwm['B'])
    stop_cell(pwm['C'])
    stop_cell(pwm['D'])

    # Shutdown all PWM and DMA activity
    PWM.cleanup()


def stop_cell(cell):
    # Stop PWM for specific GPIO on channel
    PWM.clear_channel_gpio(cell[2], cell[0])
    PWM.clear_channel_gpio(cell[2], cell[1])


def main():

    # Init all 8 pwms and returns a dictionary that represets the 4 cells wi use.
    pwm = init()

    # fake while
    print("Press any key to start heating at 5%")
    input()

    heat(pwm['A'], 5)
    heat(pwm['B'], 5)
    heat(pwm['C'], 5)
    heat(pwm['D'], 5)

    # fake while
    print("Press any key to start cooling at 5%")
    input()

    cool(pwm['A'], 5)
    cool(pwm['B'], 5)
    cool(pwm['C'], 5)
    cool(pwm['D'], 5)

    # fake while
    print("Press any key to stop")
    input()

    # stops all cells
    stop(pwm)

    return 0


if __name__ == "__main__":
    main()
