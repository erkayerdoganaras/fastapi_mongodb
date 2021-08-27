from fastapi import FastAPI, Path, Query, HTTPException, status
from models import Group, Employee
from mongoengine import *
from pydantic import BaseModel
from typing import Optional
import json


class NewEmployee(BaseModel):
    id : int
    firstname : str
    lastname :str
    title : str
    salary : int
    group : str

class NewGroup(BaseModel):
    name = str()
    description = str()

app = FastAPI()

connect(db="company", host="localhost", port=27017)

"""
groups=Group.objects().to_json()
group_list=json.loads(groups)

print(group_list[0]["name"])
print(len(group_list))
for i in range(0,len(group_list)):
    print(group_list[i]["name"])

names_list=[]
for i in range(0, len(group_list)):
    names_list.append(group_list[i]["name"])

print(names_list)


employees = Employee.objects().to_json()
employees_list = json.loads(employees)
salary=0
for i in range(0, len(employees_list)):
    salary += employees_list[i]["salary"]
print(salary)

employees = Employee.objects().to_json()
employees_list = json.loads(employees)
sırala=[]
for i in range(0, len(employees_list)):
    if i==0:
        sırala.append(employees_list[i]["salary"])

print(sorted(employees_list, key = lambda i: i['salary']))
"""
#ORGANIZATION DETAILS FAILED BECAUSE OF DATABASE PROBLEMS
"""
@app.get("/org")
def org_details():
    try:
        orgs = json.loads(Organization.objects().to_json)
        return {"organization":orgs}
    except:
        return HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED,detail="Failed to show details of organizaton")
"""

@app.get("/get_all_employees")
def get_all_employees():
    try:
        employees = Employee.objects().to_json()
        employees_list = json.loads(employees)
        return {"employees": employees_list}
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee file not found")

@app.get("/org/groups")
def list_all_groups():
    groups = Group.objects().to_json()
    group_list = json.loads(groups)
    names_list=[]
    try:
        for i in range(0, len(group_list)):
            names_list.append(group_list[i]["name"])
        return names_list
    except:
        raise HTTPException(status_code=not status, detail="Function is not working")

@app.get("/org/groups/{group_name}")
def group_details(group_name: str):
    groups = Group.objects().to_json()
    group_list = json.loads(groups)
    try:
        for i in range(0, len(group_list)):
            if(group_list[i]["name"])==group_name:
                return group_list[i]["description"]
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group Name Not Found")



@app.get("/org/groups/{group_name}/employees")
def employees_in_group(group_name: str):
    try:
        employees = Employee.objects().to_json()
        employees_list = json.loads(employees)
        gr_emp_list_names=[]
        gr_emp_list_lnames = []
        for i in range(0, len(employees_list)):
            if(employees_list[i]["group"])==group_name:
                gr_emp_list_names.append(employees_list[i]["firstname"])
                gr_emp_list_lnames.append(employees_list[i]["lastname"])
        return zip(gr_emp_list_names,gr_emp_list_lnames)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group name not found so the employees")


@app.get("/org/groups/{group_name}/employees/{id}")
def employees_in_group(*,group_name: Optional[str]=None, id:int):
    try:
        employees = Employee.objects().to_json()
        employees_list = json.loads(employees)
        for i in range(0, len(employees_list)):
            if(employees_list[i]["id"])==id:
                return employees_list[i]
    except:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Invalid id input")

@app.get("/org/average-salary")
def average_salary():
    try:
        employees = Employee.objects().to_json()
        employees_list = json.loads(employees)
        salary= 0
        for i in range(0, len(employees_list)):
            salary+= employees_list[i]["salary"]
        return "Average Salary in this company is : {}".format(int(salary/len(employees_list)))
    except:
        raise HTTPException(status_code=status.WS_1004_NO_STATUS_RCVD)


@app.get("/org/groups/{group_name}/average-salary")
def group_average_salary(group_name:str):
    try:
        employees = Employee.objects().to_json()
        employees_list = json.loads(employees)
        salary=0
        counter=0
        for i in range(0, len(employees_list)):
            if(employees_list[i]["group"])==group_name:
                salary+=employees_list[i]["salary"]
                counter+=1
        return "Average salary of {} group is {}".format(group_name,int(salary/counter))
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group Name Not Found")

"""
@app.get("/org/sort")
def sorting_salary():
    employees = Employee.objects().to_json()
    employees_list = json.loads(employees)
    return (sorted(employees_list, key = lambda i: i['salary'],reverse=True))
"""



@app.get("/org/sort")
def sorting_salary_by_x(title:str=Query(None)):
    try:
        employees = Employee.objects().to_json()
        employees_list = json.loads(employees)
        grup=[]
        if title!=None:
            for i in range(0, len(employees_list)):
                if(employees_list[i]["title"])==title:
                    grup.append(employees_list[i])
            return (sorted(grup, key = lambda i: i['salary'],reverse=True))
        else: return (sorted(employees_list, key = lambda i: i['salary'],reverse=True))
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Title not found")



@app.post("/org/groups")
def add_new_group(group: NewGroup):
    try:
        new_group = Group(name= group.name,
                          description= group.description)
        new_group.save()
        return {"message" : "New group has been created and added"}
    except:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED, detail="Group could not created")


@app.post("/org/groups/{group_name}/employees")
def add_new_employee(employee: NewEmployee,group_name=str):
    try:
        new_employee = Employee(firstname=employee.firstname,
                                lastname=employee.lastname,
                                title=employee.title,
                                salary=employee.salary,
                                group=employee.group)
        new_employee.group=group_name
        new_employee.save()
        return {"message":"New Employee has been added succesfully","group":new_employee.group}
    except:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Try again")

holder=[]
@app.delete("/org/groups/{group_name}/employees/{id}")
def delete_employee(id:int,group_name=Path(...)):
    employees = Employee.objects().to_json()
    employees_list = json.loads(employees)
    try:
        if id<=len(employees_list)and (id not in counter):
            Employee.objects(id=id).delete()
            holder.append(id)
            return "Employee with id:{} has been deleted".format(id)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee with id {} not found".format(id))

