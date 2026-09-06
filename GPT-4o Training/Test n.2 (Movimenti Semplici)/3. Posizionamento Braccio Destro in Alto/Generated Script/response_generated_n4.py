from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import time

# Funzione per sollevare il braccio destro
def lift_right_arm():
    # Posizione angolare per alzare il braccio
    lift_position = {
        reachy.r_arm.r_shoulder_pitch: -30,  # Sollevare il braccio
        reachy.r_arm.r_shoulder_roll: 0,
        reachy.r_arm.r_arm_yaw: 0,
        reachy.r_arm.r_elbow_pitch: 90,      # Posizione dell'avambraccio
        reachy.r_arm.r_forearm_yaw: 0,
        reachy.r_arm.r_wrist_pitch: 0,
        reachy.r_arm.r_wrist_roll: 0,
    }

    # Accendere il braccio destro
    reachy.turn_on('r_arm')

    # Muovere il braccio verso l'alto
    goto(
        goal_positions=lift_position,
        duration=2.0,  # Durata del movimento in secondi
        interpolation_mode=InterpolationMode.MINIMUM_JERK
    )

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Sollevare il braccio destro
    lift_right_arm()

    # Attendere un momento per vedere il movimento
    time.sleep(3)

    # Spegnere il braccio destro in modo graduale
    reachy.turn_off_smoothly('r_arm')

    # Uscire dal programma
    exit()