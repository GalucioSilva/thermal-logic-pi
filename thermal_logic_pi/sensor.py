import board
import busio
import digitalio
import adafruit_max31856
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import math


class TemperatureSensor:
    def __init__(
        self,
        alpha: float,
        spi_cs_pin,
        i2c_scl,
        i2c_sda,
        ntc_channel: int,
        ntc_beta: float,
        ntc_r0: float,
        ntc_t0_k: float,
        ntc_vcc: float,
        ntc_series_resistor: float
    ):
        self.alpha = alpha

        # Termopar via SPI
        self.spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        self.cs = digitalio.DigitalInOut(spi_cs_pin)
        self.cs.direction = digitalio.Direction.OUTPUT
        self.thermocouple = adafruit_max31856.MAX31856(self.spi, self.cs)
        self.filtered_thermocouple = self.thermocouple.temperature

        # NTC via ADS1115 (I2C)
        self.i2c = busio.I2C(i2c_scl, i2c_sda)
        self.ads = ADS.ADS1115(self.i2c)
        self.ntc = AnalogIn(self.ads, getattr(ADS, f'P{ntc_channel}'))

        # Constantes da curva beta
        self.ntc_beta = ntc_beta
        self.ntc_r0 = ntc_r0
        self.ntc_t0_k = ntc_t0_k
        self.ntc_vcc = ntc_vcc
        self.ntc_series_resistor = ntc_series_resistor
        self.rx = ntc_r0 * math.exp(-ntc_beta / ntc_t0_k)

    def read_thermocouple(self):
        raw = self.thermocouple.temperature
        self.filtered_thermocouple = self.alpha * raw + (1 - self.alpha) * self.filtered_thermocouple
        return self.filtered_thermocouple

    def read_ntc(self):
        try:
            v = self.ntc.voltage
            rt = (self.ntc_vcc * self.ntc_series_resistor) / v - self.ntc_series_resistor
            t = self.ntc_beta / math.log(rt / self.rx)
            return t - 273.0  # Celsius
        except Exception as e:
            print(f"[ERRO] NTC leitura falhou: {e}")
            return None
