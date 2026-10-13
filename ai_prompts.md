# AI Prompt Log

**Student:** Dishan (NNM24IS078)  
**AI tool used:** Gemini (Google), chat interface  

---

## 1. Initial prompt
I uploaded the assignment PDF and asked Gemini to extract the core concurrency and submission requirements[cite: 1, 2]. I initially requested Python implementations for Readers-Writers using semaphores and Dining Philosophers using monitors, along with automated, execution-driven HTML simulation files[cite: 1, 2].

---

## 2. Important follow-up prompts
1. **Code Complexity Assessment:** Asked whether the synchronization implementations were minimal and adhere directly to standard operating system primitives[cite: 1, 2].
2. **Academic References:** Requested 3 core references formatted in strict IEEE standard covering OS theory, Python language primitives, and generative AI disclosure[cite: 4].
3. **Repository Gap Analysis:** Provided screenshots of my working folder structure to identify missing deliverables against the recommended directory layout[cite: 3, 4, 8].
4. **Implementation Completion:** Prompted for the remaining two implementations—Readers-Writers using monitors (writer-preference) and Dining Philosophers using semaphores (arbiter/room capacity)—to fulfill all four required programs[cite: 1, 4].
5. **Deadlock Rule Verification:** Verified that both Dining Philosophers solutions correctly break the Coffman deadlock conditions (Circular Wait via room capacity, and Hold-and-Wait via atomic monitor tests)[cite: 1, 2].
6. **Documentation & Deliverables Scaffolding:** Requested structured templates for `README.md`, `Assignment_Report.md`, and screenshot evidence specifications[cite: 3, 4].

---

## 3. What I changed or did myself
* Organized the repository into clean subdirectories (`readers_writers/`, `dining_philosophers/`, `generated_html/`, `ai_prompts/`, `references/`, `report/`, `screenshots/`)[cite: 3].
* Executed all four Python programs locally to verify thread synchronization, race-condition absence, and HTML file generation[cite: 2, 4].
* Verified in-browser playback (Play, Pause, Reset) and fork allocation badge updates for the HTML simulations[cite: 2].
* Took terminal execution screenshots and browser playback captures for the `screenshots/` folder[cite: 4].
* Finalized the project report, verified mathematical and deadlock invariants, and prepared viva defense explanations[cite: 4, 5].

---

## 4. Reflection: limitations and improvements I found
* **Deadlock Handling:** In the semaphore-based Dining Philosophers solution, an arbiter semaphore (`room = 3`) effectively prevents Circular Wait deadlock, while the monitor solution prevents Hold-and-Wait deadlock through atomic two-fork acquisition inside `test()`[cite: 1, 2].
* **Fairness & Starvation:** The semaphore Readers-Writers uses readers-preference where consecutive readers can starve writers[cite: 1, 5]; the monitor implementation resolves this by prioritizing waiting writers[cite: 1].
* **Simulation Replay Timing:** The current browser replay uses a fixed interval stepping mechanism; a future optimization would scale playback dynamically based on the captured timestamps to replicate real thread preemption timings[cite: 2].
