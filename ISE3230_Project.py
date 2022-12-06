import gurobipy as gp
from gurobipy import GRB
import re
import sys
import pandas as pd
from difflib import get_close_matches

def getMenu(place, menuList):
    menu = pd.DataFrame()
    bestMatch = get_close_matches(place, menuList, n=1)[0]
    if bestMatch == "12thAvenueBreadCompany":
        menu = TwelfthAveBreadDF
    elif bestMatch == "BerryCafe":
        menu = BerryCafeDF
    elif bestMatch == "CurlMarketBurrito":
        menu = CurlMarketBurritoDF
    elif bestMatch == "CurlMarketPasta":
        menu = CurlMarketPastaDF
    elif bestMatch == "CurlMarketSandwich":
        menu = CurlMarketSandwichDF
    elif bestMatch == "CurlMarketSushi":
        menu = CurlMarketSushiDF
    elif bestMatch == "MarketplaceOnNeilDeliDF":
        menu = MarketplaceOnNeilDeliDF
    elif bestMatch == "MarketplaceOnNeilPastaRiceBowls":
        menu = MarketplaceOnNeilPastaRiceBowlsDF
    elif bestMatch == "MarketplaceOnNeilPizza":
        menu = MarketplaceOnNeilPizzaDF
    elif bestMatch == "MarketplaceOnNeilSushi":
        menu = MarketplaceOnNeilSushiDF
    elif bestMatch == "MirrorLakeEatery":
        menu = MirrorLakeEateryDF
    elif bestMatch == "Sloopys":
        menu = SloopysDF
    elif bestMatch == "UnionMarketGrainBowl":
        menu = UnionMarketGrainBowlDF
    elif bestMatch == "UnionMarketGrill":
        menu = UnionMarketGrillDF
    elif bestMatch == "UnionMarketSandwich":
        menu = UnionMarketSandwichDF
    elif bestMatch == "UnionMarketSushi":
        menu = UnionMarketSushiDF
    elif bestMatch == "Woodys":
        menu = WoodysDF
    elif bestMatch == "TerraByteCafe":
        menu = TerraByteCafeDF
    return menu


TwelfthAveBreadDF = pd.read_csv("menuCSV/12thAvenueBreadCompany.csv")
BerryCafeDF = pd.read_csv("menuCSV/BerryCafe.csv")
CurlMarketBurritoDF = pd.read_csv("menuCSV/CurlMarketBurrito.csv")
CurlMarketPastaDF = pd.read_csv("menuCSV/CurlMarketPasta.csv")
CurlMarketSandwichDF = pd.read_csv("menuCSV/CurlMarketSandwich.csv")
CurlMarketSushiDF = pd.read_csv("menuCSV/CurlMarketSushi.csv")
MarketplaceOnNeilDeliDF = pd.read_csv("menuCSV/MarketplaceOnNeilDeli.csv")
MarketplaceOnNeilPastaRiceBowlsDF = pd.read_csv("menuCSV/MarketplaceOnNeilPastaRiceBowls.csv")
MarketplaceOnNeilPizzaDF = pd.read_csv("menuCSV/MarketplaceOnNeilPizza.csv")
MarketplaceOnNeilSushiDF = pd.read_csv("menuCSV/MarketplaceOnNeilSushi.csv")
MirrorLakeEateryDF = pd.read_csv("menuCSV/MirrorLakeEatery.csv")
SloopysDF = pd.read_csv("menuCSV/Sloopys.csv")
UnionMarketGrainBowlDF = pd.read_csv("menuCSV/UnionMarketGrainBowl.csv")
UnionMarketGrillDF = pd.read_csv("menuCSV/UnionMarketGrill.csv")
UnionMarketSandwichDF = pd.read_csv("menuCSV/UnionMarketSandwich.csv")
UnionMarketSushiDF = pd.read_csv("menuCSV/UnionMarketSushi.csv")
WoodysDF = pd.read_csv("menuCSV/Woodys.csv")
TerraByteCafeDF = pd.read_csv("menuCSV/TerraByteCafe.csv")

menuList = ["Woodys",
            "UnionMarketSushi",
            "UnionMarketSandwich",
            "UnionMarketGrill",
            "UnionMarketGrainBowl",
            "Sloopys",
            "MirrorLakeEatery",
            "MarketplaceOnNeilSushi",
            "MarketplaceOnNeilPizza",
            "MarketplaceOnNeilPastaRiceBowls",
            "MarketplaceOnNeilDeli",
            "CurlMarketSushi",
            "CurlMarketSandwich",
            "CurlMarketPasta",
            "CurlMarketBurrito",
            "BerryCafe",
            "12thAvenueBreadCompany",
            "TerraByteCafe"]
 
fullMenuItems = []
fullMenuPrices = []

#Create a full menu too
for menu in menuList:
    df = pd.read_csv(f"menuCSV/{menu}.csv")
    items = df['Item'].tolist()
    tempItems = [menu + ' ' + food for food in items]
    fullMenuItems = fullMenuItems + tempItems
    prices = df['Price'].tolist()
    fullMenuPrices = fullMenuPrices + prices

while True:
    dollars = 0
    items = []
    prices = []

    print("""Please enter a number of Swipes, Dining Dollars, or BuckID cash in the following format:
    'n swipes', where n is the number of swipes you wish to use;
    'n Dining Dollars', where n is the number of dining dollars you have;
    'n BuckID', where n is the number of BuckID Dollars you have;
    Alternatively, enter "exit" to exit.""")

    usrInput = input()
    try:
        digits = float(re.search(r'\d{0,3}(\.\d{1,2})?', usrInput).group())
    except:
        sys.exit()

    if "swipe" in usrInput.lower():
        dollars = digits * 8
        print("List of available restaurants includes: ")
        for menu in menuList:
            print("\t" + menu)
        print("Please enter the name of the restaurant you'd like to eat at: ")
        place = input()
        menuDF = getMenu(place, menuList)
        items = menuDF["Item"].tolist()
        prices = menuDF["Price"].tolist()
    elif "dining" in usrInput.lower() or "dd" in usrInput.lower():
        dollars = float(digits / .65)
        items = fullMenuItems
        prices = fullMenuPrices
    elif "buckid" in usrInput.lower() or "buck" in usrInput.lower():
        dollars = digits
        items = fullMenuItems
        prices = fullMenuPrices
    else:
        print("Payment method not recognized. Program will exit.")
        sys.exit()

    m = gp.Model("ISE3230_Project")
    m.Params.LogToConsole = 0

    x = m.addVars(len(items), vtype=GRB.INTEGER, name="x")

    #Create sum to optimize over
    sum = 0
    for i in range(len(items)):
        sum += prices[i] * x[i]

    m.setObjective(sum, GRB.MAXIMIZE)

    m.addConstr(sum <= dollars)
    for i in range(len(items)):
        m.addConstr(x[i] >= 0)

    m.optimize()

    print(f"The optimal use of your money will cost ${round(m.objVal, 2)}, leaving you with ${round(dollars - m.objVal, 2)} left over.")

    for v in m.getVars():
        if int(v.x) != 0:
            index = int(re.search(r'\d+', v.varName).group())
            if v.x == 1:
                print(f"Order {int(v.x)} {items[index]} for ${round(int(v.x) * prices[index], 2)}")
            else:
                print(f"Order {int(v.x)} {items[index]}s for ${round(int(v.x) * prices[index], 2)}")