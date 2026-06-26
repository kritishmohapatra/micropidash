import machine, network, uasyncio as asyncio
from micropidash import Dashboard

# 1. ShrikeFi Pin Setup (use GPIO 21 for built-in LED)
led = machine.Pin(21, machine.Pin.OUT)

# 2. WiFi Connectivity
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('ssid', 'pass')

print("Connecting...")
while not wlan.isconnected(): pass
print("Server Live at IP:", wlan.ifconfig()[0])

# 3. Dashboard Configuration
dash = Dashboard("Shrike Fi Control Hub")
dash.add_toggle("1_led", "Built-in LED")
dash.add_label("2_status", "Live Status")

# 4. Hardware & Web UI Sync Task
async def sync_task():
    while True:
        
        led.value(dash.elements["1_led"]["value"])
        
    
        state = "GLOWING" if led.value() else "OFF"
        dash.update_value("2_status", f"LED is {state}")
        
        await asyncio.sleep(0.5)

# 5. Execution
async def main():
    asyncio.create_task(sync_task())
    dash.run()

asyncio.run(main())
