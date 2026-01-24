from micropidash import Dashboard
import network 

# 1. WiFi Setup
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

wlan.connect('YOUR_SSID', 'YOUR_PASSWORD')

print("Connecting...")
while not wlan.isconnected(): pass
print("Connected! IP:", wlan.ifconfig()[0])

# 2. Dashboard Initialization
dash = Dashboard("MicroPiDash v1.0")

# 3. Adding Basic Widgets
dash.add_toggle("led", "Test Switch")      # A binary toggle
dash.add_label("status", "System Status")  # A text display
dash.add_level("level", "Signal Strength") # A progress bar (0-100)

# 4. Start the Web Server
# Access the dashboard via the IP address printed above
dash.run()