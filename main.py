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

def get_food_specific_retail_loss_rate(food_type):
    return {
        "Grain": np.random.triangular(9, 12, 15), # ASSUMPTION: bounded by +/- 3%
        "Fruit": np.random.triangular(6, 9, 12), # ASSUMPTION: bounded by +/- 3%,
        "Vegetable": np.random.triangular(5, 8, 11), # ASSUMPTION: bounded by +/- 3%,
        "Dairy": np.random.triangular(8, 11, 14), # ASSUMPTION: bounded by +/- 3%,
        "Meat": np.random.triangular(2, 5, 8), # ASSUMPTION: bounded by +/- 3%,
        "Fish": np.random.triangular(5, 8, 11), # ASSUMPTION: bounded by +/- 3%,
        "Eggs": np.random.triangular(4, 7, 10), # ASSUMPTION: bounded by +/- 3%
        "Spice": 0 # ASSUMPTION: No loss rate
    }[food_type]

def get_food_specific_home_loss_rate(food_type):
    return {
        "Grain": np.random.triangular(16, 19, 22), # ASSUMPTION: bounded by +/- 3%
        "Fruit": np.random.triangular(16, 19, 22), # ASSUMPTION: bounded by +/- 3%,
        "Vegetable": np.random.triangular(19, 22, 25), # ASSUMPTION: bounded by +/- 3%,
        "Dairy": np.random.triangular(17, 20, 23), # ASSUMPTION: bounded by +/- 3%,
        "Meat": np.random.triangular(2, 5, 8), # ASSUMPTION: bounded by +/- 3%,
        "Fish": np.random.triangular(28, 31, 34), # ASSUMPTION: bounded by +/- 3%,
        "Eggs": np.random.triangular(19, 21, 24), # ASSUMPTION: bounded by +/- 3%
        "Spice": 0 # ASSUMPTION: No loss rate
    }[food_type]

def get_food_specific_loss_rate(food_type, grocery=True):
    if grocery:
        return get_food_specific_retail_loss_rate(food_type)

    return get_food_specific_home_loss_rate(food_type)

def truncnorm(mean, sd):
    ret = np.random.normal(mean, sd)
    if ret < 0:
        return 0
    return ret

def generate_parameters():
    """
    Generate random variable parameters for simulation
    """
    return {
        "R": lambda food_type, is_grocery: get_food_specific_loss_rate(food_type, is_grocery), # Home waste rate
        "D_TM": np.random.triangular(50, 796.87, 1221), # Meal Kit transportation distance
        "C_T": np.random.triangular(0.18 / 10**6, 0.28 / 10**6, 0.38 / 10**6), # Fuel emissions, ASSUMPTION: bounded by +/- 0.10
        "Y": np.random.triangular(5, 10, 15), # Energy consumed per package, ASSUMPTION: bounded by +/- 5 MJ/package
        "C_I": np.random.triangular(0.18 / 10**6, 0.28 / 10**6, 0.38 / 10**6), # Fuel emissions, ASSUMPTION: bounded by +/- 0.10
        "N_M": np.random.binomial(1, 0.85) + 2,
        "D_TG": np.random.triangular(35, 47.15, 59), # Grocery transportation distance
        "H_DF": np.random.triangular(10, 48.5, 60), # Grocery display time, ASSUMPTION: bounded by 10, 60
        "H_WF": np.random.triangular(10, 18.23, 30), # Hours in walk-in cooler, ASSUMTPION: bounded by 10, 30
        "C_D": np.random.triangular(3.31 / 10**6, 6.62 / 10**6, 9.93 / 10**6), # Display emissions, ASSUMPTION: bounded by +/- 50%
        "C_A": np.random.triangular(3.22 / 10**6, 6.44 / 10**6, 9.66 / 10**6), # Walk-in cooler emissions, ASSUMPTION: bounded by +/- 50%
        "D_L": truncnorm(4.43, 2), # Grocery last-mile distance, ASSUMPTION: standard deviation of 2
        "V": truncnorm(23.36, 5), # Vehicle fuel efficiency, ASSUMPTION: standard deviation of 5
        "C_G": np.random.triangular(0.18, 0.28, 0.38), # Fuel emissions, ASSUMPTION: bounded by +/- 0.10
        "N_G": np.random.randint(1, 6) # Number of grocery meals per trip
    }

class Meal:
    def __init__(self, name, meal_kit_ingredients, grocery_meal_ingredients):
        self.name = name
        self.meal_kit_ingredients = meal_kit_ingredients
        self.grocery_meal_ingredients = grocery_meal_ingredients
        return

class MealKitService:
    def __init__(self, meal, params):
        self.meal = meal
        self.params = params

        Q_MF = [e + u for e, u in zip(meal.meal_kit_ingredients["Food Eaten (g)"],
            meal.meal_kit_ingredients["Food Unused (g)"])]

        r_vals = [self.params["R"](food_type, False) / 100 for food_type in meal.meal_kit_ingredients["Category"]]
        self.Q_CF = [q / (1 - r) for q, r in zip(Q_MF, r_vals)]

        self.C_F = [FOOD_AND_PACKAGING_EMISSIONS.loc[item]["kg CO2-eq/g "] for item in \
            meal.meal_kit_ingredients.index]

        self.Q_B = [sum(meal.meal_kit_ingredients[col + " (g)"]) for col in PACKAGINGS]

        self.C_B = [FOOD_AND_PACKAGING_EMISSIONS.loc[item]["kg CO2-eq/g "] for item in PACKAGINGS]

        # ASSUMPTION: Q_TF == Q_MF for Meal Kit?
        self.Q_TF = Q_MF

        return

    def get_production_emissions(self, _print=True):

        ret = sum([q * c for q, c in zip(self.Q_CF, self.C_F)])
        if _print:
            print("Meal kit production emissions: {}".format(ret))

        return ret

    def get_packaging_emissions(self, _print=True):

        ret = sum([q * c / self.params["N_M"] for q, c in zip(self.Q_B, self.C_B)])
        if _print:
            print("Meal kit packaging emissions: {}".format(ret))

        return ret

    def get_processing_emissions(self, _print=True):
        """
        ASSUMPTION: No emissions from meal kit processing
        """

        ret = sum([q * self.params["D_TM"] * self.params["C_T"] for q in self.Q_CF])
        if _print:
            print("Meal kit processing emissions: {}".format(ret))

        return ret

    def get_delivery_emissions(self, _print=True):

        ret = sum([q * self.params["D_TM"] * self.params["C_T"] for q in self.Q_TF])
        if _print:
            print("Meal kit delivery emissions: {}".format(ret))

        return ret

    def get_last_mile_transportation_emissions(self, _print=True):

        ret = self.params["Y"] * self.params["C_I"] / self.params["N_M"]
        if _print:
            print("Meal kit last mile emissions: {}".format(ret))

        return ret

    def get_individual_emissions(self):
        return (
            self.get_production_emissions(_print=False),
            self.get_packaging_emissions(_print=False),
            self.get_processing_emissions(_print=False),
            self.get_delivery_emissions(_print=False),
            self.get_last_mile_transportation_emissions(_print=False)
        )

    def get_total_emissions(self):
        return self.get_production_emissions() + \
            self.get_packaging_emissions() + \
            self.get_processing_emissions() + \
            self.get_delivery_emissions() + \
            self.get_last_mile_transportation_emissions()


class GroceryService:
    def __init__(self, meal, params):
        self.meal = meal
        self.params = params

        Q_MF = [e + u for e, u in zip(meal.meal_kit_ingredients["Food Eaten (g)"],
            meal.meal_kit_ingredients["Food Unused (g)"])]

        R = [FOOD_LOSS_AND_WASTE_RATES.loc[item]["Store Loss Rate (%)"]/100 for item in \
            meal.meal_kit_ingredients.index]

        self.Q_CF = [q / (1 - r) for q, r in zip(Q_MF, R)]

        self.C_F = [FOOD_AND_PACKAGING_EMISSIONS.loc[item]["kg CO2-eq/g "] for item in \
            meal.meal_kit_ingredients.index]

        self.Q_B = [sum(meal.meal_kit_ingredients[col + " (g)"]) for col in PACKAGINGS]

        self.C_B = [FOOD_AND_PACKAGING_EMISSIONS.loc[item]["kg CO2-eq/g "] for item in PACKAGINGS]

        # ASSUMPTION: Q_TF == Q_CF for Grocery?
        self.Q_TF = self.Q_CF

        return

    def get_production_emissions(self, _print=True):

        ret = round(sum([q * c for q, c in zip(self.Q_CF, self.C_F)]),2)
        if _print:
            print("Grocery production emissions: {}".format(ret))

        return ret

    def get_packaging_emissions(self, _print=True):

        ret = sum([q * c for q, c in zip(self.Q_B, self.C_B)])
        if _print:
            print("Grocery packaging emissions: {}".format(ret))

        return ret

    def get_transportation_emissions(self, _print=True):

        ret = sum([q * self.params["D_TG"] * self.params["C_T"] for q in self.Q_TF])
        if _print:
            print("Grocery transportation emissions: {}".format(ret))

        return ret

    def get_retail_operation_emissions(self, _print=True):

        ret = sum([q * self.params["H_DF"] * self.params["C_D"] + q * self.params["H_WF"] * self.params["C_A"] for q in self.Q_CF])
        if _print:
            print("Grocery retail emissions: {}".format(ret))

        return ret

    def get_last_mile_transportation_emissions(self, _print=True):
 
        ret = (self.params["D_L"] / self.params["V"]) * self.params["C_G"] / self.params["N_G"]
        if _print:
            print("Grocery last-mile emissions: {}".format(ret))

        return ret

    def get_individual_emissions(self):
        return (
            self.get_production_emissions(_print=False),
            self.get_packaging_emissions(_print=False),
            self.get_transportation_emissions(_print=False),
            self.get_retail_operation_emissions(_print=False),
            self.get_last_mile_transportation_emissions(_print=False)
        )

    def get_total_emissions(self):
        return self.get_production_emissions() + \
            self.get_packaging_emissions() + \
            self.get_transportation_emissions() + \
            self.get_retail_operation_emissions() + \
            self.get_last_mile_transportation_emissions()


def plot_bars(data):
    data = np.array(data).T

    mk_names = [
        "Production",
        "Packaging",
        "Processing",
        "Delivery",
        "Last Mile"
    ]

    gs_names = [
        "Production",
        "Packaging",
        "Transportation",
        "Retail",
        "Last Mile"
    ]

    mk_colors = [
        "blue",
        "red",
        "orange",
        "yellow",
        "green"
    ]

    gs_colors = [
        "blue",
        "red",
        "purple",
        "pink",
        "green"
    ]

    bars = []
    inds = np.arange(4)

    def get_bottoms(i):
        bottoms = [0, 0, 0, 0]
        for j in range(i):
            for k in range(4):
                bottoms[k] += data[j][k]

        return bottoms

    for i, row in enumerate(data):
        bar = plt.bar(inds, row, 0.5, bottom=get_bottoms(i))
        bar[0].set_color(mk_colors[i])
        bar[1].set_color(gs_colors[i])
        bar[2].set_color(mk_colors[i])
        bar[3].set_color(gs_colors[i])

        bars.append(bar)


    plt.ylabel("Emissions kg CO2-eq")
    plt.xticks(inds, ["Salmon, Meal Kit", "Salmon, Grocery",
                      "Cheeseburger, Meal Kit", "Cheeseburger, Grocery"], rotation=15)

    plt.tight_layout()
    plt.ylim(-1, 10)
    plt.xlim(-0.5, 3.5)
    plt.plot([-1, 4], [0, 0], 'k', alpha=0.5)

    plt.legend(
        (bars[0][0], bars[1][0], bars[2][0], bars[3][0], bars[4][0], bars[2][1], bars[3][1]),
        ("Production", "Packaging", "Processing", "Delivery", "Last-mile", "Transportation", "Retail")
        )

    plt.show()
    return

def run():

    # Create meals
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

    # Get random variable values
    params = generate_parameters()

    # Instantiate meal services
    mks_1 = MealKitService(meal_1, params)
    mks_2 = MealKitService(meal_2, params)
    gs_1 = GroceryService(meal_1, params)
    gs_2 = GroceryService(meal_2, params)

    # Individual emission contributions
    data = []

    # Print total emissions for each meal service
    for mk, gs in zip([mks_1, mks_2], [gs_1, gs_2]):
        print("Meal Kit Service Total Emissions for {} meal: {} kg CO2\n".format(
            mk.meal.name, mk.get_total_emissions()))

        print("Grocery Service Total Emissions for {} meal: {} kg CO2\n".format(
            gs.meal.name, gs.get_total_emissions()))


        data.append(mk.get_individual_emissions())
        data.append(gs.get_individual_emissions())

    plot_bars(data)
    return

if __name__ == "__main__":
    run()

