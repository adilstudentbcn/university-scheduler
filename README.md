# 📅 University Scheduler MVP

This project is an automated scheduling system built with **Django**. It solves the problem of organizing university modules by matching them with available teachers and classrooms while respecting specific constraints.

## Features
* **Smart Scheduling**: Automatically assigns modules to dates based on teacher availability.
* **Conflict Detection**: Identifies and reports when no teacher is free for a specific time slot.
* **Django Admin Integration**: Easily manage Teachers, Classrooms, and Modules through a UI.

## Getting Started

### 1. Setup Environment
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt