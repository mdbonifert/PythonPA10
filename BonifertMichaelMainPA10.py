#####################################################################
#                                                                   #
#   Program Name: BonifertMichaelMainPA10                           #
#   Description:  Stock Earning Summary For Multiple Stocks         #
#                  Mainline                                         #
#   Date:         3/15/2019                                          #
#   Author:       Michael Bonifert                                  #
#                                                                   #
#####################################################################

# Import Classes, Date function, sqlite3, JSON, and Matplotlib pyplot.
from BonifertMichaelClassesPA10 import *
#from datetime import date
import datetime as dt
import sqlite3
import json

import matplotlib.pyplot as plt

import matplotlib.dates as mdates

import matplotlib.pyplot as plt; plt.rcdefaults()

import numpy as np

# Function that prints a report line.
def printline(section):
	
	if (section == 'STOCK'):
		max_len = 5
	else:
		max_len = 7
	
	blanks_len = max_len - len(symbol_value)	
	report_line = symbol_value
	if (blanks_len > 0):
		report_line += blanks[:blanks_len]
	if (section == 'STOCK'):
		report_line += "                  "
	else:
		report_line += "                "
	
	blanks_len = 3 - len(str(qty_of_shares_value))	
	if (blanks_len > 0):
		report_line += blanks[:blanks_len]
	report_line += str(qty_of_shares_value)
		
	if (((earnings_loss < 10000) and (earnings_loss >= 0)) or 
		((earnings_loss < -99) and (earnings_loss > -1000))):
		report_line += " "
	if ((earnings_loss > 0) and (earnings_loss < 10)):
		report_line += "   "				
	report_line += "                 $"
	report_line += str(format(earnings_loss, '.2f'))
	
	report_line += "                "
	if ((yearly_earnings_loss > 0) and (yearly_earnings_loss < 10)):
		report_line += "  "
	elif ((yearly_earnings_loss >= 10) or 
		 ((yearly_earnings_loss < 0) and (yearly_earnings_loss > -10))):
		report_line += " "
	report_line += str(format(yearly_earnings_loss, '.2f'))
	report_line += "%"
	
	output_list.append(report_line)

# Function that converts a MM/DD/YYYY string to a Date Object.
def date_convert(mmddyyyy):
	mmddyyyy_list = mmddyyyy.split('/')
	counter = 0
	for date_component in mmddyyyy_list:
		if (counter == 0):
			mm = int(date_component)
		elif (counter == 1):
			dd = int(date_component)
		elif (counter == 2):
			yyyy = int(date_component)
		counter += 1
	return dt.date(yyyy,mm,dd)

# Function that converts a MM/DD/YYYY string to a YYYYMMDD string
def date_convert_to_str(mmddyyyy):
	mmddyyyy_list = mmddyyyy.split('/')
	counter = 0
	for date_component in mmddyyyy_list:
		if (counter == 0):
			mm = int(date_component)
		elif (counter == 1):
			dd = int(date_component)
		elif (counter == 2):
			yyyy = int(date_component)
		counter += 1
	result = (yyyy * 10000) + (mm * 100) + dd
	return str(result)

# Function that converts a YYYYMMDD int date to a date object.
def date_convert_int_to_date(yyyymmdd_int):
	yyyymmdd_str = str(yyyymmdd_int)
	yyyy = int(yyyymmdd_str[:4])
	mm   = int(yyyymmdd_str[4:6])
	dd   = int(yyyymmdd_str[6:])
	return dt.date(yyyy,mm,dd)

# Function that creates the Stock, Bond, and Investor tables
def create_tables(dbPath):
	
	print("Creating the Stock, Bond, and Investor Tables.")
	
	try:
		
		sql_create_stock_table = """CREATE TABLE IF NOT EXISTS Stock (
			PurchaseId	INTEGER NOT NULL UNIQUE,
			InvestorId	INTEGER NOT NULL,
			Symbol		TEXT NOT NULL,
			QtyOfShares	INTEGER NOT NULL,
			SharePricePurchased	REAL NOT NULL,
			SharePriceCurrent	REAL NOT NULL,
			PurchaseDate	NUMERIC NOT NULL,
			PRIMARY KEY(PurchaseId)
			);"""
		
		sql_create_bond_table = """CREATE TABLE IF NOT EXISTS Bond (
			PurchaseId	INTEGER NOT NULL UNIQUE,
			InvestorId	INTEGER NOT NULL,
			Symbol		TEXT NOT NULL,
			QtyOfShares	INTEGER NOT NULL,
			SharePricePurchased	REAL NOT NULL,
			SharePriceCurrent	REAL NOT NULL,
			PurchaseDate	NUMERIC NOT NULL,
			BondCoupon  REAL NOT NULL,
			BondYield   REAL NOT NULL,
			PRIMARY KEY(PurchaseId)
			);"""
		
		sql_create_investor_table = """CREATE TABLE IF NOT EXISTS Investor (
			InvestorId	INTEGER NOT NULL,
			Address		TEXT NOT NULL,
			PhoneNumber TEXT NOT NULL,
			PRIMARY KEY(InvestorId)
			);"""
			
		# Purge-Table logic in case tables already exist with data.
		sql_purge_stock_table = """DELETE FROM Stock;"""
		sql_purge_bond_table  = """DELETE FROM Bond;"""
		sql_purge_investor_table = """DELETE FROM Investor;"""
		
		connection = sqlite3.connect(dbPath)
		cursor	=	connection.cursor()
		cursor.execute(sql_create_stock_table)
		cursor.execute(sql_create_bond_table)
		cursor.execute(sql_create_investor_table)
		cursor.execute(sql_purge_stock_table)
		cursor.execute(sql_purge_bond_table)
		cursor.execute(sql_purge_investor_table)
		connection.commit()	
		connection.close()
		
	except:
		msg = """Sorry, there was a problem creating or purging the Stock,
		Bond, or Investor tables in database""" + dbPath
		print(msg)

# Function that Writes data to a supplied table.	
def write_to_table(dbPath, fileName, lineList, lineItemTypes):
	try:
		idx = 0
		sqlStmt = "INSERT INTO " + fileName + " VALUES("
		for lineItem in lineList:
			
			if (lineItemTypes[idx] == "STR"):
				sqlStmt += "'"
				sqlStmt += lineItem
				sqlStmt += "'"
			elif (lineItemTypes[idx] == "FLT"):
				sqlStmt += str(lineItem)
			elif (lineItemTypes[idx] == "INT"):
				sqlStmt += str(lineItem)
			elif (lineItemTypes[idx] == "DAT"):
				sqlStmt += str(date_convert_to_str(lineItem))
		
			if (lineItem != lineList[-1]):
				sqlStmt += ", "
			else:
				sqlStmt += ")"
				
			idx += 1
		
		connection = sqlite3.connect(dbPath)
		cursor	=	connection.cursor()
		cursor.execute(sqlStmt)
		connection.commit()	
		connection.close()
	except:
		msg = "Sorry, there was a problem writing " + lineList + " to table "
		+ fileName + " in database " + dbPath
		print(msg)
	
	
# Function that reads data from a supplied table and instantiates
#  objects from the corresponding class in a dictionary.
def read_from_table(dbPath, fileName):
	try:
		sqlStmt = "SELECT * FROM " + fileName + ";"
		connection = sqlite3.connect(dbPath)
		cursor	=	connection.cursor()
		objidx = 0
		for record in cursor.execute(sqlStmt):
			if (fileName == "Stock"):
				date_obj = date_convert_int_to_date(record[6])
				stock_obj = Stock(record[0], record[1], record[2], record[3],
								record[4], record[5], date_obj)
				key = "stock_object" + str(objidx)
				stock_object_dict[key] = stock_obj
			elif (fileName == "Bond"):
				date_obj = date_convert_int_to_date(record[6])
				bond_obj = Bond(record[0], record[1], record[2], record[3],
								record[4], record[5], date_obj, record[7],
								record[8])
				key = "bond_object" + str(objidx)
				bond_object_dict[key] = bond_obj
			elif (fileName == "Investor"):
				investor_obj = Investor(record[0], record[1], record[2])
				key = "investor_object" + str(objidx)
				investor_object_dict[key] = investor_obj
			objidx += 1
		connection.close()
	except:
		msg = "Sorry, there was a problem reading table "
		+ fileName + " in database " + dbPath
		print(msg)
	
		
# Function to delete the Stock, Bond, and Investor Tables.		
def delete_tables(dbPath):
	
	print("Deleting the Stock, Bond, and Investor Tables.")
	
	try:
		sql_delete_stock_table = """DROP TABLE Stock;"""
		
		sql_delete_bond_table = """DROP TABLE Bond;"""
		
		sql_delete_investor_table = """DROP TABLE Investor;"""
		
		connection = sqlite3.connect(dbPath)
		cursor	=	connection.cursor()
		cursor.execute(sql_delete_stock_table)
		cursor.execute(sql_delete_bond_table)
		cursor.execute(sql_delete_investor_table)
		connection.commit()	
		connection.close()
	except:
		msg = """Sorry, there was a problem deleting the Stock,
		Bond, or Investor tables in database""" + dbPath
		print(msg)


# Retrieve the current directory path (Database and JSON files).
dir_path = "PA7.db"
print("The current database is " + dir_path)

json_path = "AllStocks.json"
print("The current json file is " + json_path)

# Create three tables for Stock, Bond, and Investor within the directory path.
create_tables(dir_path)


# Create/load lists for line-item types corresponding to the three
#  table layouts.
line_item_types_stock = ['INT', 'INT', 'STR', 'INT', 'FLT', 'FLT', 'DAT']
line_item_types_bond  = ['INT', 'INT', 'STR', 'INT', 'FLT', 'FLT', 'DAT',
						 'FLT', 'FLT']
line_item_types_investor = ['INT', 'STR', 'STR']


# Create a list of input values for the Investor Table Row.
investor_row_list = ["123 Sesame Street, Queens, NY 10001",
				 "999-123-4567"]

# Create a list for the report output.
output_list = []

# Create/load File-Name variables.
stock_input_file = 'Lesson6_Data_Stocks.csv'
bond_input_file = 'Lesson6_Data_Bonds.csv'
output_file = 'Report.txt'

# Create/load Table-Name variables.
stock_table = 'Stock'
bond_table = 'Bond'
investor_table = 'Investor'

# Create/load Investor Id variable
investor_id = 0


# Load the Stock table with input from the Stock CSV File.
purchase_id = 0

print("Loading the Stock table.")

try:
	with open(stock_input_file) as file_object:
		for line in file_object:
			if ('SYMBOL' not in line):
				line_list = line.split(',')
				line_list.insert(0, investor_id)
				line_list.insert(0, purchase_id)
				write_to_table(dir_path, stock_table, line_list, 
					line_item_types_stock)
				
				purchase_id += 1
				
except FileNotFoundError:
	msg = "Sorry, the file " + stock_input_file + " does not exist."
	print(msg)

# Load the Investor Table.
print("Loading the Investor Table.")
investor_row_list.insert(0, investor_id)
write_to_table(dir_path, investor_table, investor_row_list,
		line_item_types_investor)

# Define variables for a string of blanks and a length of blanks.
blanks = "       "
blanks_len = 0

# Create empty dictionaries for stock, bond, and investor objects.
stock_object_dict = {}
bond_object_dict = {}
investor_object_dict = {}


# Set the user name to Bob Smith.
user_name = "Bob Smith"


# Load the Bond table with input from the CSV file.
purchase_id = 0
print("Loading the Bond table.")
try:
	with open(bond_input_file) as file_object:
		for line in file_object:
			if ('SYMBOL' not in line):
				line_list = line.split(',')
				line_list.insert(0, investor_id)
				line_list.insert(0, purchase_id)
				write_to_table(dir_path, bond_table, line_list, 
					line_item_types_bond)
				
				purchase_id += 1

except FileNotFoundError:
	msg = "Sorry, the file " + bond_input_file + " does not exist."
	print(msg)

# Read from the three tables and instantiate class objects.
print("Reading Data from the Stock, Bond, and Investor Tables.")
read_from_table(dir_path, stock_table)
read_from_table(dir_path, bond_table)
read_from_table(dir_path, investor_table)

# Retrieve Instantiated Objects for Bond and Investor.
key = "bond_object" + str(0)
bond_obj = bond_object_dict[key]

key = "investor_object" + str(0)
investor_obj = investor_object_dict[key]


# Load data from JSON file into a dataset.
print("Loading Data from JSON File.")
with open(json_path) as f:
	dataSet = json.load(f) 

# Generate lists from the JSON dataset.
print("Generating lists from the JSON dataset.")
symbols_list = []
dates_list = []
opens_list = []
highs_list = []
lows_list = []
closes_list = []
volumes_list = []
for item in dataSet:
	symbols_list.append(item['Symbol'])
	dates_list.append(dt.datetime.strptime(item['Date'], '%d-%b-%y').date())
	opens_list.append(item['Open'])
	highs_list.append(item['High'])
	lows_list.append(item['Low'])
	closes_list.append(item['Close'])
	volumes_list.append(item['Volume'])

# Extract unique stock symbols into a separate list.
unique_symbols_list = list(set(symbols_list))
unique_symbols_list.sort()

# Construct a dictionary with two key/value entries for each unique symbol,
#  one for a list of dates and one for a list of closing prices.
print("Building dictionary for line graph.")
symbols_dates_prices_dict = {}

for ss in unique_symbols_list:
	ssdates = []
	ssprices = []
	keydates = ss + '_DATES'
	keyprices = ss + '_PRICES'
	for i in range(len(symbols_list)):
		if (ss == symbols_list[i]):
			ssdates.append(dates_list[i])
			ssprices.append(float(closes_list[i]))
	symbols_dates_prices_dict[keydates] = ssdates
	symbols_dates_prices_dict[keyprices] = ssprices
	
# Plot the dates/prices for each unique stock symbol.
print("Plotting the dates/prices for each stock symbol.")
for ss in unique_symbols_list:
	keydates = ss + '_DATES'
	keyprices = ss + '_PRICES'
	ssdates = symbols_dates_prices_dict[keydates]
	ssprices = symbols_dates_prices_dict[keyprices]
	plt.plot(ssdates, ssprices, label = ss)

		
# Generate a Stock line graph with dates on the x-axis, stock prices 
#   on the y-axis, and one line for each stock symbol.
print("Generating line graph.")
fmt = mdates.DateFormatter('%b %y')
X = plt.gca().xaxis
X.set_major_formatter(fmt)

plt.xlabel('Dates')
plt.ylabel('Closing Prices')
plt.xticks(rotation=45)
plt.title('Stock Line Graph')

plt.legend()
plt.savefig('stocklinegraph.png', bbox_inches = "tight")
plt.clf()
plt.close('all')

# Generate a portfolio total value list by date.

# Extract unique dates into a separate list and sort it in ascending order.
print("Generating list of unique dates.")
unique_dates_list = list(set(dates_list))
unique_dates_list.sort()

# Create and load a new list to store closing prices for each unique date.
print("Storing closing prices for each unique date.")
closing_prices_for_each_unique_date_list = []
for dtobj in unique_dates_list:
	closing_price_total = 0.0
	for i in range(len(dates_list)):
		if (dtobj == dates_list[i]):
			closing_price_total += float(closes_list[i])
	closing_prices_for_each_unique_date_list.append(closing_price_total)

# Create a histogram graph for the portfolio total value list.
print("Generating Histogram.")
fmt = mdates.DateFormatter('%b %y')
X = plt.gca().xaxis
X.set_major_formatter(fmt)

plt.xlabel('Dates')
plt.ylabel('Closing Prices')
plt.title('Portfolio Total Value List By Date Histogram')

y_pos = np.arange(len(unique_dates_list))
closing_prices_for_each_unique_date_list.sort(reverse=True)

plt.bar(y_pos, closing_prices_for_each_unique_date_list, align='center', alpha=0.5)
plt.xticks(y_pos, unique_dates_list)


plt.savefig('stockhistogram.png', bbox_inches = "tight")
plt.clf()
plt.close('all')



# Create a pie chart for value distribution of stocks in the portfolio.
print("Generating Pie Chart.")

# Generate a list of final closing prices for each unique stock symbol.
final_closing_prices_list = []
for ss in unique_symbols_list:
	keydates = ss + '_DATES'
	keyprices = ss + '_PRICES'
	ssdates = symbols_dates_prices_dict[keydates]
	ssprices = symbols_dates_prices_dict[keyprices]
	final_closing_prices_list.append(ssprices[0])

# Sum all closing prices in the list.
sum_closing_prices = sum(final_closing_prices_list)

# Now calculate a percentage of the sum of all closing prices for each
#  stock symbol's closing price in the list.
final_closing_prices_percentages_list = []
for fcp in final_closing_prices_list:
	final_closing_prices_percentages_list.append(float(fcp/sum_closing_prices))
	
# Plot the Data.
labels = unique_symbols_list
sizes = final_closing_prices_list
colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'grey']
patches, texts = plt.pie(sizes, colors=colors, shadow=True, startangle=90)
plt.legend(patches, labels, loc="best")
plt.axis('equal')	
plt.title('Portfolio Closing Prices By Stock Symbol Pie Chart')

plt.savefig('stockpiechart.png', bbox_inches = "tight")
plt.clf()
plt.close('all')




print("Printing the report to a text file.")

# Output the user name and stock section headings.
output_list.append("\n")
output_list.append("Stock ownership for: " + user_name + "\n")
output_list.append("----------------------------------------------------" +
	  "---------------------------------\n")
output_list.append("STOCK               SHARE NO.             EARNINGS/LOSS" + 
	  "          YEARLY EARNING/LOSS\n")
output_list.append("----------------------------------------------------" +
	  "---------------------------------\n")

# For each stock object, calculate the overall earnings/loss and yearly
#  earnings/loss by executing the appropriate functions. Then output a
#  line displaying the list-item stock symbol, number of shares, overall
#  earnings/loss, and yearly earnings/loss utilizing substrings of the
#  'blanks' variable to evenly space the column values.
section = 'STOCK'
for line_number in range(len(stock_object_dict)):
	key = "stock_object" + str(line_number)
	stock_obj = stock_object_dict[key]
	
	symbol_value = stock_obj.symbol
	qty_of_shares_value = stock_obj.qty_of_shares
	share_price_purchased_value = stock_obj.share_price_purchased
	share_price_current_value = stock_obj.share_price_current
	purchase_date_current_value = stock_obj.purchase_date
	
	earnings_loss = stock_obj.calc_loss_gain()
		
	yearly_earnings_loss = stock_obj.calc_yearly_earnings_loss()
		
	printline(section)
	
	
# Space Down Two Lines and then output the Bond Section Headings.
output_list.append("\n\n")
output_list.append("Bond ownership for: " + user_name + "\n")
output_list.append("----------------------------------------------------" +
	  "---------------------------------\n")
output_list.append("BOND                SHARE NO.             EARNINGS/LOSS" + 
	  "          YEARLY EARNING/LOSS\n")
output_list.append("----------------------------------------------------" +
	  "---------------------------------\n")

# For the bond object, calculate the overall earnings/loss and yearly
#  earnings/loss by executing the appropriate functions. Then output a
#  line displaying the bond symbol, number of shares, overall
#  earnings/loss, and yearly earnings/loss utilizing substrings of the
#  'blanks' variable to evenly space the column values.
symbol_value = bond_obj.symbol
qty_of_shares_value = bond_obj.qty_of_shares
share_price_purchased_value = bond_obj.share_price_purchased
share_price_current_value = bond_obj.share_price_current
purchase_date_current_value = bond_obj.purchase_date
	
earnings_loss = bond_obj.calc_loss_gain()
		
yearly_earnings_loss = bond_obj.calc_yearly_earnings_loss()

section = 'BOND'
printline(section)

# Write all output-list lines to the output file.
try:
	with open(output_file, 'w') as file_object:
		for line in output_list:
			file_object.write(line + '\n')
			
except IOError:
	msg = "Sorry, the file " + output_file + " cannot be opened for writing."
	print(msg)


# Delete the three Database Tables.
delete_tables(dir_path)
