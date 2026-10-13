import json
import random
import threading
import time

NUM_PHILOSOPHERS = 4

# Semaphores
forks = [threading.Semaphore(1) for _ in range(NUM_PHILOSOPHERS)]
room = threading.Semaphore(NUM_PHILOSOPHERS - 1)  # Room capacity = 3 to prevent deadlock

# Runtime logs
events = []
log_lock = threading.Lock()
start_time = time.time()
fork_holders = [-1] * NUM_PHILOSOPHERS  # Tracks which philosopher holds each fork

def record_event(phil_id, state, action_msg):
    timestamp = round(time.time() - start_time, 2)
    with log_lock:
        events.append({
            "time": timestamp,
            "philosopher": phil_id,
            "state": state,
            "action": action_msg,
            "forks": list(fork_holders)
        })

def philosopher(phil_id, rounds=3):
    left_fork = phil_id
    right_fork = (phil_id + 1) % NUM_PHILOSOPHERS

    for _ in range(rounds):
        # Thinking
        record_event(phil_id, "THINKING", "Thinking...")
        time.sleep(random.uniform(0.1, 0.3))

        # Hungry / Requesting Entry to Dining Room
        record_event(phil_id, "HUNGRY", "Waiting for room admission")
        room.acquire()

        # Acquiring Forks
        forks[left_fork].acquire()
        fork_holders[left_fork] = phil_id
        record_event(phil_id, "WAITING", f"Acquired left fork {left_fork}")

        forks[right_fork].acquire()
        fork_holders[right_fork] = phil_id
        record_event(phil_id, "EATING", f"Acquired right fork {right_fork}. Eating...")

        # Critical Section (Eating)
        time.sleep(random.uniform(0.2, 0.4))

        # Releasing Forks
        fork_holders[right_fork] = -1
        forks[right_fork].release()

        fork_holders[left_fork] = -1
        forks[left_fork].release()

        room.release()
        record_event(phil_id, "THINKING", f"Released forks {left_fork} & {right_fork}")

def generate_html_simulation(output_file="dining_philosophers_semaphore.html"):
    events_json = json.dumps(events)
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dining Philosophers (Semaphore) Simulation</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0b132b; color: #fff; padding: 20px; }}
        h1 {{ text-align: center; color: #48cae4; }}
        .controls {{ display: flex; justify-content: center; gap: 10px; margin-bottom: 20px; }}
        button {{ padding: 8px 16px; background: #48cae4; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; color: #0b132b; }}
        .table-view {{ display: flex; justify-content: space-around; margin: 20px 0; }}
        .phil-card {{ background: #1c2541; padding: 15px; border-radius: 8px; width: 180px; text-align: center; border: 2px solid #3a506b; }}
        .state-THINKING {{ border-color: #6c757d; color: #ced4da; }}
        .state-HUNGRY, .state-WAITING {{ border-color: #ffb703; color: #ffb703; }}
        .state-EATING {{ border-color: #52b788; color: #52b788; font-weight: bold; }}
        .fork-panel {{ background: #1c2541; border: 1px solid #3a506b; border-radius: 8px; padding: 10px; text-align: center; margin-bottom: 20px; }}
        .fork-badge {{ display: inline-block; margin: 0 10px; padding: 5px 10px; border-radius: 4px; background: #3a506b; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        th, td {{ border: 1px solid #3a506b; padding: 8px; text-align: left; }}
        th {{ background: #1c2541; }}
    </style>
</head>
<body>
    <h1>Dining Philosophers (4 Philosophers - Semaphore)</h1>
    <div class="controls">
        <button onclick="play()">Play</button>
        <button onclick="pause()">Pause</button>
        <button onclick="reset()">Reset</button>
    </div>

    <div class="fork-panel">
        <strong>Forks Status:</strong>
        <span id="f0" class="fork-badge">Fork 0: Free</span>
        <span id="f1" class="fork-badge">Fork 1: Free</span>
        <span id="f2" class="fork-badge">Fork 2: Free</span>
        <span id="f3" class="fork-badge">Fork 3: Free</span>
    </div>

    <div class="table-view">
        <div id="p0" class="phil-card state-THINKING"><h3>P0</h3><div class="status">THINKING</div></div>
        <div id="p1" class="phil-card state-THINKING"><h3>P1</h3><div class="status">THINKING</div></div>
        <div id="p2" class="phil-card state-THINKING"><h3>P2</h3><div class="status">THINKING</div></div>
        <div id="p3" class="phil-card state-THINKING"><h3>P3</h3><div class="status">THINKING</div></div>
    </div>

    <table>
        <thead>
            <tr><th>Time (s)</th><th>Philosopher</th><th>State</th><th>Action Details</th></tr>
        </thead>
        <tbody id="logBody"></tbody>
    </table>

    <script>
        const events = {events_json};
        let currentIndex = 0;
        let timer = null;

        function updateUI(ev) {{
            const card = document.getElementById("p" + ev.philosopher);
            card.className = "phil-card state-" + ev.state;
            card.querySelector(".status").innerText = ev.state;

            for (let f = 0; f < 4; f++) {{
                const badge = document.getElementById("f" + f);
                const holder = ev.forks[f];
                if (holder === -1) {{
                    badge.innerText = `Fork ${{f}}: Free`;
                    badge.style.background = "#3a506b";
                }} else {{
                    badge.innerText = `Fork ${{f}}: Held by P${{holder}}`;
                    badge.style.background = "#d90429";
                }}
            }}
        }}

        function step() {{
            if (currentIndex < events.length) {{
                const ev = events[currentIndex];
                updateUI(ev);
                const tr = document.createElement("tr");
                tr.innerHTML = `<td>${{ev.time}}</td><td>P${{ev.philosopher}}</td><td>${{ev.state}}</td><td>${{ev.action}}</td>`;
                document.getElementById("logBody").prepend(tr);
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
            for (let i = 0; i < 4; i++) {{
                const card = document.getElementById("p" + i);
                card.className = "phil-card state-THINKING";
                card.querySelector(".status").innerText = "THINKING";
                document.getElementById("f" + i).innerText = `Fork ${{i}}: Free`;
                document.getElementById("f" + i).style.background = "#3a506b";
            }}
        }}

        play();
    </script>
</body>
</html>"""
    with open(output_file, "w") as f:
        f.write(html_content)
    print(f"[+] Simulation HTML written to: {output_file}")

if __name__ == "__main__":
    threads = []
    for i in range(NUM_PHILOSOPHERS):
        t = threading.Thread(target=philosopher, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    generate_html_simulation()