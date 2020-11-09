# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 15:38:41 2020

@author: jinyi
"""



annual_salary = float(input("Enter the starting salary: "))

total_cost = 1000000
semi_annual_raise = .07

high_rate = 10000.0
low_rate = 0

portion_saved = high_rate
monthly_salary = annual_salary / 12
portion_down_payment = 0.25
r = 0.04       #r is the aunnal rate of investments earn a return
additional_earn_monthly = 0 
current_saving = 0
flag = True
step = 0


while abs(current_saving - (total_cost * portion_down_payment)) > 100:
    monthly_save = monthly_salary * portion_saved / 10000   
    current_saving = 0 
    num_month = 0
    
    while current_saving < (total_cost * portion_down_payment):
        #investment are computed based on last month saving
        current_saving += monthly_save
        current_saving += additional_earn_monthly
        additional_earn_monthly = current_saving*r/12
        num_month += 1
        #salary will increase every six months 
        if num_month % 6 == 0:
            monthly_save = monthly_save * (1 + semi_annual_raise)
    #bisection search for saving rate by juding number of months 
    if num_month <= 36:
        high_rate = portion_saved
    elif step == 0 and num_month > 36:
        print("It is not possible to pay the down payment in three years.")
        flag = False
        break
    else:
        low_rate = portion_saved
    
    portion_saved = (high_rate + low_rate) / 2
    step += 1
            
if flag:
    print("Best savings rate: ", portion_saved/10000)    
    print("Steps in bisection search: ", step)
    