from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import time

def lift_left_arm(duration=2.0):
    # Posizione angolare per alzare il braccio sinistro
    left_arm_position = {
        reachy.l_arm.l_shoulder_pitch: 60,  # Alza la spalla sinistra
        reachy.l_arm.l_shoulder_roll: 0,    # Mantieni la spalla dritta
        reachy.l_arm.l_arm_yaw: 0,          # Mantieni l'orientamento dritto
        reachy.l_arm.l_elbow_pitch: -30,    # Alza il gomito
        reachy.l_arm.l_forearm_yaw: 0,      # Mantieni il polso dritto
        reachy.l_arm.l_wrist_pitch: 0,      # Mantieni il polso dritto
        reachy.l_arm.l_wrist_roll: 0,       # Mantieni il polso dritto
    }

    # Accensione del braccio sinistro
    reachy.turn_on('l_arm')

    # Movimento del braccio verso la posizione specificata
    goto(goal_positions=left_arm_position, duration=duration, interpolation_mode=InterpolationMode.MINIMUM_JERK)

    # Attendere il completamento del movimento
    time.sleep(duration)

    # Spegnere il braccio sinistro in modo graduale
    reachy.turn_off_smoothly('l_arm')

if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Alzare il braccio sinistro
    lift_left_arm(duration=2.0)

    # Uscire dal programma
    exit()