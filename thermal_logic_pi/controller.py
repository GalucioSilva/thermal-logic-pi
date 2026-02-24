import os
import time
import uuid
from datetime import datetime

import matplotlib.pyplot as plt

from .pin_config import (
    HEATER_PWM_PIN, HEATER_CTRL1_PIN, HEATER_CTRL2_PIN, # Heater VNH5019 pins
    PELTIER_PWM_PIN, PELTIER_CTRL1_PIN, PELTIER_CTRL2_PIN, FAN_PWM_PIN, # Peltier VNH5019 pins
    SPI_CS_PIN,
    I2C_SCL, I2C_SDA, NTC_CHANNEL, NTC_R0, NTC_BETA, NTC_T0_K, NTC_VCC, NTC_SERIES_RESISTOR, # NTC pins
    BLOW_FILTER_ALPHA, # Filter coefficient for thermocouple temperature
    NTC_NEUTRAL_ZONE # Neutral zone for NTC temperature
)

from .temperature_cycle import TemperatureCycle
from .sensor import TemperatureSensor
from .heater import HeaterController
from .peltier import PeltierController


class TemperatureController:
    def __init__(self, heat_temp: float, cycles: list[TemperatureCycle]):
        self.heat_temp = heat_temp
        self.cycles = cycles
        self.sensor = TemperatureSensor(
            alpha=BLOW_FILTER_ALPHA,
            spi_cs_pin=SPI_CS_PIN,
            i2c_scl=I2C_SCL,
            i2c_sda=I2C_SDA,
            ntc_channel=NTC_CHANNEL,
            ntc_beta=NTC_BETA,
            ntc_r0=NTC_R0,
            ntc_t0_k=NTC_T0_K,
            ntc_vcc=NTC_VCC,
            ntc_series_resistor=NTC_SERIES_RESISTOR
        )
        self.heater = HeaterController(
            HEATER_PWM_PIN, 
            HEATER_CTRL1_PIN, 
            HEATER_CTRL2_PIN
        )
        self.peltier = PeltierController(
            PELTIER_PWM_PIN, PELTIER_CTRL1_PIN, 
            PELTIER_CTRL2_PIN, FAN_PWM_PIN, NTC_NEUTRAL_ZONE
        )
        self.data = []
        self.start_time = time.time()
        self.last_filepath = None

    def _log(self, cycle_temp, heater_temp):
        now = time.time() - self.start_time
        tc_temp = self.sensor.read_thermocouple()
        ntc_temp = self.sensor.read_ntc()
        if ntc_temp is None:
            ntc_temp = float("nan")
        self.data.append((now, tc_temp, cycle_temp, ntc_temp, heater_temp))
        return tc_temp, ntc_temp

    def _run_cycle(self, duration: float, cycle_temp: float, sse: bool = True):
        message = f"[INFO] Ciclo {cycle_temp}°C por {duration}s"
        yield f"data: {message}\n\n" if sse else print(message)
        start = time.time()
        while time.time() - start <= duration:
            tc_temp, ntc_temp = self._log(cycle_temp, self.heat_temp)
            self.peltier.update(cycle_temp, tc_temp)
            self.heater.update(self.heat_temp, ntc_temp)
            message = f"Peltier={tc_temp:.2f}C / Heater={ntc_temp:.2f}C"
            yield f"data: {message}\n\n" if sse else print(message)
            time.sleep(0.5)
        message = f"[INFO] Fim do ciclo {cycle_temp}°C"
        yield f"data: {message}\n\n" if sse else print(message)

    def run(self, sse: bool = True):
        message = "[INFO] Iniciando controle térmico"
        yield f"data: {message}\n\n" if sse else print(message)
        for cycle in self.cycles:
            yield from self._run_cycle(cycle.time, cycle.temperature, sse=sse)

        self.peltier.off()
        self.heater.off()

        os.makedirs("data", exist_ok=True)
        filename = f"temp_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}.csv"
        filepath = os.path.join("data", filename)
        self.last_filepath = filepath

        with open(filepath, "w") as f:
            f.write("time,temp_peltier,target_peltier,temp_heater,target_heater\n")
            for row in self.data:
                f.write(f"{row[0]:.2f},{row[1]:.2f},{row[2]:.2f},{row[3]:.2f},{row[4]:.2f}\n")

        try:
            t, tp, sp, th, sh = zip(*self.data)
            plt.plot(t, tp, label="Peltier")
            plt.plot(t, sp, "--", label="Set Peltier")
            plt.plot(t, th, label="Heater")
            plt.plot(t, sh, "--", label="Set Heater")
            plt.xlabel("Tempo (s)")
            plt.ylabel("Temperatura (°C)")
            plt.title("Controle de Temperatura")
            plt.legend()
            plt.savefig(filepath.replace(".csv", ".png"))
            plt.close()

        except Exception as e:
            print(f"[ERRO] Falha ao gerar gráfico: {e}")

        yield f"data: [INFO] Arquivo salvo: {filepath}\n\n" if sse else print(f"[INFO] Arquivo salvo: {filepath}")
