from micropidash import Dashboard
import network, uasyncio as asyncio, dht, machine

# ─── WiFi Setup ───────────────────────────────────────────────────────────────
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('kritish', 'pass')
print("Connecting...")
while not wlan.isconnected(): pass
print("Connected! IP:", wlan.ifconfig()[0])

# ─── Hardware Setup ───────────────────────────────────────────────────────────
sensor  = dht.DHT11(machine.Pin(1))        # DHT11 on GP1
led_pin = machine.Pin("LED", machine.Pin.OUT) 

# ─── Dashboard Setup ──────────────────────────────────────────────────────────
dash = Dashboard("MicroPiDash v2.0")

# Graphs
dash.add_graph("temp", "Temperature (°C)", color="#FF5722")
dash.add_graph("humi", "Humidity (%)",     color="#4CAF50")

# Level bars
dash.add_level("temp_level", "Temp Level",     color="#FF5722")
dash.add_level("humi_level", "Humidity Level", color="#4CAF50")

# LED Toggle
dash.add_toggle("led", "LED")

# ─── Sensor Loop ──────────────────────────────────────────────────────────────
async def sensor_loop():
    while True:
        try:
            sensor.measure()
            t = sensor.temperature()
            h = sensor.humidity()

            dash.update_value("temp",       t)
            dash.update_value("humi",       h)
            dash.update_value("temp_level", t)
            dash.update_value("humi_level", h)

            print(f"Temp: {t}°C  |  Humidity: {h}%")
        except Exception as e:
            print("DHT11 error:", e)
        await asyncio.sleep(2)

# ─── LED Loop ─────────────────────────────────────────────────────────────────
async def led_loop():
    while True:
        led_pin.value(dash.elements["led"]["value"])  
        await asyncio.sleep_ms(100)

# ─── Main ─────────────────────────────────────────────────────────────────────
loop = asyncio.get_event_loop()
loop.create_task(sensor_loop())
loop.create_task(led_loop())
dash.run()
