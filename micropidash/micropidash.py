import uasyncio as asyncio
import json, gc

class Dashboard:
    def __init__(self, title="Pi IoT Lab"):
        self.title = title
        self.elements = {}

    def add_toggle(self, id, label):
        self.elements[id] = {"type": "toggle", "label": label, "value": 0}

    def add_label(self, id, label):
        self.elements[id] = {"type": "label", "label": label, "value": "---"}

    def add_level(self, id, label, color="#4CAF50"):
        self.elements[id] = {"type": "level", "label": label, "value": 0, "color": color}

    def update_value(self, id, value):
        if id in self.elements:
            self.elements[id]["value"] = value

    async def _send_html(self, writer):
        # Header + CSS
        html_start = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{self.title}</title>
        <style>
        :root {{ 
            --bg:#f4f4f4;
            --card:#fff; 
            --text:#000; 
            --primary:#4CAF50; }}
        body {{ 
                margin:0; 
                font-family:
                sans-serif; 
                background:var(--bg); 
                color:var(--text); 
                text-align:center; 
                padding:10px; }}
        .header {{ 
                display:flex; 
                justify-content:
                space-between; 
                align-items:center; 
                max-width:600px; 
                margin:0 auto 20px; }}
        .grid {{ display: grid; 
                repeat(auto-fit, minmax(160px, 1fr)); 
                gap: 15px; 
                max-width: 800px; 
                margin: 0 auto; }}
        .card {{ background:var(--card);
                padding:15px; 
                border-radius:12px; 
                box-shadow:0 3px 6px rgba(0,0,0,.1); 
                display:flex; 
                flex-direction:column; 
                align-items:center; gap:8px; }}
        .p-bg {{ width:100%; 
                height:12px; 
                background:#bbb; 
                border-radius:6px; 
                overflow:hidden; }}
        .p-fill {{ 
                height:100%; 
                transition:width .4s; }}
        .switch {{ 
                position:relative; 
                width:48px; 
                height:26px; }}
        .switch input {{ 
                opacity:0; 
                width:0; 
                height:0; }}
        .slider {{ 
                position:absolute; 
                cursor:pointer; 
                inset:0; 
                background:#ccc; 
                border-radius:26px; 
                transition:.3s; }}
        .slider:before {{ 
            content:""; 
            position:absolute; 
            height:20px; 
            width:20px; 
            left:3px; 
            bottom:3px; 
            background:#fff; 
            border-radius:50%; 
            transition:.3s; }}
        input:checked + .slider {{ background:var(--primary); }}
        input:checked + .slider:before {{ transform:translateX(22px); }}
        </style>
        <script>
        let dark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        function applyTheme() {{
            document.documentElement.style.setProperty('--bg', dark ? '#121212' : '#f4f4f4');
            document.documentElement.style.setProperty('--card', dark ? '#1e1e1e' : '#fff');
            document.documentElement.style.setProperty('--text', dark ? '#fff' : '#000');
        }}
        function updateData(){{
            fetch('/data').then(r=>r.json()).then(d=>{{
                for(let id in d){{
                    let i=d[id]; let tx=document.getElementById(id); let sw=document.getElementById(id+"-sw");
                    if(!tx)continue;
                    if(i.type==="level"){{ tx.style.width=i.value+"%"; document.getElementById(id+"-txt").innerText=i.value+"%"; }} 
                    else if(i.type==="toggle"){{ tx.innerText=i.value?"ON":"OFF"; tx.style.color=i.value? "var(--primary)":"#888"; if(sw) sw.checked=!!i.value; }} 
                    else {{ tx.innerText=i.value; }}
                }}
            }});
        }}
        setInterval(updateData, 1200);
        function sendCmd(id){{ fetch('/?'+id+'=toggle'); }}
        
        // FIXED BRACES HERE
        function toggleTheme() {{
          dark=!dark;
          applyTheme();
          document.getElementById("themeBtn").innerText = dark ? "☀️" : "🌙";
        }}

        </script></head><body onload="applyTheme()">
        <div class="header">
            <h1>{self.title}</h1>
            <button id="themeBtn" onclick="toggleTheme()" style="background:none;border:none;font-size:24px;cursor:pointer;">🌙</button>
        </div>
        <div class="grid">"""

        writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n")
        writer.write(html_start.encode())

        # Cards generation
        sorted_keys = sorted(self.elements.keys()) 

        for id in sorted_keys:
            info = self.elements[id]
            card = f"<div class='card'><strong>{info['label']}</strong>"
            if info["type"] == "level":
                card += f'<div id="{id}-txt">{info["value"]}%</div><div class="p-bg"><div id="{id}" class="p-fill" style="width:{info["value"]}%;background:{info["color"]}"></div></div>'
            elif info["type"] == "toggle":
                state = "ON" if info["value"] else "OFF"
                c = "checked" if info["value"] else ""
               
                card += f'''
                <div style="display:flex;align-items:center;gap:10px;">
                  <span id="{id}" style="font-weight:bold;color:{'var(--primary)' if info["value"] else '#888'}">
                    {state}
                  </span>
                  <label class="switch">
                    <input type="checkbox" id="{id}-sw" onchange="sendCmd('{id}')" {c}>
                    <span class="slider"></span>
                  </label>
                </div>
                '''
            else:
                card += f"<div id='{id}' style='font-size:20px;font-weight:bold;'>{info['value']}</div>"
            card += "</div>"
            writer.write(card.encode())

        writer.write(b"</div></body></html>")
        await writer.drain()

    async def _handle_request(self, reader, writer):
        try:
            raw = await reader.readline()
            if not raw: return
            req = raw.decode()
            while await reader.readline() != b'\r\n': pass

            if "/data" in req:
                body = json.dumps({k: {"type": v["type"], "value": v["value"]} for k,v in self.elements.items()})
                writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n")
                writer.write(body.encode())
            elif "toggle" in req:
                for k,v in self.elements.items():
                    if f"{k}=toggle" in req: v["value"] ^= 1
                writer.write(b"HTTP/1.1 200 OK\r\n\r\n")
            else:
                await self._send_html(writer)
            await writer.drain()
        except Exception as e:
            print("Dashboard error:", e)
        finally:
            await writer.wait_closed()
            gc.collect()

    def run(self, port=80):
        print(f"Pico Dashboard Live on Port {port}")
        loop = asyncio.get_event_loop()
        loop.create_task(asyncio.start_server(self._handle_request, "0.0.0.0", port))
        loop.run_forever()
