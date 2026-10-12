# AI Prompt Log

**Student:** Dishan (NNM24IS078)  
**AI tool used:** Gemini (Google), chat interface  

---

## 1. Initial prompt
I uploaded the assignment PDF and asked Gemini to identify the core code requirements. I then asked for Python implementations of the synchronization problems (Readers-Writers using semaphores and Dining Philosophers using monitors) along with the program-generated HTML simulation files based on execution logs[cite: 1, 2].

---

## 2. Important follow-up prompts
1. **Code Complexity Check:** Asked whether the generated synchronization code was too complicated or if it appropriately followed standard operating system concepts[cite: 1, 2].
2. **References Request:** Asked for 2 to 3 formal references for the written report in strict IEEE citation format, covering textbooks, Python documentation, and AI usage[cite: 4].
3. **Repository Audit:** Provided screenshots of my workspace directory and asked what required files and folders were missing according to the assignment checklist[cite: 3, 4, 8].
4. **Deliverables Generation:** Asked for complete templates for `ai_prompts/prompts.md`, the `report/` draft, and guidance on what screenshots to include in `screenshots/`[cite: 3, 4].
5. **Code Alignment Verification:** Asked to verify whether the recorded prompt log accurately reflected the synchronization primitives and methods used in the actual Python scripts[cite: 1, 2].

---

## 3. What I changed or did myself
* Created the project directory structure and separated files according to the assignment requirements[cite: 3].
* Ran the Python scripts locally using the terminal to verify thread execution and ensure that `.html` simulation files were generated cleanly[cite: 2, 4].
* Captured screenshots of the terminal runs and browser simulation interfaces for the `screenshots/` directory[cite: 4].
* Formatted the final report, added my own student details, and prepared the viva explanation points[cite: 3, 4, 5].

---

## 4. Reflection: limitations and improvements I found
* **Visualization Timing:** The simulation replay currently steps through events using a fixed interval rather than true proportional time gaps; scaling the playback delay using the recorded event timestamps would make it more realistic[cite: 2].
* **Writer Starvation:** The Readers-Writers semaphore implementation follows reader-preference, meaning continuous reader arrivals can starve writers[cite: 1, 5]. A fairer queue or monitor-based writer-preference approach can prevent this[cite: 1, 5].
* **Dining Philosophers Deadlock:** Without proper state testing or asymmetric fork acquisition, four philosophers simultaneously taking their left fork will deadlock[cite: 1, 5]. The monitor implementation resolves this by checking both neighbors' states before granting access[cite: 1, 5].
