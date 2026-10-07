# PrintBai — Student Printing Service Web Application

A complete, modern, student-friendly printing service business website built for a **Business + Event-Driven Programming** school project.

![PrintBai](https://img.shields.io/badge/Project-PrintBai-blue?style=for-the-badge)
![Tech-PyScript](https://img.shields.io/badge/Technology-PyScript%20%7C%20Python-yellow?style=for-the-badge)
![Tech-Frontend](https://img.shields.io/badge/Frontend-HTML5%20%2F%20CSS3-green?style=for-the-badge)

---

## 📌 Project Overview

**PrintBai** is a small printing service business model designed specifically for college and senior high school students in the Philippines. It solves long printing shop queues, irregular pricing, and rushed campus printing needs with an easy-to-use digital portal.

- **Tagline**: *"Print It. Get It. Done."*
- **Positioning**: Fast, Affordable, Student-Friendly Printing
- **Target Audience**: College and Senior High School students preparing research papers, reports, assignments, visual aids, and school project materials.

---

## 💻 Tech Stack & Architecture

This project strictly emphasizes **Event-Driven Programming with PyScript (Python)**:

* **HTML5**: Clean semantic layout with 10 structured sections.
* **CSS3**: Custom responsive stylesheet with student-inspired branding, responsive CSS grid/flexbox, modern typography (Poppins & Inter), and rounded card components.
* **PyScript / Pyodide**: Executes standard Python in the client web browser via WebAssembly.
* **Event-Driven Handlers**: All interactive behavior is implemented in `main.py` using PyScript's `@when` event decorators. No hidden JavaScript business logic.

---

## ⚙️ Event-Driven Programming in PrintBai

Here is how Event-Driven Programming is applied throughout the application:

| Feature / UI Component | Event Triggered | Python Function in `main.py` | Event Action & Behavior |
| :--- | :--- | :--- | :--- |
| **Service Cards ("Choose Service")** | `click` | `on_choose_bw()`, `on_choose_color()`, etc. | Selects service type, synchronizes calculator & order form, and smoothly scrolls into view. |
| **Printing Calculator** | `input`, `change` | `on_calc_input()` | **Live reactive price preview**: Updates estimated cost in real-time as pages, copies, or print types change. |
| **Calculate Total Button** | `click` | `on_calculate_click()` | Computes complete itemized cost breakdown and populates receipt details. |
| **Order Form Submission** | `submit` | `on_order_submit()` | Intercepts submission, runs **pure Python validations**, renders inline error warnings or a generated demo receipt. |

---

## 📂 Project Directory Structure

```text
D:\PrintBai\
│
├── index.html        # Complete single-page layout & PyScript markup
├── main.py           # Core Python logic, event handlers & validation
├── style.css         # Modern, responsive design system & component styles
├── README.md         # Project documentation and presentation guide
├── .gitignore        # Standard git ignore definitions
└── assets/
    ├── images/       # Brand graphics and visuals
    └── icons/        # SVG icon assets
```

---

## 🚀 How to Run the Project Locally

Because modern web browsers enforce security policies (CORS) on WebAssembly and modules loaded over `file://`, run a lightweight local HTTP server:

### Option 1: Using Python Launcher (Recommended)
Open Command Prompt or PowerShell in `D:\PrintBai` and run:

```bash
# Navigate to D:\PrintBai
d:
cd D:\PrintBai

# Start local server on port 8000
py -m http.server 8000
```

Then open your browser and navigate to:
```
http://localhost:8000
```

### Option 2: Using Node.js / npx
```bash
npx serve .
```

---

## 🎓 Guide for Video Presentation / Project Defense

When recording your video or defending your project in front of your instructor, highlight these key aspects:

1. **Demonstrate PyScript in Action**:
   - Point out the top indicator banner showing **Python 3 Runtime Active**.
   - Show that open Developer Tools (F12 > Console) display PyScript engine outputs rather than typical JavaScript frameworks.
2. **Demonstrate Event-Driven Programming**:
   - **Click Event**: Click on *"Colored Printing"* in the Services section and demonstrate how it immediately activates the colored radio option in the calculator.
   - **Input / Change Event**: Type numbers into the *"Number of Pages"* and *"Number of Copies"* fields. Show how the **Live Reactive Preview** (`₱XX.XX`) recalculates dynamically without pressing any submit button.
   - **Form Submit Event with Python Validation**: Attempt to submit the order form with empty or invalid fields (e.g., negative page numbers or invalid email format). Point out how the inline error alerts are driven by Python regular expressions and logic in `main.py`.
3. **Business Viability**:
   - Explain the student pricing model (₱2.00 B&W, ₱5.00 Colored) and how the 4-step workflow (*Submit &rarr; Choose &rarr; We Print &rarr; Pick Up*) fits the real daily routine of students.

---

## 📄 License & Academic Note
Created for academic demonstration in Business and Event-Driven Programming coursework.
Order submission is simulated for demonstration purposes.
