'''9. Take electricity units as input and print:
   - "Low usage" if units <= 100
   - "Medium usage" if units between 101 and 300
   - "High usage" if units > 300
'''

electricity_units = float(input("Enter the units consumed: "))
if electricity_units <= 100:
    print("Household has low usage")
elif electricity_units > 100 and electricity_units < 300:
    print("Household has medium usage")
elif electricity_units > 300:
    print("Household has high usage")
    
