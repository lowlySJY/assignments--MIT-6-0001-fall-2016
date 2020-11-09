# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 14:28:04 2020

@author: jinyi
"""

annual_salary = float(input("Enter your annual salary: "))
portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
total_cost = float(input("Enter the cost of your dream home: "))

monthly_salary = annual_salary / 12
portion_down_payment = 0.25
current_saving = 0 
r = 0.04       #r is the aunnal rate of investments earn a return
additional_earn_monthly = 0 
num_month = 0
monthly_save = monthly_salary * portion_saved

#investment are computed based on last month saving
while current_saving < (total_cost * portion_down_payment):
    current_saving += monthly_save
    current_saving += additional_earn_monthly
    additional_earn_monthly = current_saving*r/12
    num_month += 1
    
print("Number of months: ", num_month)