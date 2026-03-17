<h1 align="center">📅 Genetic Timetable Scheduler</h1>

<p align="center">
  <strong>Genetic algorithm that auto-generates conflict-free university timetables</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white"/>
  <img src="https://img.shields.io/badge/Genetic%20Algorithm-AI-green?style=for-the-badge"/>
</p>

---

## 📖 About

An Artificial Intelligence project that uses a **Genetic Algorithm** to automatically generate conflict-free university timetables. The algorithm evolves a population of timetable chromosomes over multiple generations, selecting and mutating solutions to satisfy all scheduling constraints.

## ✨ Features

- 🧬 Chromosome-based timetable encoding
- 🔄 Selection, crossover and mutation operators
- ✅ Constraint satisfaction — no room/professor/section conflicts
- 📈 Fitness function tracking across generations
- 🗓️ Schedules 5 courses × 5 sections across 5 days × 6 slots × 10 rooms

## 🛠️ Tech Stack

| | |
|---|---|
| Language | Python |
| Libraries | NumPy |
| Algorithm | Genetic Algorithm (Evolutionary Computation) |

## 🚀 Getting Started

```bash
git clone https://github.com/HamzaSaeed31/Genetic-Timetable-Scheduler.git
cd Genetic-Timetable-Scheduler

pip install numpy
python 21i-0671_AI-Project_D.py
```

## 📐 Algorithm Flow

```
1. Initialise random population of timetable chromosomes
2. Evaluate fitness (penalty for conflicts)
3. Select top chromosomes
4. Crossover → produce offspring
5. Mutate randomly
6. Repeat until conflict-free timetable found
```
