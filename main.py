import argparse

from thermal_logic_pi import TemperatureController, TemperatureCycle


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Controle de temperatura para Raspberry Pi (Peltier + Heater)."
    )
    parser.add_argument(
        "--heater-temp",
        type=float,
        default=37.0,
        help="Setpoint do heater em Celsius (padrao: 37.0)",
    )
    parser.add_argument(
        "--cycle",
        action="append",
        default=[],
        metavar="TEMP:DURACAO",
        help="Ciclo da peltier no formato temp:segundos. Ex: --cycle 4:30",
    )
    parser.add_argument(
        "--sse",
        action="store_true",
        help="Emite mensagens no formato Server-Sent Events.",
    )
    return parser


def parse_cycles(raw_cycles: list[str]) -> list[TemperatureCycle]:
    if not raw_cycles:
        return [
            TemperatureCycle(temperature=4.0, time=20.0),
            TemperatureCycle(temperature=15.0, time=20.0),
        ]

    cycles: list[TemperatureCycle] = []
    for raw in raw_cycles:
        try:
            temp, duration = raw.split(":", 1)
            cycles.append(TemperatureCycle(temperature=float(temp), time=float(duration)))
        except ValueError as exc:
            raise ValueError(
                f"Ciclo invalido '{raw}'. Use o formato TEMP:DURACAO, por exemplo 4:30."
            ) from exc
    return cycles


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    controller = TemperatureController(
        heat_temp=args.heater_temp,
        cycles=parse_cycles(args.cycle),
    )

    for _ in controller.run(sse=args.sse):
        pass


if __name__ == "__main__":
    main()
