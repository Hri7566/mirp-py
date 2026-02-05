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

extra_keys = {}

def load_extra_keys():
    line_num = 0
    with open("./extra.mlf", "r") as f:
        for line in f:
            # key is the line number, and value is the line itself
            key = line_num
            value = line[0]
            extra_keys[key] = value
            line_num += 1

def main():
    load_keymap()
    load_extra_keys()

    print("Keymap:")
    print(keymap)

    # Detect midi input
    midi_in = rtmidi.MidiIn()
    midi_in.open_port(1)

    # Press midi message as key in keymap
    while True:
        message = midi_in.get_message()
        if message is None:
            continue

        print(message)

        status = message[0][0]
        note_index = message[0][1] - 36

        if note_index >= 0 and note_index <= 60:
            is_wide = False
            key = keymap.get(note_index)
        else:
            is_wide = True
            if note_index > 0:
                print("New index: " + str(note_index - 46))
                key = extra_keys.get(note_index - 46)
            else:
                print("New index: " + str(note_index + 15))
                key = extra_keys.get(note_index + 15)

        if status == 0xB0:
            try:
                keyboard.press("'")
                keyboard.release("'")
            except TypeError:
                continue
            except StopIteration:
                continue
            except ValueError:
                continue


        if status == 0x90:
            try:
                print("pressing " + key)
                if not key.isnumeric() and key == key.upper():
                    if is_wide == True:
                        keyboard.press('control')
                    keyboard.press('shift')
                    keyboard.press(key.lower())
                    #keyboard.release(key.lower())
                    keyboard.release('shift')
                    if is_wide == True:
                        keyboard.release('control')
                    # keyboard.press_and_release("shift+" + key.lower())
                else:
                    #print("using write")
                    #keyboard.write(key)
                    if is_wide == True:
                        keyboard.press('control')
                    keyboard.press(key.lower())
                    #keyboard.release(key.lower())
                    if is_wide == True:
                        keyboard.release('control')
            except TypeError:
                continue
            except StopIteration:
                continue
            except ValueError:
                continue

        if status == 0x80:
            try:
                print("releasing " + key)
                if not key.isnumeric() and key == key.upper():
                    if is_wide == True:
                        keyboard.press('control')
                    keyboard.press('shift')
                    #keyboard.press(key.lower())
                    keyboard.release(key.lower())
                    keyboard.release('shift')
                    if is_wide == True:
                        keyboard.release('control')
                    # keyboard.press_and_release("shift+" + key.lower())
                else:
                    #print("using write")
                    #keyboard.write(key)
                    if is_wide == True:
                        keyboard.press('control')
                    #keyboard.press(key.lower())
                    keyboard.release(key.lower())
                    if is_wide == True:
                        keyboard.release('control')
            except TypeError:
                continue
            except StopIteration:
                continue
            except ValueError:
                continue


if __name__ == "__main__":
    main()
