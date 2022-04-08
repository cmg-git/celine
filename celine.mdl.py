#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 15:29:26 2022

@author: cghiaus

An example of cloze questions obtained wth Pyton
"""

# 1. Import modules
import numpy as np
import MdlClz


# 2. Create a function which solves the problem

def problem_fun(x):
    """
    Vapor humidification.

    Function solving the problem
    x : dict
        inputs: data for the quiz
    Returns
    y : dict
        outputs: embedded answers in the quiz
    """
    ρ, d, w = [x[k] for k in ['ρ', 'd', 'w']]

    m = ρ * w * np.pi / 4 * d**2 / 1000000

    y = {'m': m}                      # kg/s, mass flow
    return y


# 3. Define the input space
x_ranges = {
    'ρ': np.array([887, 1000]),         # kg/m**3, density
    'd': np.array([156, 40]),           # mm, diameter
    'w': np.array([1.5, 2])}             # m/s, velocity


# 4. Write the text of the cloze question in Markdown
text = """
**Notes :**

A fluid of density ρ {ρ} kg/m3 flows in a pipe with diameter d = {d} mm.
The average velocity in the pipe is {w} m/s.

Calculate the mass flow in the pipe
{{1:NUMERICAL:={m:.1f}:5}} kg/s.
"""

# 5. Generate the quiz in Moodle - cloze format and save .xml file
question_name = "celine"      # It will be followed by question number
quiz = MdlClz.generate_quiz(question_name, problem_fun, x_ranges, text)

# 6. Show the inputs and outputs of all questions
test_nr = 0
for x in MdlClz.cprod(x_ranges):
    print("Test: ", test_nr)
    print("Inputs:")
    print(x)
    print("Outputs:")
    print(problem_fun(x), "\n")
    test_nr += 1
