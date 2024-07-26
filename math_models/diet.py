# Optimization Model for Diet Problem with Ortools, Deployed in Flask
"""The Stigler diet problem.
Link: https://developers.google.com/optimization/lp/stigler_diet

A description of the problem can be found here:
https://en.wikipedia.org/wiki/Stigler_diet.
"""
import pandas as pd
from ortools.linear_solver import pywraplp
from data.demo import data # Food Nutrients Data

# async function
def solve(nutrients):
    """Entry point of the program.
    nunutrients_parameters:
    Example:
    nutrients = [
        ["Calories (kcal)", 3],
        ["Protein (g)", 70],
        ["Calcium (g)", 0.8],
        ["Iron (mg)", 12],
        ["Vitamin A (KIU)", 5],
        ["Vitamin B1 (mg)", 1.8],
        ["Vitamin B2 (mg)", 2.7],
        ["Niacin (mg)", 18],
        ["Vitamin C (mg)", 75],]
    """

    # Instantiate the data problem.
    # Nutrient minimums.

    # Instantiate a Glop solver and naming it.
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        return

    # Declare an array to hold our variables.
    foods = [solver.NumVar(0.0, solver.infinity(), item[0]) for item in data]

    print("Number of variables =", solver.NumVariables())

    # Create the constraints, one per nutrient.
    constraints = []
    for i, nutrient in enumerate(nutrients):
        constraints.append(solver.Constraint(nutrient[1], solver.infinity()))
        for j, item in enumerate(data):
            constraints[i].SetCoefficient(foods[j], item[i + 3])

    print("Number of constraints =", solver.NumConstraints())

    # Objective function: Minimize the sum of (price-normalized) foods.
    objective = solver.Objective()
    for food in foods:
        objective.SetCoefficient(food, 1)
    objective.SetMinimization()

    print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve()

    # Check that the problem has an optimal solution.
    if status != solver.OPTIMAL:
        print("The problem does not have an optimal solution!")
        if status == solver.FEASIBLE:
            print("A potentially suboptimal solution was found.")
        else:
            print("The solver could not solve the problem.")
            exit(1)

    # Display the amounts (in dollars) to purchase of each food.
    nutrients_result = [0] * len(nutrients)
    food_results = []
    print("\nAnnual Foods:")
    for i, food in enumerate(foods):
        if food.solution_value() > 0.0:
            food_cost = 365.0 * food.solution_value()
            print("{}: ${}".format(data[i][0], food_cost))
            food_results.append([data[i][0], food_cost])
            for j, _ in enumerate(nutrients):
                nutrients_result[j] += data[i][j + 3] * food.solution_value()
    print("\nOptimal annual price: ${:.4f}".format(365.0 * objective.Value()))

    print("\nNutrients per day:")
    nutrient_results = []
    for i, nutrient in enumerate(nutrients):
        nutrient_amount = nutrients_result[i]
        print(
            "{}: {:.2f} (min {})".format(nutrient[0], nutrient_amount, nutrient[1])
        )
        nutrient_results.append([nutrient[0], nutrient_amount, nutrient[1]])

    print("\nAdvanced usage:")
    print(f"Problem solved in {solver.wall_time():d} milliseconds")
    print(f"Problem solved in {solver.iterations():d} iterations")

    # Return the nutrients and food data in a pandas DataFrame.
    df_nutrients = pd.DataFrame(nutrient_results, columns=["Nutrient", "Amount", "Minimum"])
    df_foods = pd.DataFrame(food_results, columns=["Food", "Annual Cost"])

    return df_nutrients, df_foods


