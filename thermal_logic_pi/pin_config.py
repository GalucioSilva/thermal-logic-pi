import board

# Heater (tampa)
HEATER_PWM_PIN = 17
HEATER_CTRL1_PIN = 27
HEATER_CTRL2_PIN = 22

# Peltier (controle térmico)
PELTIER_PWM_PIN = 13
PELTIER_CTRL1_PIN = 26
PELTIER_CTRL2_PIN = 4
FAN_PWM_PIN = 23

# SPI CS (termopar)
SPI_CS_PIN = board.D24

# I2C (ADS1115 para NTC)
I2C_SCL = board.SCL
I2C_SDA = board.SDA
NTC_CHANNEL = 0  # ADS.P0
NTC_R0 = 9940.0
NTC_BETA = 3976.0
NTC_T0_K = 273.0 + 25.0
NTC_VCC = 3.3
NTC_SERIES_RESISTOR = 47000.0

# Filtro de temperatura (termopar)
BLOW_FILTER_ALPHA = 0.18

# NTC neutral zone (temperatura de referência)
NTC_NEUTRAL_ZONE = 0.5  # Celsius
