# OS Synchronization Assignment - Readers-Writers & Dining Philosophers

**Student Name:** Dishan  
**USN:** NNM24IS078  
**Course:** Operating Systems  

---

## 1. Project Overview
This repository currently contains two standalone synchronization implementations demonstrating classical concurrency problems using native Python threads and synchronization primitives[cite: 1, 2]. Each program captures real runtime state transitions and automatically generates a self-contained, browser-viewable HTML simulation directly from the recorded event trace[cite: 1, 2].

| # | Problem | Technique | Source File | Generated HTML |
|---|---|---|---|---|
| 1 | Readers-Writers | Semaphores (`mutex`, `wrt`), Readers-preference[cite: 1] | `readers_writers_semaphore.py` | `readers_writers_semaphore.html` |
| 2 | Dining Philosophers (4) | Monitor (`Lock` + `Condition` variables)[cite: 1] | `dining_philosophers_monitor.py` | `dining_philosophers_monitor.html` |

---

## 2. Language and Environment Requirements
* **Language:** Python 3.8+
* **Dependencies:** Python Standard Library only (`threading`, `time`, `json`, `random`, `os`). No third-party packages or virtual environments required.
* **Browser:** Any modern web browser (Chrome, Edge, Firefox, Safari)[cite: 1].

---

## 3. Build / Compilation Instructions
Python is an interpreted language; no build or compilation step is required.

---

## 4. Execution & HTML Generation
Run each program directly from the repository root using the terminal or command prompt[cite: 3]:

```bash
# Readers-Writers Solutions
python readers_writers/semaphore/rw_semaphore.py
python readers_writers/monitor/rw_monitor.py

# Dining Philosophers Solutions (4 Philosophers)
python dining_philosophers/semaphore/dp_semaphore.py
python dining_philosophers/monitor/dp_monitor.py
