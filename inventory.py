# BEFORE: import json
# BEFORE: import logging  # <-- Unused import (FIXED: removed)
import json
from datetime import datetime

stock_data = {}

# BEFORE: def addItem(item="default", qty=0, logs=[]):  # <-- Mutable default argument (PROBLEM)
def addItem(item="default", qty=0, logs=None):  # <-- FIXED: Changed to None
    if logs is None:  # <-- FIXED: Initialize empty list inside function
        logs = []
    # BEFORE: # No initialization needed (logs=[] was shared across calls)
    if not item:
        return
    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append("%s: Added %d of %s" % (str(datetime.now()), qty, item))

def removeItem(item, qty):
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    # BEFORE: except:  # <-- Bare except clause (PROBLEM: catches all exceptions)
    # BEFORE:     pass  # <-- Silent failure (PROBLEM: no error handling)
    except KeyError:  # <-- FIXED: Specific exception handling
        print(f"Item '{item}' not found in inventory")  # <-- FIXED: Informative error message

def getQty(item):
    return stock_data[item]

def loadData(file="inventory.json"):
    # BEFORE: f = open(file, "r")  # <-- Unsafe file operation (PROBLEM: no context manager)
    # BEFORE: global stock_data
    # BEFORE: stock_data = json.loads(f.read())
    # BEFORE: f.close()  # <-- Manual file closing (PROBLEM: might not close if exception occurs)
    with open(file, "r", encoding='utf-8') as f:  # <-- FIXED: Context manager with encoding
        global stock_data
        stock_data = json.loads(f.read())

def saveData(file="inventory.json"):
    # BEFORE: f = open(file, "w")  # <-- Unsafe file operation (PROBLEM: no context manager)
    # BEFORE: f.write(json.dumps(stock_data))
    # BEFORE: f.close()  # <-- Manual file closing (PROBLEM: might not close if exception occurs)
    with open(file, "w", encoding='utf-8') as f:  # <-- FIXED: Context manager with encoding
        f.write(json.dumps(stock_data))

def printData():
    print("Items Report")
    for i in stock_data:
        print(i, "->", stock_data[i])

def checkLowItems(threshold=5):
    result = []
    for i in stock_data:
        if stock_data[i] < threshold:
            result.append(i)
    return result

def main():
    addItem("apple", 10)
    addItem("banana", -2)
    addItem(123, "ten")
    removeItem("apple", 3)
    removeItem("orange", 1)
    print("Apple stock:", getQty("apple"))
    print("Low items:", checkLowItems())
    saveData()
    loadData()
    printData()
    # BEFORE: eval("print('eval used')")  # <-- Security vulnerability (PROBLEM: can execute arbitrary code)
    print('eval used')  # <-- FIXED: Direct print statement (safe)

main()
