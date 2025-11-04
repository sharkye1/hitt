from case_simulator.app import CaseSimulatorApp


def main() -> None:
    """Это основная точка входа, которая связывает консольный симулятор."""
    app = CaseSimulatorApp()
    app.run()


if __name__ == "__main__":
    main() 
