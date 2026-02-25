# Thermal Logic Pi

Projeto de controle de temperatura para Raspberry Pi usando:
- Peltier (aquecimento/resfriamento)
- Heater (aquecimento auxiliar)
- Termopar MAX31856
- NTC via ADS1115

O controlador executa ciclos de temperatura, registra dados em CSV e gera grafico PNG ao final.

## Estrutura do projeto

```text
thermal-logic-pi/
├── main.py
├── requirements.txt
├── thermal_logic_pi/
│   ├── __init__.py
│   ├── controller.py
│   ├── heater.py
│   ├── peltier.py
│   ├── pin_config.py
│   ├── sensor.py
│   └── temperature_cycle.py
└── data/ (gerado automaticamente)
```

## 1. Preparar ambiente no Raspberry Pi

Recomendado usar Python 3.11+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Configurar pinos e constantes

Edite `thermal_logic_pi/pin_config.py` conforme seu hardware:
- pinos PWM/controle do heater e peltier
- pino CS do MAX31856 (`SPI_CS_PIN`)
- constantes do NTC (R0, beta, resistor serie, canal ADS1115)

## 3. Executar

Execucao com ciclos padrao:

```bash
python3 main.py
```

Execucao com parametros customizados:

```bash
python3 main.py \
  --heater-temp 37 \
  --cycle 4:60 \
  --cycle 15:120
```

Formato de `--cycle`:
- `TEMP:DURACAO`
- Exemplo: `4:60` = alvo de 4 C por 60 segundos

## 5. Saida gerada

Ao final da execucao, o sistema cria:
- `data/temp_data_YYYYMMDD_HHMMSS_xxxxxx.csv`
- `data/temp_data_YYYYMMDD_HHMMSS_xxxxxx.png`

CSV contem:
- tempo
- temperatura medida na peltier
- setpoint da peltier
- temperatura do heater (NTC)
- setpoint do heater

## Dicas de operacao

- Execute com privilegios adequados para acessar GPIO/I2C/SPI quando necessario.
- Garanta dissipacao termica e ventilacao adequadas no conjunto peltier/heater.
- Valide os sensores antes de rodar ciclos longos.
