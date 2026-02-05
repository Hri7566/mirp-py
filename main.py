import rtmidi
import keyboard

keymap = {}

def load_keymap():
    # open keymap file (./default.mlf) and read each line
    line_num = 0
    with open("./default.mlf", "r") as f:
        for line in f:
            # key is the line number, and value is the line itself
            key = line_num
            value = line[0]
            keymap[key] = value
            line_num += 1

def main():
    load_keymap()

    print("Keymap:")
    print(keymap)

    # Detect midi input
    midi_in = rtmidi.RtMidiIn()
    midi_in.openPort(1)

    # Press midi message as key in keymap
    while True:
        message = midi_in.getMessage()
        if message is None:
            continue
        
        print(message.isNoteOn())
        note_index = message.getNoteNumber() - 36
        print(note_index)

        key = keymap.get(note_index)

        if message.isNoteOn():
            try:
                print("pressing " + key)
                if not key.isnumeric() and key == key.upper():
                    print("using press/release")
                    keyboard.press('shift')
                    keyboard.press(key.lower())
                    keyboard.release(key.lower())
                    keyboard.release('shift')
                    # keyboard.press_and_release("shift+" + key.lower())
                else:
                    print("using write")
                    keyboard.write(key)
            except TypeError:
                continue
            except StopIteration:
                continue
            except ValueError:
                continue
            


if __name__ == "__main__":
    main()
