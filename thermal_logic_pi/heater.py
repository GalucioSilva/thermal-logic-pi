from gpiozero import PWMLED, LED

class HeaterController:
    def __init__(self, pwm_pin: int, ctrl1_pin: int, ctrl2_pin: int):
        self.heater = PWMLED(pwm_pin)
        self.ctrl1 = LED(ctrl1_pin)
        self.ctrl2 = LED(ctrl2_pin)
        self.neutral_zone = 0.5
        self.heater.value = 0
        self.ctrl1.off()
        self.ctrl2.off()

    def on(self):
        self.ctrl1.on()
        self.ctrl2.off()

    def off(self):
        self.ctrl1.off()
        self.ctrl2.off()
        self.heater.value = 0

    def update(self, setpoint: float, current_temp: float):
        error = setpoint - current_temp
        if abs(error) < self.neutral_zone:
            self.heater.value = 0
        elif error > 0:
            self.on()
            self.heater.value = 1
        else:
            self.off()
