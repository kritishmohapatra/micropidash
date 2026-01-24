### 🔌 ESP32 Onboard LED Example

import machine, network, uasyncio as asyncio
from micropidash import Dashboard

# 1. ESP32 Pin Setup (Most boards use GPIO 2 for built-in LED)
led = machine.Pin(2, machine.Pin.OUT)

# 2. WiFi Connectivity
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('YOUR_SSID', 'YOUR_PASSWORD')

print("Connecting...")
while not wlan.isconnected(): pass
print("Server Live at IP:", wlan.ifconfig()[0])

# 3. Dashboard Configuration
dash = Dashboard("ESP32 Control Hub")
dash.add_toggle("1_led", "Built-in LED")
dash.add_label("2_status", "Live Status")

# 4. Hardware & Web UI Sync Task
async def sync_task():
    while True:
        # Dashboard UI state ko physical LED se link karna
        led.value(dash.elements["1_led"]["value"])
        
        # Dashboard par status update bhejni
        state = "GLOWING" if led.value() else "OFF"
        dash.update_value("2_status", f"LED is {state}")
        
        await asyncio.sleep(0.5)

# 5. Execution
async def main():
    asyncio.create_task(sync_task())
    dash.run()

asyncio.run(main())