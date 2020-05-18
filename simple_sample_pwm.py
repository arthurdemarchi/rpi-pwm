import pins as PIN
from RPIO import PWM


def main():
    # Set up Frequency in Hertz
    FREQUENCY = 1000
    SUBCYCLE_US = ((1/FREQUENCY)*1000000)
    CHANNEL = 0

    # Set duty_cycle 0 -> 100
    DUTY_CYCLE = 50

    # Set Pin
    PINO = PIN.CEL_A_1

    # Setup PWM and DMA channel 0
    PWM.setup()
    PWM.init_channel(channel=CHANNEL, subcycle_time_us=SUBCYCLE_US)

    # Test initialization
    if not(PWM.is_channel_initialized(CHANNEL)):
        print("ERROR: Channel could not be initialized!")
        return -1

    # Test Frequency
    if not(PWM.get_channel_subcycle_time_us(CHANNEL) == SUBCYCLE_US):
        print("ERROR: Frequency could not be setted!")
        return -1

    # Add pwm Pulse
    PWM.add_channel_pulse(dma_channel=CHANNEL, gpio=PINO,
                          start=0, width=((SUBCYCLE_US/10)*(DUTY_CYCLE/100)))

    # fake while
    print("Press any key to stop")
    input()

    # Stop PWM for specific GPIO on channel 0
    PWM.clear_channel_gpio(0, PINO)

    # Shutdown all PWM and DMA activity
    PWM.cleanup()

    return 0


if __name__ == "__main__":
    main()
