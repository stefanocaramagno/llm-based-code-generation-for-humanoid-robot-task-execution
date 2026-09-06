from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import time

# Funzione per alzare il braccio destro
def raise_right_arm(duration=2.0):
    # Posizione attuale delle giunture del braccio destro
    current_positions = {joint: reachy.r_arm.joints[joint].position for joint in reachy.r_arm.joints}

    # Creazione di un nuovo dizionario per le posizioni delle giunture
    new_positions = current_positions.copy()

    # Aumentare l'angolo della spalla per alzare il braccio
    new_positions[reachy.r_arm.r_shoulder_pitch] = current_positions[reachy.r_arm.r_shoulder_pitch] + 30  # Aumentare di 30 gradi
    new_positions[reachy.r_arm.r_elbow_pitch] = current_positions[reachy.r_arm.r_elbow_pitch] - 30  # Aumentare l'angolo dell'ellbow

    # Accensione del braccio destro
    reachy.turn_on('r_arm')

    # Movimento del braccio verso la nuova posizione
    goto(new_positions, duration=duration, interpolation_mode=InterpolationMode.MINIMUM_JERK)

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Alzare il braccio destro
    raise_right_arm(duration=2.0)

    # Attendere il completamento del movimento
    time.sleep(2.0)

    # Spegnere il braccio destro in modo graduale
    reachy.turn_off_smoothly('r_arm')

    # Uscire dal programma
    exit()