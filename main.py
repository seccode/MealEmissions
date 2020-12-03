import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

FOOD_LOSS_AND_WASTE_RATES = {
    "Grain": {
        "RETAIL": np.random.triangular(0, 0.12, 1),
        "HOME": np.random.triangular(0, 0.19, 1)
    },
    "Fruit": {
        "RETAIL": np.random.triangular(0, 0.09, 1),
        "HOME": np.random.triangular(0, 0.19, 1)
    },
    "Vegetable": {
        "RETAIL": np.random.triangular(0, 0.08, 1),
        "HOME": np.random.triangular(0, 0.22, 1)
    },
    "Dairy": {
        "RETAIL": np.random.triangular(0, 0.11, 1),
        "HOME": np.random.triangular(0, 0.20, 1)
    },
    "Meat": {
        "RETAIL": np.random.triangular(0, 0.05, 1),
        "HOME": np.random.triangular(0, 0.22, 1)
    },
    "Poultry": {
        "RETAIL": np.random.triangular(0, 0.04, 1),
        "HOME": np.random.triangular(0, 0.18, 1)
    },
    "Fish": {
        "RETAIL": np.random.triangular(0, 0.08, 1),
        "HOME": np.random.triangular(0, 0.31, 1)
    },
    "Eggs": {
        "RETAIL": np.random.triangular(0, 0.07, 1),
        "HOME": np.random.triangular(0, 0.21, 1)
    },
    "Spice": {
        "RETAIL": 0,
        "HOME": 0
    }
}

def get_meal_kit_ingredients():
    """
    Get meal kit ingredients and food-specific
    packaging masses
    """
    df = pd.read_excel("meal_kit_ingredients.xlsx")
    salmon_df = df.iloc[1:10]
    cheeseburger_df = df.iloc[11:]

    return salmon_df, cheeseburger_df

def get_grocery_meal_ingredients():
    """
    Get grocery mael ingredients and food-specific
    packaging masses
    """
    df = pd.read_excel("grocery_meal_ingredients.xlsx")
    salmon_df = df.iloc[1:10]
    cheeseburger_df = df.iloc[11:]

    return salmon_df, cheeseburger_df

def get_food_and_packaging_emissions():
    """
    Get emission values associated with
    specific foods and packaging
    """
    return pd.read_excel("food_and_packaging_emissions.xlsx")

def get_food_loss_and_waste_rates():
    """
    Get food loss and waste rates
    """
    return pd.read_excel("food_loss_and_waste_rates.xlsx")

SALMON_MEAL_KIT_INGREDIENTS, CHEESEBURGER_MEAL_KIT_INGREDIENTS = \
    get_meal_kit_ingredients()

SALMON_GROCERY_MEAL_INGREDIENTS, CHEESEBURGER_GROCERY_MEAL_INGREDIENTS = \
    get_grocery_meal_ingredients()

FOOD_AND_PACKAGING_EMISSIONS = get_food_and_packaging_emissions()

FOOD_LOSS_AND_WASTE_RATES = get_food_loss_and_waste_rates()



def get_meal_kits_per_box():
    """
    Return the number of meal kits per box according
    to a binomial distribution with probabilities:
        3 (85%)
        2 (15%)
    """
    return np.random.binomial(1, 0.85) + 2

def get_food_retail_loss_and_home_waste_rate(food):
    """
    Get food retail loss and home waste rates
    according to trinagular distribution
    """
    retail_loss = FOOD_LOSS_AND_WASTE_RATES[food["Category"]]["RETAIL"]
    home_waste = FOOD_LOSS_AND_WASTE_RATES[food["Category"]]["HOME"]

    return (retail_loss, home_waste)

def meal_kit_processing_loss_rate():
    """
    Get meal kit processing loss rate according
    to a triangular distribution with a mode of 10%
    """
    return np.random.triangular(0, 0.10, 1)

def get_meals_purchased_at_grocery_store():
    """
    Get number of meals purchased at grocery store
    according to a uniform distribution with a
    range of 1-5
    """
    return np.random.randint(1, 6, 1)[0]

def get_meals_per_grocery_bag():
    """
    Get number of meals per grocery store bag
    according to a uniform distribution with
    a range of 2-3
    """
    return np.random.randint(2, 4, 1)[0]



class Meal:
    def __init__(self, name):
        self.name = name
        return


class MealKitService:
    def __init__(self):
        return

    def get_production_emissions(self, meal):
        raise Exception("Unimplemented")
        return

    def get_packaging_emissions(self, meal):
        raise Exception("Unimplemented")
        return

    def get_processing_emissions(self, meal):
        raise Exception("Unimplemented")
        return

    def get_delivery_emissions(self, meal):
        raise Exception("Unimplemented")
        return

    def get_last_mile_transportation_emissions(self, meal):
        raise Exception("Unimplemented")
        return

    def get_total_emissions(self, meal):
        return self.get_production_emissions(meal) + \
            self.get_packaging_emissions(meal) + \
            self.get_processing_emissions(meal) + \
            self.get_delivery_emissions(meal) + \
            self.get_last_mile_transportation_emissions(meal)



class GroceryService:
    def __init__(self):
        return

    def get_production_emissions(self, meal):
        raise Exception("Unimplemented")
        return

    def get_packaging_emissions(self, meal):
        raise Exception("Unimplemented")
        return

    def get_transportation_emissions(self, meal):
        raise Exception("Unimplemented")
        return

    def get_retail_operation_emissions(self, meal):
        raise Exception("Unimplemented")
        return

    def get_last_mile_transportation_emissions(self, meal):
        raise Exception("Unimplemented")
        return

    def get_total_emissions(self, meal):
        return self.get_production_emissions(meal) + \
            self.get_packaging_emissions(meal) + \
            self.get_transportation_emissions(meal) + \
            self.get_retail_operation_emissions(meal) + \
            self.get_last_mile_transportation_emissions(meal)


def main():

    meal_1 = Meal("Salmon")
    meal_2 = Meal("Cheeseburger")

    mks = MealKitService()
    gs = GroceryService()

    for meal in [meal_1, meal_2]:
        print("Meal Kit Service Total Emissions for {} meal: {} kg CO2".format(
            meal.name, mks.get_total_emissions(meal)))

    return

if __name__ == "__main__":
    main()

