import numpy as np
import random

# Constants
n_courses = 5
n_sections = 5
n_professors = 5
n_days = 5
n_slots_per_day = 6
n_rooms = 10
n_theory_courses = 5
n_slots_per_morning = 4
rooms_per_floor = 5

section_names = [f"Section {i+1}" for i in range(n_sections)]
professor_names = [f"Professor {chr(65+i)}" for i in range(n_professors)]

class TimetableChromosome:
    def __init__(self):
        self.chromosome = np.zeros((n_days, n_slots_per_day, n_rooms, n_courses, n_sections), dtype=int)
        for section in range(n_sections):
            for course in range(n_courses):
                for _ in range(2):  # Each course occurs twice in a week
                    while True:
                        day = np.random.randint(n_days)  # Randomly assign a day to the section
                        slot = np.random.randint(n_slots_per_day)  # Randomly assign a slot to the section
                        room = np.random.randint(n_rooms)  # Randomly assign a room to the section
                        if np.sum(self.chromosome[day, slot, room, :, :]) == 0:  # Ensure the room is not occupied
                            self.chromosome[day][slot][room][course][section] = 1
                            break

    def decode(self):
        timetable = []
        for day in range(n_days):
            for slot in range(n_slots_per_day):
                for room in range(n_rooms):
                    for course in range(n_courses):
                        for section in range(n_sections):
                            if self.chromosome[day][slot][room][course][section] == 1:
                                professor = professor_names[course % n_professors]
                                timetable.append({
                                    'day': day,
                                    'time': slot_times[slot],
                                    'room': room,
                                    'course': course,
                                    'section': section,
                                    'professor': professor
                                })
        return timetable

def random_population(pop_size):
    return [TimetableChromosome() for _ in range(pop_size)]

def fitness(timetable):
    conflicts = 0
    # Pre-compute counts
    professor_courses_count = [[0] * n_courses for _ in range(n_professors)]
    section_courses_count = [[0] * n_sections for _ in range(n_courses)]
    lectures_days = [[set() for _ in range(n_courses)] for _ in range(n_days)]
    room_section_assigned = np.zeros((n_days, n_slots_per_day, n_rooms, n_sections))

    for day in range(n_days):
        for slot in range(n_slots_per_day):
            for room in range(n_rooms):
                for course in range(n_courses):
                    for section in range(n_sections):
                        if timetable.chromosome[day][slot][room][course][section] == 1:
                            professor_courses_count[course][section] += 1
                            section_courses_count[course][section] += 1
                            lectures_days[day][course].add(slot)
                            room_section_assigned[day][slot][room][section] += 1

    # Hard Constraints
    for day in range(n_days):
        for slot in range(n_slots_per_day):
            for professor in range(n_professors):
                lectures_assigned = []
                for course in range(n_courses):
                    for room in range(n_rooms):
                        for section in range(n_sections):
                            if timetable.chromosome[day][slot][room][course][section] == 1:
                                if professor in lectures_assigned:
                                    conflicts += 2
                                else:
                                    lectures_assigned.append(professor)

    for day in range(n_days):
        for slot in range(n_slots_per_day):
            for section in range(n_sections):
                rooms_assigned = []
                for room in range(n_rooms):
                    for course in range(n_courses):
                        if timetable.chromosome[day][slot][room][course][section] == 1:
                            if room_section_assigned[day][slot][room][section] > 1:
                                conflicts += 2
                            else:
                                room_section_assigned[day][slot][room][section] += 1

    for day in range(n_days):
        for slot in range(n_slots_per_day):
            for room in range(n_rooms):
                sections_assigned = []
                for course in range(n_courses):
                    for section in range(n_sections):
                        if timetable.chromosome[day][slot][room][course][section] == 1:
                            if room in sections_assigned:
                                conflicts += 2
                            else:
                                sections_assigned.append(room)

    for professor in range(n_professors):
        for count in professor_courses_count[professor]:
            if count > 3:
                conflicts += 2

    for course in range(n_courses):
        for section in range(n_sections):
            if section_courses_count[course][section] > 5:
                conflicts += 2

    for day in range(n_days):
        for course in range(n_courses):
            lectures_days_count = len(lectures_days[day][course])
            if lectures_days_count != 2 or (lectures_days_count == 2 and max(lectures_days[day][course]) - min(lectures_days[day][course]) <= 1):
                conflicts += 2

    for day in range(n_days):
        for course in range(n_courses):
            lab_lecture_count = 0
            for slot in range(n_slots_per_day - 1):
                for room in range(n_rooms):
                    for section in range(n_sections):
                        if timetable.chromosome[day][slot][room][course][section] == 1 and timetable.chromosome[day][slot + 1][room][course][section] == 1:
                            lab_lecture_count += 1
            if lab_lecture_count != 1:
                conflicts += 2
                
    for day in range(n_days):
        for slot in range(n_slots_per_day):
            for section in range(n_sections):
                rooms_assigned = set()
                for room in range(n_rooms):
                    for course in range(n_courses):
                        if timetable.chromosome[day][slot][room][course][section] == 1:
                            if room in rooms_assigned:
                                conflicts += 2
                            else:
                                rooms_assigned.add(room)

    # Soft Constraints
    return -conflicts


def selection(pop, scores, k=3):
    selection_ix = random.randint(0, len(pop)-1)
    for ix in random.sample(range(len(pop)), k-1):
        if scores[ix] < scores[selection_ix]:
            selection_ix = ix
    return pop[selection_ix]

def crossover(p1, p2, r_cross):
    c1, c2 = p1.chromosome.copy(), p2.chromosome.copy()
    if random.random() < r_cross:
        pt = random.randint(1, min(len(p1.chromosome), len(p2.chromosome)) - 2)
        c1[:pt] = p2.chromosome[:pt]
        c2[:pt] = p1.chromosome[:pt]
    return TimetableChromosome(), TimetableChromosome()

def mutation(chromosome, r_mut):
    for day in range(n_days):
        for slot in range(n_slots_per_day):
            for room in range(n_rooms):
                for course in range(n_courses):
                    if random.random() < r_mut:
                        chromosome[day][slot][room][course] = 1 - chromosome[day][slot][room][course]

def genetic_algorithm(n_iter, n_pop, r_cross, r_mut, early_stop_generations=10):
    pop = random_population(n_pop)
    best_solution = None
    best_fitness = float('-inf')
    no_improvement_count = 0
    for gen in range(n_iter):
        scores = [fitness(chromosome) for chromosome in pop]
        for i in range(n_pop):
            if scores[i] > best_fitness:
                best_solution = pop[i]
                best_fitness = scores[i]
                no_improvement_count = 0
                print(f"> Generation {gen}, New Best Fitness: {best_fitness}")
            else:
                no_improvement_count += 1
        if no_improvement_count >= early_stop_generations:
            print(f"Early stopping at generation {gen}")
            break
        selected = [selection(pop, scores) for _ in range(n_pop)]
        children = []
        for i in range(0, n_pop, 2):
            p1, p2 = selected[i], selected[i + 1]
            for c in crossover(p1, p2, r_cross):
                mutation(c.chromosome, r_mut)
                children.append(c)
        pop = children
    print("Best Fitness:", best_fitness)
    print("Best Timetable:")
    print_timetable(best_solution)
    return best_solution, best_fitness

def print_timetable(solution):
    timetable = solution.decode()
    #defining names
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    section_names = ['A', 'B', 'C', 'D', 'E']
    course_names = ['Programming', 'Maths', 'Physics', 'Accounting', 'English']
    section_names = [f"Section {i+1}" for i in range(n_sections)]
    professor_names = [f"Professor {chr(65+i)}" for i in range(n_professors)]
    for entry in timetable:
        day = day_names[entry['day']]
        time = entry['time']
        room = entry['room']
        course = course_names[entry['course']]
        section = section_names[entry['section']]
        professor = entry['professor']
        print(f"Day {day}, Time {time}, Room {room}, Course {course}, Section {section}, Professor {professor}")


# Example usage
slot_times = ["8:30 AM - 9:50 AM", "10:00 AM - 11:20 AM", "11:30 AM - 12:50 PM", "1:00 PM - 2:20 PM", "2:30 PM - 3:50 PM", "4:00 PM - 5:20 PM"]  # Define time slots
best_solution, best_fitness = genetic_algorithm(n_iter=100, n_pop=50, r_cross=0.9, r_mut=0.01)
