# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 15:19:48 2020

@author: jinyi
"""


annual_salary = float(input("Enter your annual salary: "))
portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
total_cost = float(input("Enter the cost of your dream home: "))
semi_annual_raise = float(input("Enter the semiannual raise, as a decimal: "))

monthly_salary = annual_salary / 12
portion_down_payment = 0.25
current_saving = 0 
r = 0.04       #r is the aunnal rate of investments earn a return
additional_earn_monthly = 0 
num_month = 0
monthly_save = monthly_salary * portion_saved


while current_saving < (total_cost * portion_down_payment):
    #investment are computed based on last month saving
    current_saving += monthly_save
    current_saving += additional_earn_monthly
    additional_earn_monthly = current_saving*r/12
    num_month += 1
    #salary will increase every six months 
    if num_month % 6 == 0:
        monthly_save = monthly_save * (1 + semi_annual_raise)
    
print("Number of months: ", num_month)