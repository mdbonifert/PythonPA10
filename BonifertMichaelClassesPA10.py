#####################################################################
#                                                                   #
#   Program Name: BonifertMichaelClassesPA8                         #
#   Description:  Stock Earning Summary For Multiple Stocks         #
#                  Classes                                          #
#   Date:         3/15/2019                                         #
#   Author:       Michael Bonifert                                  #
#                                                                   #
#####################################################################

from datetime import date

# Class for Stock Properties and Methods
class Stock():
	"""This class contains properties and methods for Stock Objects"""
	def __init__(self, purchase_ID, investor_ID, symbol, qty_of_shares,
				 share_price_purchased, share_price_current,
				 purchase_date):
		self.purchase_ID = purchase_ID
		self.investor_ID = investor_ID
		self.symbol = symbol
		self.qty_of_shares = qty_of_shares
		self.share_price_purchased = share_price_purchased
		self.share_price_current = share_price_current
		self.purchase_date = purchase_date
		
	# Function to calculate overall loss/gain.
	def calc_loss_gain(self):
		"""Calculate overall loss/gain based on supplied parameters"""
		stock_value_purchased = self.share_price_purchased * self.qty_of_shares
		stock_value_current = self.share_price_current * self.qty_of_shares
		return round(stock_value_current - stock_value_purchased,2)
		
	# Function to calculate annual earnings/loss.
	def calc_yearly_earnings_loss(self):
		"""Calculate Yearly earnings/loss based on supplied parameters"""
		delta = date.today() - self.purchase_date
		no_of_days = int(delta.days)
		no_of_years = float(no_of_days/365)
		return (((self.share_price_current - self.share_price_purchased)/self.share_price_purchased)/
				no_of_years)*100

# Class for Investor Properties		
class Investor():
	"""This class contains properties for investors"""
	def __init__(self, investor_ID, investor_address,
				 investor_phone_number):
		self.investor_ID = investor_ID
		self.investor_address = investor_address
		self.investor_phone_number = investor_phone_number
		
# Class for Bond Properties and Methods.
class Bond(Stock):
	"""This class has inherited properties and methods from the Stock class"""
	def __init__(self, purchase_ID, investor_ID, symbol, qty_of_shares,
				 share_price_purchased, share_price_current,
				 purchase_date, bond_coupon, bond_yield):		
		super().__init__ (purchase_ID, investor_ID, symbol, qty_of_shares,
				 share_price_purchased, share_price_current,
				 purchase_date)
		self.bond_coupon = bond_coupon
		self.bond_yield = bond_yield		
