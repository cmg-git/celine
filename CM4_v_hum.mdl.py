#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 10:34:54 2022

@author: cghiaus

Oulet conditions of vapor humidification

Given the inlet temperature & humidity and the mass flow rate of vapor,
find the temperature and the humidity of the oulet air in dry cooling

Nomenclature:
    θ, Temperatures: °C
    w, Humidity ration: kg_vapor / kg_dry_air
    φ, Relative humidity: 0 ≤ φ ≤ 1
    q, Heat flow rate: W
    m, Mass flow rate: kg/s

Model:
    ==o=>[VH]==0==>
      m   /    m
          l

Points on the psychrometric chart (θ, w):
    o) out      inlet air
    0) 0        cooled air

Inputs:
    m       mass flow rate [kg/s]
    θo, φo  inlet temperature [°C] & humidity ratio [%]
    Ql      latent load of the vapor humidifier [kW]

Elements (2 equations) [Fig. 2 in Ghiaus (2022)]:
    VH      vapor humidifier (2 equations)

Outputs:
    θ0, w0  outlet temperature & humidity ratio

Equations:
    system
    m * c * θ0 = m * c * θo         # [VH]
    m * l * w0 = m * l * wo + QlVH

    unknowns
    x = [θ0, w0]

Bibliography:
    C. Ghiaus (2022) Computational psychrometric analysis of cooling systems
    as a control problem: case of cooling and dehumidification systems,
    International Journal of Building Performance Simulation,
    vol. 15, no. 1, p. 21-38
    DOI: 10.1080/19401493.2021.1995498
    https://hal.archives-ouvertes.fr/hal-03484064/document

    EnergiePlus-lesite. Humidificateur à vapeur
    https://energieplus-lesite.be/techniques/humidification-et-deshumidification5/types-d-humidificateurs/humidificateurs-a-vapeur/
"""

# 1. Import modules
import numpy as np
import psychro as psy
import MdlClz

# constants
c = 1e3         # J/kg K, air specific heat
l = 2496e3      # J/kg, latent heat


# 2. Create a function which solves the problem
def vap_hum(m, θo, φo, QlVH):
    wo = psy.w(θo, φo)              # humidity inlet air

    # Model
    no_eq = 2                       # number of equations
    A = np.zeros((no_eq, no_eq))    # matrix of coefficents of unknowns
    b = np.zeros(no_eq)             # vector of inputs
    # [HC]
    A[0, 0], b[0] = m * c, m * c * θo
    A[1, 1], b[1] = m * l, m * l * wo + QlVH

    x = np.linalg.solve(A, b)
    return x


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
    m, air_i, mv = [x[k] for k in ['m', 'air_i', 'mv']]
    # m       mass flow rate [kg/s]
    # θo, φo  inlet temperature [°C] & humidity ratio [%]
    # mv      mass flow of vapor [kg/h]
    θo, φo = air_i
    φo /= 100
    mv /= 3600
    QlVH = l * mv   # W, latent heat flow rate of the humidifier

    x = vap_hum(m, θo, φo, QlVH)

    y = {'θVH': x[0],                       # °C, temperature
         'φVH': psy.φ(x[0], x[1]) * 100,    # %, relative humidity
         'QlVH': QlVH / 1000}               # kW, latent load
    return y


# 3. Define the input space
x_ranges = {
    'm': np.array([12.75, 10.5]),           # kg/s, mass flow rate
    'air_i': np.array([[35, 40],            # °C, %, inlet air
                       [30, 50]]),
    'mv': np.array([200, 150])}             # kg/h, mass flow rate of vapor


# 4. Write the text of the cloze question in Markdown
text = """
**Notes :**

- Dans l’enthalpie de la vapeur, on néglige la chaleur sensible.

- La chaleur latente de vaporisation est $$l_v$$ = 2496 kJ/kg.

**Données**

On considère que le débit d’air de {m:.1f} kg air sec par seconde avec les
caractéristiques ({air_i[0]:.0f} °C, {air_i[1]:.0f} %) est humidifié par
l'injection de {mv:.1f} kg de vapeur d'eau par heure.

**Trouvez :**

- La température de l'air à la sortie de l'hudificateur :
$$\\theta_{{VH}}$$ = {{1:NUMERICAL:={θVH:.1f}:2}} °C.

- L'humidité relative de l'air à la sortie de l'hudificateur :
$$\\varphi_{{VH}}$$ = {{1:NUMERICAL:={φVH:.1f}:5}} %.

- La puissance électrique necessaire pour évaporer l'eau injectée sous la forme
de la vapeur :
$$\\dot{{Q}}_{{l,VH}}$$ = {{1:NUMERICAL:={QlVH:.1f}:5}} kW.
"""

# 5. Generate the quiz in Moodle - cloze format and save .xml file
question_name = "CM4_v_hum"      # It will be followed by question number
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
