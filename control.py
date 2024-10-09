from typing import NamedTuple


class IRDeviceControl(NamedTuple):
    """a docstring"""
    name: str
    file_with_buttons: str
    gpio: int


def extension_cable_on():
    print("ext cable enabled")


def extension_cable_off():
    print("ext cable disabled")


def light_on():
    print("light enabled")


def light_off():
    print("light disabled")


def ir_signal_send(device: IRDeviceControl, button: str):
    print(f"{device} {button=}")

