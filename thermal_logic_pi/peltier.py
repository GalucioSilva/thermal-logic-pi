from gpiozero import PWMLED, LED

class PeltierController:
    def __init__(self, pwm_pin: int, ctrl1_pin: int, ctrl2_pin: int, fan_pin: int, neutral_zone: float):
        self.peltier = PWMLED(pwm_pin)
        self.ctrl1 = LED(ctrl1_pin)
        self.ctrl2 = LED(ctrl2_pin)
        self.fan = PWMLED(fan_pin)
        self.neutral_zone = neutral_zone
        self.peltier.value = 0
        self.fan.value = 0
        self.ctrl1.off()
        self.ctrl2.off()

    def heat(self):
        self.ctrl1.off()
        self.ctrl2.on()

    def cool(self):
        self.ctrl1.on()
        self.ctrl2.off()

    def off(self):
        self.peltier.value = 0
        self.fan.value = 0

    def update(self, setpoint: float, current_temp: float):
        error = setpoint - current_temp
        if abs(error) < self.neutral_zone:
            self.peltier.value = 0
            self.fan.value = 0
        elif error > 0:
            self.heat()
            self.peltier.value = 1
            self.fan.value = 1
        else:
            self.cool()
            self.peltier.value = 1
            self.fan.value = 0
