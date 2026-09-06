from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import time

# Funzione per eseguire il gesto di saluto
def wave_hand():
    # Accendere il braccio destro
    reachy.turn_on('r_arm')

    # Posizione iniziale della mano
    start_position = {
        reachy.r_arm.r_shoulder_pitch: -30,
        reachy.r_arm.r_shoulder_roll: 20,
        reachy.r_arm.r_arm_yaw: 0,
        reachy.r_arm.r_elbow_pitch: 45,
        reachy.r_arm.r_forearm_yaw: 0,
        reachy.r_arm.r_wrist_pitch: 0,
        reachy.r_arm.r_wrist_roll: 0,
    }

    # Movimenti di saluto
    wave_positions = [
        {
            reachy.r_arm.r_wrist_pitch: 30,  # Alza la mano
            reachy.r_arm.r_wrist_roll: -20,  # Ruota leggermente
        },
        {
            reachy.r_arm.r_wrist_pitch: 0,   # Torna alla posizione iniziale
            reachy.r_arm.r_wrist_roll: 0,    # Ruota di nuovo
        },
        {
            reachy.r_arm.r_wrist_pitch: 30,  # Alza di nuovo la mano
            reachy.r_arm.r_wrist_roll: 20,   # Ruota dall'altra parte
        },
        {
            reachy.r_arm.r_wrist_pitch: 0,   # Torna alla posizione iniziale
            reachy.r_arm.r_wrist_roll: 0,    # Ruota di nuovo
        },
    ]

    # Movimento alla posizione iniziale
    goto(start_position, duration=1.0)

    # Eseguire i movimenti di saluto
    for position in wave_positions:
        goto(position, duration=0.5)
        time.sleep(0.5)  # Pausa tra i movimenti

    # Spegnere il braccio destro in modo graduale
    reachy.turn_off_smoothly('r_arm')

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire il gesto di saluto
    wave_hand()

    # Uscire dal programma
    exit()