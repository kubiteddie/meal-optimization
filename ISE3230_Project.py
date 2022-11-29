import gurobipy as gp
from gurobipy import GRB
import re
import sys
import pandas as pd

menu = {}

df = pd.read_csv("menuCSV/MarketplaceOnNeilPizza.csv")
 
# converting column data to list
items = df['Item'].tolist()
prices = df['Price'].tolist()



while True:
    dollars = 0

    print("""Please enter a number of Swipes, Dining Dollars, or BuckID cash in the following format:
    'n swipes', where n is the number of swipes you wish to use;
    'n Dining Dollars', where n is the number of dining dollars you have;
    'n BuckID', where n is the number of BuckID Dollars you have;
    Alternatively, enter "exit" to exit.""")

    usrInput = input()
    try:
        digits = int(re.search(r'\d+', usrInput).group())
    except:
        sys.exit()

    if "swipe" in usrInput.lower():
        dollars = digits * 8
    elif "dining" in usrInput.lower() or "dd" in usrInput.lower():
        dollars = digits / .65
    elif "buckid" in usrInput.lower() or "buck" in usrInput.lower():
        dollars = digits
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
                print(f"Order {int(v.x)} {items[index]} for ${int(v.x) * prices[index]}")
            else:
                print(f"Order {int(v.x)} {items[index]}s for ${int(v.x) * prices[index]}")