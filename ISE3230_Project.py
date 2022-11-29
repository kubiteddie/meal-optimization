import gurobipy as gp
from gurobipy import GRB
import re
import sys

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

    #"Burger", 5.31
    #"Chicken", 3.84
    #"Drink", 1.63
    items = ["Burger", "Chicken", "Drink"]
    prices = [5.31, 3.84, 1.62]

    x = m.addVars(3, vtype=GRB.INTEGER, name="x")

    sum = 5.31*x[0] + 3.84*x[1] + 1.62*x[2]

    m.setObjective(sum, GRB.MAXIMIZE)

    m.addConstr(5.31*x[0] + 3.84*x[1] + 1.62*x[2] <= dollars)
    m.addConstr(x[0] >= 0)
    m.addConstr(x[1] >= 0)
    m.addConstr(x[2] >= 0)

    m.optimize()

    print(f"The optimal use of your money will cost ${round(m.objVal, 2)}, leaving you with ${round(dollars - m.objVal, 2)} left over.")

    for v in m.getVars():
        index = int(v.varName[2])
        if v.x == 1:
            print(f"Order {int(v.x)} {items[index]} for ${int(v.x) * prices[index]}")
        else:
            print(f"Order {int(v.x)} {items[index]}s for ${int(v.x) * prices[index]}")