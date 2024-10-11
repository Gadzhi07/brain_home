from typing import NamedTuple
from json import load
import pigpio, time


class IRDeviceControl(NamedTuple):
    """Устройства, управляющиеся ИК сигналом"""
    name: str
    file_with_buttons: str
    gpio: int


all_devices = [IRDeviceControl('Пульт', 'pult.conf', 17), IRDeviceControl('Подсветка', 'svet.conf', 27)]

def extension_cable_on():
    print("ext cable enabled")


def extension_cable_off():
    print("ext cable disabled")


def light_on():
    print("light enabled")


def light_off():
    print("light disabled")


def ir_signal_send(device: IRDeviceControl, button: str):
    pi = pigpio.pi() # Connect to Pi.

    if not pi.connected:
        raise Exception('Can\' connect, try restart after: sudo pigpiod')
    try:
        with open(device.file_with_buttons, "r") as f:
            records = load(f)
    except:
        raise ValueError("Can't open: {}".format(device.file_with_buttons))

    pi.set_mode(device.gpio, pigpio.OUTPUT)
    pi.wave_add_new()

    emit_time = time.time()

    if button not in records: raise ValueError(f"{button} not finded in {device.file_with_buttons}")
    code = records[button]

    # Create wave
    marks_wid = {}
    spaces_wid = {}
    wave = [0]*len(code)

    for i in range(0, len(code)):
        ci = code[i]
        if i & 1: # Space
            if ci not in spaces_wid:
                pi.wave_add_generic([pigpio.pulse(0, 0, ci)])
                spaces_wid[ci] = pi.wave_create()
            wave[i] = spaces_wid[ci]
        else: # Mark
            if ci not in marks_wid:
                wf = carrier(device.gpio, 38.0, ci)
                pi.wave_add_generic(wf)
                marks_wid[ci] = pi.wave_create()
            wave[i] = marks_wid[ci]

    delay = emit_time - time.time()

    if delay > 0.0:
        time.sleep(delay)

    pi.wave_chain(wave)

    while pi.wave_tx_busy():
        time.sleep(0.002)

    for i in marks_wid:
        pi.wave_delete(marks_wid[i])

    for i in spaces_wid:
        pi.wave_delete(spaces_wid[i])

    pi.stop() # Disconnect from Pi.


def carrier(gpio, frequency, micros):
   """
   Generate carrier square wave.
   """
   wf = []
   cycle = 1000.0 / frequency
   cycles = int(round(micros/cycle))
   on = int(round(cycle / 2.0))
   sofar = 0
   for c in range(cycles):
      target = int(round((c+1)*cycle))
      sofar += on
      off = target - sofar
      sofar += off
      wf.append(pigpio.pulse(1<<gpio, 0, on))
      wf.append(pigpio.pulse(0, 1<<gpio, off))
   return wf

