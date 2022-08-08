from codecs import escape_encode
from datetime import datetime
import pickle

def create_shadow_marker(markers):
    marker = {}
    sub_markers = ['start_shadow', 'end_shadow']
    for sub_marker in sub_markers:
        print(f"Press key for '{sub_marker}'")
        input()  # just wait for any keypress
        marker[sub_marker] = datetime.now()
    markers.append(marker)
    print(f"Shadow maker {len(markers)} was created!\n---")


def write_file(markers):
    ts_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    with open("test_data/" + f"markers_{ts_str}.pkl", 'wb') as f:
        pickle.dump(markers, f)

if __name__ == "__main__":
    markers = []
    while True:
        try:
            create_shadow_marker(markers)
        except KeyboardInterrupt:
            write_file(markers)
            exit()
    