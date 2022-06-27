import pandas as pd
import warnings
warnings.filterwarnings("ignore")

food_keywords = ["chocolate"]
book_keywords = ["book"]
medical_keywords = ["pills"]

def inputToDf(input):
	item_row = []

	df = pd.DataFrame(columns=['quantity','item','price','sales_tax','import_tax','total'])


	iterable_obj = iter(input.split())
	 
	while True:
	    try:
	        #appending quantity
	        quantity = next(iterable_obj)
	        item_row.append(int(quantity))

	        #appending item name
	        word=""
	        item_name=""
	        while word!="at":
	            item_name=item_name+" "+word
	            word=next(iterable_obj)
	        item_row.append(item_name)

	        price = next(iterable_obj)
	        item_row.append(float(price))

	        df = df.append(pd.DataFrame( [item_row],
	                   columns=['quantity','item','price']),
	                   ignore_index = True)
	        item_row = []
	        continue
	    except StopIteration:
	 
	        # exception will happen when iteration will over
	        break
	return df


def getSalesTax(df):
	for index, row in df.iterrows():
		if (isFood(row["item"]) or isBook(row["item"]) or isMedical(row["item"])):
			df.loc[index,'sales_tax'] = 0
		else:
			df.loc[index,'sales_tax'] = round_nearest(row["price"]*0.1*row["quantity"],0.05)


def isFood(item):
    for key in food_keywords:
        if(key in item):
            return True
    return False

def isBook(item):
    for key in book_keywords:
        if(key in item):
            return True
    return False

def isMedical(item):
    for key in medical_keywords:
        if(key in item):
            return True
    return False

def isImported(item):
    if("imported" in item):
        return True
    return False

def getImportTax(df):
	for index, row in df.iterrows():
		if (isImported(row["item"])):
		    df.loc[index,'import_tax'] = round_nearest(row["price"]*0.05*row["quantity"],0.05)
		else:
		    df.loc[index,'import_tax'] = 0

def getOutputString(df):
    string = ""
    for index, row in df.iterrows():
        string = string + str(row['quantity']) + str(row['item']) + ": " + str(round(row['total'],2)) + " "
    salesTax = df['sales_tax'].sum() + df['import_tax'].sum()
    total = df['total'].sum()
    string = string + "Sales Taxes: " + str(round(salesTax,2)) + " Total: " + str(round(total,2))
    print(string)

def round_nearest(x, a):
    return round(x / a) * a

def main():
	reciept = input("Enter reciept details in a single line: ")

	df=inputToDf(reciept)
	getSalesTax(df)
	getImportTax(df)

	df['total'] = df['quantity'] * df['price'] + df['import_tax'] + df['sales_tax']
	getOutputString(df)


if __name__ == '__main__':
	main()

