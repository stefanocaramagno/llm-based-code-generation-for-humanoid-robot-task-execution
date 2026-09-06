from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import time
import numpy as np

# Funzione per muovere il braccio in un movimento di saluto
def wave_hand(reachy, duration=1.0, repetitions=3):
    # Accensione del braccio destro
    reachy.turn_on('r_arm')

    # Posizioni per il gesto di saluto
    start_position = {
        reachy.r_arm.r_shoulder_pitch: -30,
        reachy.r_arm.r_shoulder_roll: 0,
        reachy.r_arm.r_arm_yaw: 0,
        reachy.r_arm.r_elbow_pitch: 45,
        reachy.r_arm.r_forearm_yaw: 0,
        reachy.r_arm.r_wrist_pitch: 0,
        reachy.r_arm.r_wrist_roll: 0,
    }

    # Posizione di saluto (braccio alzato)
    wave_position = {
        reachy.r_arm.r_shoulder_pitch: -10,
        reachy.r_arm.r_shoulder_roll: 0,
        reachy.r_arm.r_arm_yaw: 0,
        reachy.r_arm.r_elbow_pitch: 90,
        reachy.r_arm.r_forearm_yaw: 0,
        reachy.r_arm.r_wrist_pitch: 20,
        reachy.r_arm.r_wrist_roll: 0,
    }

    # Muovere il braccio nella posizione di partenza
    goto(start_position, duration=1.0)

    for _ in range(repetitions):
        # Muovere il braccio verso la posizione di saluto
        goto(wave_position, duration=0.5)
        time.sleep(0.5)
        # Tornare alla posizione di partenza
        goto(start_position, duration=0.5)
        time.sleep(0.5)

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire il gesto di saluto
    wave_hand(reachy)