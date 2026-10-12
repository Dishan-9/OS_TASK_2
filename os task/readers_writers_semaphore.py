import json
import os
import random
import threading
import time

# --- Synchronization Setup ---
mutex = threading.Semaphore(1)       # Protects read_count
wrt = threading.Semaphore(1)         # Mutual exclusion for writing / critical section
read_count = 0
shared_resource = "Initial Value"

# Runtime event log for HTML generation
events = []
log_lock = threading.Lock()
start_time = time.time()

def record_event(entity_type, entity_id, action, resource_val):
    timestamp = round(time.time() - start_time, 2)
    with log_lock:
        events.append({
            "time": timestamp,
            "type": entity_type,
            "id": entity_id,
            "action": action,
            "resource": resource_val
        })

def reader(reader_id, iterations=2):
    global read_count, shared_resource
    for _ in range(iterations):
        time.sleep(random.uniform(0.1, 0.4))
        record_event("Reader", reader_id, "Waiting to read", shared_resource)

        # Entry section
        mutex.acquire()
        read_count += 1
        if read_count == 1:
            wrt.acquire()  # First reader locks out writers
        mutex.release()

        # Critical Section (Reading)
        record_event("Reader", reader_id, "Reading resource", shared_resource)
        time.sleep(random.uniform(0.1, 0.3))

        # Exit section
        mutex.acquire()
        read_count -= 1
        record_event("Reader", reader_id, "Finished reading", shared_resource)
        if read_count == 0:
            wrt.release()  # Last reader frees writer access
        mutex.release()

def writer(writer_id, iterations=2):
    global shared_resource
    for i in range(iterations):
        time.sleep(random.uniform(0.2, 0.5))
        record_event("Writer", writer_id, "Waiting to write", shared_resource)

        # Entry Section
        wrt.acquire()

        # Critical Section (Writing)
        shared_resource = f"Data updated by Writer {writer_id} (rev {i+1})"
        record_event("Writer", writer_id, "Writing to resource", shared_resource)
        time.sleep(random.uniform(0.2, 0.4))

        # Exit Section
        record_event("Writer", writer_id, "Finished writing", shared_resource)
        wrt.release()

def generate_html_simulation(output_file="readers_writers_semaphore.html"):
    events_json = json.dumps(events)
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Readers-Writers (Semaphore) Simulation</title>
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
        .active {{ background: #1e3a8a; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>Readers-Writers Execution Simulation</h1>
    <div class="controls">
        <button onclick="play()">Play</button>
        <button onclick="pause()">Pause</button>
        <button onclick="reset()">Reset</button>
    </div>
    <div class="card resource-box">
        <strong>Current Shared Resource:</strong> <span id="resVal">-</span>
    </div>
    <div class="card">
        <h3>Execution Timeline</h3>
        <table>
            <thead>
                <tr><th>Time (s)</th><th>Entity</th><th>ID</th><th>Action</th><th>Resource State</th></tr>
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
            document.getElementById("resVal").innerText = row.resource;
            const tr = document.createElement("tr");
            tr.innerHTML = `<td>${{row.time}}</td><td>${{row.type}}</td><td>${{row.id}}</td><td>${{row.action}}</td><td>${{row.resource}}</td>`;
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
            if (!timer) timer = setInterval(step, 400);
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
        f.write(html_template)
    print(f"[+] Simulation HTML written to: {output_file}")

if __name__ == "__main__":
    threads = []
    # 4 Readers, 2 Writers
    for i in range(1, 5):
        threads.append(threading.Thread(target=reader, args=(i,)))
    for j in range(1, 3):
        threads.append(threading.Thread(target=writer, args=(j,)))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    generate_html_simulation()