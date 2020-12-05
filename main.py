import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def get_meal_kit_ingredients():
    """
    Get meal kit ingredients and food-specific
    packaging masses
    """
    df = pd.read_excel("meal_kit_ingredients.xlsx", index_col=0).fillna(0)
    salmon_df = df.iloc[1:10]
    cheeseburger_df = df.iloc[11:]

    return salmon_df, cheeseburger_df

def get_grocery_meal_ingredients():
    """
    Get grocery mael ingredients and food-specific
    packaging masses
    """
    df = pd.read_excel("grocery_meal_ingredients.xlsx", index_col=0).fillna(0)
    salmon_df = df.iloc[1:10]
    cheeseburger_df = df.iloc[11:]

    return salmon_df, cheeseburger_df

def get_food_and_packaging_emissions():
    """
    Get emission values associated with
    specific foods and packaging
    """
    return pd.read_excel("food_and_packaging_emissions.xlsx").drop_duplicates()

def get_food_loss_and_waste_rates():
    """
    Get food loss and waste rates
    """
    return pd.read_excel("food_loss_and_waste_rates.xlsx", index_col=0).drop_duplicates()

SALMON_MEAL_KIT_INGREDIENTS, CHEESEBURGER_MEAL_KIT_INGREDIENTS = \
    get_meal_kit_ingredients()

SALMON_GROCERY_MEAL_INGREDIENTS, CHEESEBURGER_GROCERY_MEAL_INGREDIENTS = \
    get_grocery_meal_ingredients()

FOOD_AND_PACKAGING_EMISSIONS = get_food_and_packaging_emissions()

FOOD_LOSS_AND_WASTE_RATES = get_food_loss_and_waste_rates()


class MonteCarloParameters:
    def __init__(self):
        return

class Meal:
    def __init__(self, name, meal_kit_ingredients, grocery_meal_ingredients):
        self.name = name
        self.meal_kit_ingredients = meal_kit_ingredients
        self.grocery_meal_ingredients = grocery_meal_ingredients
        return
    

class MealKitService:
    def __init__(self, meal):
        self.meal = meal
        Q_MF = [e + u for e, u in zip(meal.meal_kit_ingredients["Food Eaten (g)"],
            meal.meal_kit_ingredients["Food Unused (g)"])]

        # TODO, add parameter to Monte Carlo params
        R = 0.1

        self.Q_CF = sum([q / R for q in Q_MF])

        self.C_F = None
        self.Q_B = None
        self.C_B = None
        self.Q_TF = None
        self.D_T = None
        self.C_T = None
        self.Y = None
        self.C_I = None
        self.N = None
        return
    
    def get_production_emissions(self, meal):
        raise Exception("Unimplemented")
        assert self.Q_CF and self.C_F, "Parameters not defined yet"

        return self.Q_CF * self.C_F

    def get_packaging_emissions(self, meal):
        assert self.Q_B and self.C_B, "Parameters not defined yet"
        raise Exception("Unimplemented")

        return self.Q_B * self.C_B

    def get_processing_emissions(self, meal):
        return 0

    def get_delivery_emissions(self, meal):
        raise Exception("Unimplemented")
        assert self.Q_TF and self.D_T and self.C_T, "Parameters not defined yet"

        return self.Q_TF * self.D_T * self.C_T

    def get_last_mile_transportation_emissions(self, meal):
        raise Exception("Unimplemented")
        assert self.Y and self.C_I and self.N, "Parameters not defined yet"

        return self.Y * self.C_I / self.N

    def get_total_emissions(self, meal):
        return self.get_production_emissions(meal) + \
            self.get_packaging_emissions(meal) + \
            self.get_processing_emissions(meal) + \
            self.get_delivery_emissions(meal) + \
            self.get_last_mile_transportation_emissions(meal)



class GroceryService:
    def __init__(self, meal):
        self.meal = meal
        Q_MF = [e + u for e, u in zip(meal.meal_kit_ingredients["Food Eaten (g)"],
            meal.meal_kit_ingredients["Food Unused (g)"])]

        R = [FOOD_LOSS_AND_WASTE_RATES[item]["Store Loss Rate (%)"] for item in \
            meal.meal_kit_ingredients.index]

        self.Q_CF = sum([q / (1 - r) for q, r in zip(Q_MF, R)])

        self.C_F = None
        self.Q_B = None
        self.C_B = None
        self.Q_TF = None
        self.D_T = None
        self.C_T = None
        self.H_DF = None
        self.H_WF = None
        self.C_D = None
        self.C_A = None
        self.D_L = None
        self.V = None
        self.C_G = None
        self.N = None
        return

    def get_production_emissions(self, meal):
        raise Exception("Unimplemented")
        assert self.Q_CF and self.C_F, "Parameters not defined yet"

        return self.Q_CF * self.C_F

    def get_packaging_emissions(self, meal):
        raise Exception("Unimplemented")
        assert self.Q_B and self.C_B, "Parameters not defined yet"

        return self.Q_B * self.C_B

    def get_transportation_emissions(self, meal):
        raise Exception("Unimplemented")
        assert self.Q_TF and self.D_T and self.C_T, "Parameters not defined yet"

        return self.Q_TF * self.D_T * self.C_T

    def get_retail_operation_emissions(self, meal):
        raise Exception("Unimplemented")
        assert self.H_DF and self.H_WF and self.C_D and self.C_A, "Parameters not defined yet"

        return self.Q_CF * self.H_DF * self.C_D + self.Q_CF * self.H_WF * self.C_A

    def get_last_mile_transportation_emissions(self, meal):
        raise Exception("Unimplemented")
        assert self.D_L and self.V and self.C_G and self.N, "Parameters not defined yet"

        return (self.D_L / self.V) * self.C_G / self.N

    def get_total_emissions(self, meal):
        return self.get_production_emissions(meal) + \
            self.get_packaging_emissions(meal) + \
            self.get_transportation_emissions(meal) + \
            self.get_retail_operation_emissions(meal) + \
            self.get_last_mile_transportation_emissions(meal)


def main():

    meal_1 = Meal(
        "Salmon",
        SALMON_MEAL_KIT_INGREDIENTS,
        SALMON_GROCERY_MEAL_INGREDIENTS
        )

    meal_2 = Meal(
        "Cheeseburger",
        CHEESEBURGER_MEAL_KIT_INGREDIENTS,
        CHEESEBURGER_GROCERY_MEAL_INGREDIENTS
        )

    mks_1 = MealKitService(meal_1)
    mks_2 = MealKitService(meal_2)
    gs_1 = GroceryService(meal_1)
    gs_2 = GroceryService(meal_2)

    for mk, gs in zip([mks_1, mks_2], [gs_1, gs_2]):
        print("Meal Kit Service Total Emissions for {} meal: {} kg CO2\n".format(
            mk.meal.name, mk.get_total_emissions()))
        
        print("Grocery Service Total Emissions for {} meal: {} kg CO2\n".format(
            gs.meal.name, gs.get_total_emissions()))

    return

if __name__ == "__main__":
    main()

