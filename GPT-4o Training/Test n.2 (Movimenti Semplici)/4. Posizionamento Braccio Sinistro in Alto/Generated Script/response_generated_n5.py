from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import time

def lift_left_arm(duration):
    # Posizione angolare del braccio sinistro per alzarlo
    left_arm_position = {
        reachy.l_arm.l_shoulder_pitch: 45,  # Alzare la spalla
        reachy.l_arm.l_shoulder_roll: 0,    # Mantenere il braccio in linea
        reachy.l_arm.l_arm_yaw: 0,          # Mantenere il braccio dritto
        reachy.l_arm.l_elbow_pitch: -90,     # Piegare il gomito
        reachy.l_arm.l_forearm_yaw: 0,      # Mantenere il polso neutro
        reachy.l_arm.l_wrist_pitch: 0,      # Mantenere il polso neutro
        reachy.l_arm.l_wrist_roll: 0,       # Mantenere il polso neutro
    }

    # Accensione del braccio sinistro
    reachy.turn_on('l_arm')

    # Movimento del braccio verso la posizione specificata
    goto(
        goal_positions=left_arm_position,
        duration=duration,
        interpolation_mode=InterpolationMode.MINIMUM_JERK
    )

    # Spegnere il braccio sinistro in modo graduale
    reachy.turn_off_smoothly('l_arm')

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Alzare il braccio sinistro
    lift_left_arm(duration=2.0)  # Durata del movimento di alzata in secondi