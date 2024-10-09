from nicegui import ui
from nicegui.events import ValueChangeEventArguments
from control import IRDeviceControl, extension_cable_off, extension_cable_on, ir_signal_send, light_off, light_on


all_devices = [IRDeviceControl('Пульт', 'pult.conf', 17), IRDeviceControl('Подсветка', 'svet.conf', 27)]

with ui.grid(columns=2):
    with ui.row().style('gap: 0.1rem'):
        ui.image("static/light.svg").style("height: 30px; width: 30px")
        ui.label("Свет").style('font-size: 150%; font-weight: 450; margin-top: 2px')
    with ui.button_group().style('gap: 0.2rem').props("flat"):
        ui.button('Вкл.', on_click=lambda: light_on())
        ui.button('Выкл.', on_click=lambda: light_off())

    with ui.row().style('gap: 0.1rem'):
        ui.image("static/ext_cable.svg").style("height: 30px; width: 30px; margin-top: 5px")
        ui.label("Удлинитель").style('font-size: 150%; font-weight: 450; margin-top: 2px')
    with ui.button_group().style('gap: 0.2rem').props("flat"):
        ui.button('Вкл.', on_click=lambda: extension_cable_on())
        ui.button('Выкл.', on_click=lambda: extension_cable_off())

def update_device_var(e: ValueChangeEventArguments):
    global device
    for dev in all_devices:
        if dev.name == e.value:
            device = dev
            break
    update_device_ui.refresh()

@ui.refreshable
def update_device_ui():
    device_name = selected_device.value
    if device_name == 'Пульт':
        remote_controller_ui()
    elif device_name == "Подсветка":
        backlight_ui()

def remote_controller_ui():
    with ui.grid(columns=3).style("gap: 10px 10px; padding-left: 50px"):
        ui.label()
        with ui.button(on_click=lambda: ir_signal_send(device, 'on'),
                    color='red').style('border-radius: 40px'):
            ui.image('./static/on_off.svg').classes('w-9 h-10')
        ui.label()

        ui.button(icon='volume_up', on_click=lambda: ir_signal_send(device, 'volume_up'))
        ui.label()
        ui.button(icon='keyboard_arrow_up', on_click=lambda: ir_signal_send(device, 'channel_up'))
        ui.button(icon='volume_down', on_click=lambda: ir_signal_send(device, 'volume_down'))
        ui.label()
        ui.button(icon='keyboard_arrow_down', on_click=lambda: ir_signal_send(device, 'channel_down'))
        
        ui.label()
        ui.button(icon='home', on_click=lambda: ir_signal_send(device, 'menu')
                ).style('border-radius: 40px; margin-bottom: 20px')
        ui.label()
        
        ui.label()
        ui.button(icon='arrow_upward', on_click=lambda: ir_signal_send(device, 'up'))
        ui.label()
        ui.button(icon='keyboard_arrow_left', on_click=lambda: ir_signal_send(device, 'left'))
        ui.button(icon='radio_button_checked', on_click=lambda: ir_signal_send(device, 'ok'))
        ui.button(icon='keyboard_arrow_right', on_click=lambda: ir_signal_send(device, 'right'))
        ui.button('BACK', on_click=lambda: ir_signal_send(device, 'back'))
        ui.button(icon='arrow_downward', on_click=lambda: ir_signal_send(device, 'down'))
        ui.button('EXIT', on_click=lambda: ir_signal_send(device, 'exit'))


def backlight_ui():
    with ui.grid(columns=3).style("gap: 10px 10px; padding-left: 10px"):
        ui.button('ON', on_click=lambda: ir_signal_send(device, 'on')).style('width: 98px')
        ui.label()
        ui.button('OFF', on_click=lambda: ir_signal_send(device, 'off'))

        with ui.button(on_click=lambda: ir_signal_send(device, 'up')).style('height: 50px; width: 98px'):
            ui.image('./static/bright_up.png').style('margin-top: -13px')
        ui.label()
        ui.button('Белый', on_click=lambda: ir_signal_send(device, 'white'))
        with ui.button(on_click=lambda: ir_signal_send(device, 'down')).style('height: 50px; width: 98px'):
            ui.image('./static/bright_down.png').style('margin-top: -13px')


device: IRDeviceControl = all_devices[0]
selected_device = ui.toggle(
    [device.name for device in all_devices],
    on_change=update_device_var, value=all_devices[0].name
).style("margin-left: 61.69px")
update_device_ui()

ui.run()
