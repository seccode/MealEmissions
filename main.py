import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PACKAGINGS = [
    "Plastic",
    "Cardboard",
    "Styrofoam",
    "Paper",
    "Glass",
    "Metal"
    ]

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
    return pd.read_excel("food_and_packaging_emissions.xlsx", index_col=0)

def get_food_loss_and_waste_rates():
    """
    Get food loss and waste rates
    """
    return pd.read_excel("food_loss_and_waste_rates.xlsx", index_col=0)


# Load data
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

        self.Q_CF = [q / (1 - R) for q in Q_MF]
        
        self.C_F = [FOOD_AND_PACKAGING_EMISSIONS.loc[item]["kg CO2-eq/g "] for item in \
            meal.meal_kit_ingredients.index]

        self.Q_B = [sum(meal.meal_kit_ingredients[col + " (g)"]) for col in PACKAGINGS]

        self.C_B = [FOOD_AND_PACKAGING_EMISSIONS.loc[item]["kg CO2-eq/g "] for item in PACKAGINGS]

        # Assumption: Q_TF == Q_MF for Meal Kit?
        self.Q_TF = Q_MF

        # TODO, add parameter to Monte Carlo params
        self.D_T = 976.87 # km

        # TODO, add parameter to Monte Carlo params
        self.C_T = 0.00000028 # kg CO2 e/g-km
        
        # TODO, add parameter to Monte Carlo params
        self.Y = 10 # MJ/package
        
        # TODO, add parameter to Monte Carlo params
        self.C_I = 0.28

        # TODO, add parameter to Monte Carlo params
        self.N = 3
        return
    
    def get_production_emissions(self):
        assert self.Q_CF and self.C_F, "Parameters not defined yet"

        ret = sum([q * c for q, c in zip(self.Q_CF, self.C_F)])
        print("Meal kit production emissions: {}".format(ret))

        return ret

    def get_packaging_emissions(self):
        assert self.Q_B and self.C_B, "Parameters not defined yet"

        ret = sum([q * c for q, c in zip(self.Q_B, self.C_B)])
        print("Meal kit packaging emissions: {}".format(ret))

        return ret

    def get_processing_emissions(self):
        """
        Assumption: No emissions from meal kit processing
        """
        return 0

    def get_delivery_emissions(self):
        assert self.Q_TF and self.D_T and self.C_T, "Parameters not defined yet"

        ret = sum([q * self.D_T * self.C_T for q in self.Q_TF])
        print("Meal kit delivery emissions: {}".format(ret))

        return ret

    def get_last_mile_transportation_emissions(self):
        assert self.Y and self.C_I and self.N, "Parameters not defined yet"

        ret = self.Y * self.C_I / self.N
        print("Meal kit delivery emissions: {}".format(ret))

        return ret

    def get_total_emissions(self):
        return self.get_production_emissions() + \
            self.get_packaging_emissions() + \
            self.get_processing_emissions() + \
            self.get_delivery_emissions() + \
            self.get_last_mile_transportation_emissions()


class GroceryService:
    def __init__(self, meal):
        self.meal = meal
        Q_MF = [e + u for e, u in zip(meal.meal_kit_ingredients["Food Eaten (g)"],
            meal.meal_kit_ingredients["Food Unused (g)"])]

        R = [FOOD_LOSS_AND_WASTE_RATES.loc[item]["Store Loss Rate (%)"]/100 for item in \
            meal.meal_kit_ingredients.index]
        
        self.Q_CF = [q / (1 - r) for q, r in zip(Q_MF, R)]

        self.C_F = [FOOD_AND_PACKAGING_EMISSIONS.loc[item]["kg CO2-eq/g "] for item in \
            meal.meal_kit_ingredients.index]
        
        self.Q_B = [sum(meal.meal_kit_ingredients[col + " (g)"]) for col in PACKAGINGS]

        self.C_B = [FOOD_AND_PACKAGING_EMISSIONS.loc[item]["kg CO2-eq/g "] for item in PACKAGINGS]

        # Assumption: Q_TF == Q_CF for Grocery?
        self.Q_TF = self.Q_CF

        # TODO, add parameter to Monte Carlo params
        self.D_T = 47.15 # km

        # TODO, add parameter to Monte Carlo params
        self.C_T = 0.00000028 # kg CO2 e/g-km

        # TODO, add parameter to Monte Carlo params
        self.H_DF = 48.5 # hours

        # TODO, add parameter to Monte Carlo params
        self.H_WF = 18.23 # hours

        # TODO, add parameter to Monte Carlo params
        self.C_D = 6.62 / 10**6

        # TODO, add parameter to Monte Carlo params
        self.C_A = 6.44 / 10**6

        # TODO, add parameter to Monte Carlo params
        self.D_L = 4.43 # miles

        # TODO, add parameter to Monte Carlo params
        self.V = 23.36 # mpg

        # TODO, add parameter to Monte Carlo params
        self.C_G = 0.28

        # TODO, add parameter to Monte Carlo params
        self.N = 5

        return

    def get_production_emissions(self):
        assert self.Q_CF and self.C_F, "Parameters not defined yet"

        ret = round(sum([q * c for q, c in zip(self.Q_CF, self.C_F)]),2)
        print("Grocery production emissions: {}".format(ret))

        return ret

    def get_packaging_emissions(self):
        assert self.Q_B and self.C_B, "Parameters not defined yet"

        ret = sum([q * c for q, c in zip(self.Q_B, self.C_B)])
        print("Grocery packaging emissions: {}".format(ret))

        return ret

    def get_transportation_emissions(self):
        assert self.Q_TF and self.D_T and self.C_T, "Parameters not defined yet"

        ret = sum([q * self.D_T * self.C_T for q in self.Q_TF])
        print("Grocery transportation emissions: {}".format(ret))

        return ret

    def get_retail_operation_emissions(self):
        assert self.H_DF and self.H_WF and self.C_D and self.C_A, "Parameters not defined yet"

        ret = sum([q * self.H_DF * self.C_D + q * self.H_WF * self.C_A for q in self.Q_CF])
        print("Grocery retail emissions: {}".format(ret))

        return ret

    def get_last_mile_transportation_emissions(self):
        assert self.D_L and self.V and self.C_G and self.N, "Parameters not defined yet"

        ret = (self.D_L / self.V) * self.C_G / self.N
        print("Grocery last-mile emissions: {}".format(ret))

        return ret

    def get_total_emissions(self):
        return self.get_production_emissions() + \
            self.get_packaging_emissions() + \
            self.get_transportation_emissions() + \
            self.get_retail_operation_emissions() + \
            self.get_last_mile_transportation_emissions()


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

