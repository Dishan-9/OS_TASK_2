import json
import random
import threading
import time

class ReadersWritersMonitor:
    def __init__(self, logger_fn):
        self.lock = threading.Lock()
        self.read_ok = threading.Condition(self.lock)
        self.write_ok = threading.Condition(self.lock)
        
        self.active_readers = 0
        self.waiting_readers = 0
        self.active_writers = 0
        self.waiting_writers = 0
        self.logger = logger_fn

    def start_read(self, reader_id):
        with self.lock:
            self.waiting_readers += 1
            self.logger("Reader", reader_id, "Waiting to read", f"Active readers: {self.active_readers}")
            # Readers wait if a writer is active or if writers are waiting (writer preference)
            while self.active_writers > 0 or self.waiting_writers > 0:
                self.read_ok.wait()
            self.waiting_readers -= 1
            self.active_readers += 1
            self.logger("Reader", reader_id, "Reading resource", f"Active readers: {self.active_readers}")

    def end_read(self, reader_id):
        with self.lock:
            self.active_readers -= 1
            self.logger("Reader", reader_id, "Finished reading", f"Active readers: {self.active_readers}")
            if self.active_readers == 0:
                self.write_ok.notify()  # Awaken waiting writer

    def start_write(self, writer_id):
        with self.lock:
            self.waiting_writers += 1
            self.logger("Writer", writer_id, "Waiting to write", f"Writers waiting: {self.waiting_writers}")
            # Writer waits if another writer is writing or any readers are reading
            while self.active_writers > 0 or self.active_readers > 0:
                self.write_ok.wait()
            self.waiting_writers -= 1
            self.active_writers = 1
            self.logger("Writer", writer_id, "Writing to resource", "Exclusive lock held")

    def end_write(self, writer_id):
        with self.lock:
            self.active_writers = 0
            self.logger("Writer", writer_id, "Finished writing", "Lock released")
            # If writers are waiting, awaken one writer; otherwise awaken all waiting readers
            if self.waiting_writers > 0:
                self.write_ok.notify()
            else:
                self.read_ok.notify_all()

# --- Event Logging for HTML Generation ---
events = []
log_lock = threading.Lock()
start_time = time.time()
shared_data = "Initial State"

def record_event(entity_type, entity_id, action, status_detail):
    timestamp = round(time.time() - start_time, 2)
    with log_lock:
        events.append({
            "time": timestamp,
            "type": entity_type,
            "id": entity_id,
            "action": action,
            "detail": status_detail,
            "data": shared_data
        })

def reader(reader_id, monitor, iterations=2):
    for _ in range(iterations):
        time.sleep(random.uniform(0.1, 0.3))
        monitor.start_read(reader_id)
        # Critical Section (Reading)
        time.sleep(random.uniform(0.1, 0.2))
        monitor.end_read(reader_id)

def writer(writer_id, monitor, iterations=2):
    global shared_data
    for i in range(iterations):
        time.sleep(random.uniform(0.2, 0.4))
        monitor.start_write(writer_id)
        # Critical Section (Writing)
        shared_data = f"Updated by Writer {writer_id} (rev {i+1})"
        time.sleep(random.uniform(0.1, 0.3))
        monitor.end_write(writer_id)

def generate_html_simulation(output_file="readers_writers_monitor.html"):
    events_json = json.dumps(events)
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Readers-Writers (Monitor) Simulation</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 20px; }}
        h1 {{ text-align: center; color: #38bdf8; }}
        .controls {{ display: flex; justify-content: center; gap: 10px; margin-bottom: 20px; }}
        button {{ padding: 8px 16px; background: #38bdf8; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; color: #0f172a; }}
        button:hover {{ background: #0284c7; }}
        .card {{ background: #1e293b; border-radius: 8px; padding: 15px; margin-bottom: 15px; border: 1px solid #334155; }}
        .resource-box {{ font-size: 1.2rem; color: #a7f3d0; text-align: center; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        th, td {{ border: 1px solid #334155; padding: 8px; text-align: left; font-size: 0.9rem; }}
        th {{ background: #334155; }}
    </style>
</head>
<body>
    <h1>Readers-Writers (Monitor-Based) Simulation</h1>
    <div class="controls">
        <button onclick="play()">Play</button>
        <button onclick="pause()">Pause</button>
        <button onclick="reset()">Reset</button>
    </div>
    <div class="card resource-box">
        <strong>Shared Data Value:</strong> <span id="resVal">-</span>
    </div>
    <div class="card">
        <h3>Execution Timeline</h3>
        <table>
            <thead>
                <tr><th>Time (s)</th><th>Entity</th><th>ID</th><th>Action</th><th>Synchronization State</th><th>Resource Data</th></tr>
            </thead>
            <tbody id="logBody"></tbody>
        </table>
    </div>

    <script>
        const events = {events_json};
        let currentIndex = 0;
        let timer = null;

        function renderRow(idx) {{
            const row = events[idx];
            document.getElementById("resVal").innerText = row.data;
            const tr = document.createElement("tr");
            tr.innerHTML = `<td>${{row.time}}</td><td>${{row.type}}</td><td>${{row.id}}</td><td>${{row.action}}</td><td>${{row.detail}}</td><td>${{row.data}}</td>`;
            document.getElementById("logBody").prepend(tr);
        }}

        function step() {{
            if (currentIndex < events.length) {{
                renderRow(currentIndex);
                currentIndex++;
            }} else {{
                clearInterval(timer);
                timer = null;
            }}
        }}

        function play() {{
            if (!timer) timer = setInterval(step, 350);
        }}

        function pause() {{
            clearInterval(timer);
            timer = null;
        }}

        function reset() {{
            pause();
            currentIndex = 0;
            document.getElementById("logBody").innerHTML = "";
            document.getElementById("resVal").innerText = "-";
        }}
        play();
    </script>
</body>
</html>"""
    with open(output_file, "w") as f:
        f.write(html_content)
    print(f"[+] Simulation HTML written to: {output_file}")

if __name__ == "__main__":
    mon = ReadersWritersMonitor(record_event)
    threads = []
    for r in range(1, 5):
        threads.append(threading.Thread(target=reader, args=(r, mon)))
    for w in range(1, 3):
        threads.append(threading.Thread(target=writer, args=(w, mon)))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    generate_html_simulation()