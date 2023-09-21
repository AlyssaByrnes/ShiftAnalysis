import csv
import tabula
import pandas as pd

def read_pdf(filename, pages=1):
    """Read .pdf file"""
    df = tabula.read_pdf(filename, pages='all')
    return df

def get_employee_hours(df: pd.DataFrame) -> dict:
    """Gets each employee's scheduled hours from the data frame"""
    hours = []
    for elem in df:
        # Go through each element of pulled data 
        # to get all columns of employee info
        hours.extend(elem.loc[:,"Unnamed: 0"].tolist())
    # Strip erroneous info from hours
    employee_shifts = []
    for elem in hours:
        if isinstance(elem, str):
            if "\r" in elem:
                employee_shifts.append(elem)
    # Make dictionary
    hours_dict: dict = {}
    for entry in employee_shifts:
        [employee, hrs] = entry.split("\r")
        hrs = hrs.split("/ ")[1]
        hrs = float(hrs.replace("hrs", ""))
        hours_dict[employee] = hrs
    return hours_dict
        

def read_data(filename) -> list:
    """Basic .csv file reader"""
    ret_data = []
    with open(filename, mode ='r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            ret_data.append(lines)
    return ret_data


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

def _lecture_help(name: str, airtable_data: list):
    """Checks if a TA has volunteered for lecture help"""
    header = airtable_data[0]
    
    for record in airtable_data[1:]:
        first_name = record[2]
        last_initial = record[3][0]
        employee_name = first_name + " " + last_initial + "."
        classification = record[-1]
        if name == employee_name:
            if "Lecture" in classification:
                return True
            else:
                return False
        
    print("Error: Employee not found")
    return False

def _get_mail_data(name: str, airtable_data: list, under: int):
    """Gets data of employee for mail merge"""
    header = airtable_data[0]
    
    for record in airtable_data[1:]:
        first_name = record[2]
        last_initial = record[3][0]
        email = record[4]
        employee_name = first_name + " " + last_initial + "."
        classification = record[-1]
        if name == employee_name:
            record = [first_name, email, under]
            return record
        
    print(f"Error: Employee {name} not found")
    return False

def export_under(employees: dict, team_info: list, fname: str):
    with open(fname, 'w') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        for name in employees.keys():
            # If they are short by an hour, ignore
            if not (employees[name] == 1):
                csvwriter.writerow(_get_mail_data(name, team_info, employees[name]))
