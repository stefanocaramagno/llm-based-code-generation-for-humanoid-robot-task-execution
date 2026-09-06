from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import time

# Funzione per alzare il braccio destro
def raise_right_arm(reachy, duration):
    # Accensione del braccio destro
    reachy.turn_on('r_arm')

    # Posizione angolare desiderata per alzare il braccio
    raised_position = {
        reachy.r_arm.r_shoulder_pitch: -30,  # Angolo per alzare il braccio
        reachy.r_arm.r_shoulder_roll: 0,
        reachy.r_arm.r_arm_yaw: 0,
        reachy.r_arm.r_elbow_pitch: 90,  # Posizione dell'articolazione del gomito
        reachy.r_arm.r_forearm_yaw: 0,
        reachy.r_arm.r_wrist_pitch: 0,
        reachy.r_arm.r_wrist_roll: 0,
    }

    # Muovere il braccio verso la posizione desiderata
    goto(goal_positions=raised_position, duration=duration, interpolation_mode=InterpolationMode.MINIMUM_JERK)

    # Attendere il completamento del movimento
    time.sleep(duration)

    # Spegnere il braccio destro in modo graduale
    reachy.turn_off_smoothly('r_arm')

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Alzare il braccio destro per 2 secondi
    raise_right_arm(reachy, duration=2.0)

    # Uscire dal programma
    exit()