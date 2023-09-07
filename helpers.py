import csv

def read_data(filename) -> list:
    """Basic .csv file reader"""
    ret_data = []
    with open(filename, mode ='r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            ret_data.append(lines)
    return ret_data

def get_schedules(weekdays: list, schedule_data: list) -> dict[str,list]:
    """Take the .csv data and make it into a readable dict"""
    schedules: dict[str,list] = {}
    key = "x"
    schedules["x"] = list()
    for line in schedule_data:
        
        if len(line[0]) != 0: 
            #This means it's starting a new record for an employee
            key = line[0]
            
    return schedules

"""
def get_schedules(weekdays: list, schedule_data: list) -> dict[str,list]:
    
    schedules: dict[str,list] = {}
    key = "x"
    schedules["x"] = list()
    for line in schedule_data:
        weekday = str(line)
        if len(line[0]) != 0: 
            #This means it's starting a new record for an employee
            key = line[0]
            if '\n' in key:
                key = key.split('\n')[0]
            schedules[key] = list()
        if not ("Monday" in weekday):
            for day in range(1, len(line)-1):
                if len(line[day]) != 0:
                    shift_day: str = weekdays[day]
                    shift_time: str = line[day]
                    schedules[key].append(shift_day + ";" + shift_time)
    return schedules
"""

def get_weekly_hours(airtable_data: list):
    """Get a dict with each TA's name and weekly hours"""
    header = airtable_data[0]
    employee_hours: dict = {}
    for record in airtable_data[1:]:
        first_name = record[2]
        last_initial = record[3][0]
        employee_name = first_name + " " + last_initial + "."
        weekly_hours = int(record[1])
        employee_hours[employee_name] = weekly_hours
    return employee_hours