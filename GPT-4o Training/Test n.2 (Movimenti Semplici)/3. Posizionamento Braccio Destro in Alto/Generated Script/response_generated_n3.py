from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import time

def lift_right_arm(duration):
    # Posizione angolare per alzare il braccio destro
    right_arm_position = {
        reachy.r_arm.r_shoulder_pitch: -30,  # Modifica l'angolo come necessario
        reachy.r_arm.r_shoulder_roll: 0,
        reachy.r_arm.r_arm_yaw: 0,
        reachy.r_arm.r_elbow_pitch: 90,
        reachy.r_arm.r_forearm_yaw: 0,
        reachy.r_arm.r_wrist_pitch: 0,
        reachy.r_arm.r_wrist_roll: 0,
    }

    # Accensione del braccio destro
    reachy.turn_on('r_arm')

    # Movimento del braccio verso l'alto
    goto(goal_positions=right_arm_position, duration=duration, interpolation_mode=InterpolationMode.MINIMUM_JERK)

if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Alzare il braccio destro
    lift_duration = 2.0  # Durata del movimento in secondi
    lift_right_arm(lift_duration)

    # Attendere che il movimento sia completato
    time.sleep(lift_duration)

    # Spegnere il braccio destro in modo graduale
    reachy.turn_off_smoothly('r_arm')

    # Uscire dal programma
    exit()