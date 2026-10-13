# OS Synchronization Assignment - Readers-Writers & Dining Philosophers

**Student Name:** Dishan  
**USN:** NNM24IS078  
**Course:** Operating Systems  

---

## 1. Project Overview
This repository contains all four standalone synchronization implementations demonstrating classical concurrency problems using native Python threads and synchronization primitives[cite: 1, 2]. Each program captures runtime state transitions and automatically generates a self-contained, browser-viewable HTML simulation directly from the recorded event trace[cite: 1, 2].

| # | Problem | Technique | Source File | Generated HTML |
|---|---|---|---|---|
| 1 | Readers-Writers | Semaphores (`mutex`, `wrt`), Readers-preference[cite: 1] | `readers_writers_semaphore.py` | `readers_writers_semaphore.html` |
| 2 | Readers-Writers | Monitor (`Lock` + `Condition` variables), Writer-preference[cite: 1] | `readers_writers_monitor.py` | `readers_writers_monitor.html` |
| 3 | Dining Philosophers (4) | Semaphores (Arbiter room semaphore = 3)[cite: 1] | `dining_philosophers_semaphore.py` | `dining_philosophers_semaphore.html` |
| 4 | Dining Philosophers (4) | Monitor (`Lock` + 4 Condition queues, atomic check)[cite: 1] | `dining_philosophers_monitor.py` | `dining_philosophers_monitor.html` |

---

## 2. Language and Environment Requirements
- **Language:** Python 3.8+[cite: 2]
- **Dependencies:** Python Standard Library only (`threading`, `time`, `json`, `random`)[cite: 2]. No third-party packages or virtual environments required.
- **Browser:** Any modern web browser (Chrome, Edge, Firefox, Safari)[cite: 1].

---

## 3. Build / Compilation Instructions
Python is an interpreted language; no compilation or build step is required[cite: 2].

---

## 4. Execution & HTML Generation
Run each program directly from the command prompt or terminal using Python[cite: 2]:

```bash
# Readers-Writers Solutions
python readers_writers_semaphore.py
python readers_writers_monitor.py

# Dining Philosophers Solutions (4 Philosophers)
python dining_philosophers_semaphore.py
python dining_philosophers_monitor.py
