def classify_column(col: str) -> str:
    c = col.upper()

    sensor_keys = [
        "TEMP","PRESS","FLOW","LEVEL","HUM","PH",
        "VOLT","CURR","FREQ","LOAD","LIT","AIT","FIT","PIT"
    ]

    actuator_keys = [
        "PUMP","VALVE","FAN","MOTOR","MV","ACT",
        "COOL","HEAT"
    ]

    if any(k in c for k in sensor_keys):
        return "SENSOR"

    if any(k in c for k in actuator_keys):
        return "ACTUATOR"

    return "CONTROL"
