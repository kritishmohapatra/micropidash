import machine, network, uasyncio as asyncio
import dht
from micropidash import Dashboard

# 1. Pin Setup
led = machine.Pin('LED', machine.Pin.OUT)
sensor = dht.DHT11(machine.Pin(28))  # GP28

# 2. WiFi Connectivity
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('YOUR_SSID', 'YOUR_PASSWORD')  
print("Connecting...")
while not wlan.isconnected(): pass
print("Server Live at IP:", wlan.ifconfig()[0])

# 3. Dashboard Configuration
dash = Dashboard("Pico Control Hub")
dash.add_toggle("1_led", "Built-in LED")
dash.add_label("2_status", "LED Status")
dash.add_label("3_temp", "Temperature (°C)")
dash.add_label("4_humidity", "Humidity (%)")
dash.add_level("5_hum_bar", "Humidity Level", "#2196F3")

# 4. Sync Task
async def sync_task():
    while True:
        # LED control
        led.value(dash.elements["1_led"]["value"])
        state = "GLOWING" if led.value() else "OFF"
        dash.update_value("2_status", f"LED is {state}")

        # DHT11 reading
        try:
            sensor.measure()
            temp = sensor.temperature()
            hum = sensor.humidity()
            dash.update_value("3_temp", f"{temp} °C")
            dash.update_value("4_humidity", f"{hum} %")
            dash.update_value("5_hum_bar", hum)
        except Exception as e:
            print("Sensor error:", e)

        await asyncio.sleep(2)  # DHT11 needs ~2s between readings

# 5. Execution
async def main():
    asyncio.create_task(sync_task())
    dash.run()

asyncio.run(main())