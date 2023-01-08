from autoserver import AutoServer
app = AutoServer()

@app.addfunc
def TaxCalc(province: str, cost: float, taxrate: int):
    """
    Computes the amount of tax on an item given the tax rate
    :param province: The name of the province
    :param cost: The cost of the item expressed in dollars
    :param taxrate: The tax rate expressed as a percentage
    :return:
    """
    tax = cost * float(taxrate) / 100
    output = f"The tax in {province} for an item worth ${cost} is {tax}."
    output += f"The total cost is ${cost + tax}."
    return output

@app.addfunc
def TargetPrice(province: str, targetcost: float, taxrate: int):
    targetRatio = 1.0 + float(taxrate) / 100
    output = f"To have a final cost of ${targetcost} in {province},"
    output += f"the pretax price should be ${targetcost / targetRatio}"
    return output

app.run()