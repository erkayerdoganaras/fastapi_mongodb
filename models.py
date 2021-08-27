from mongoengine import Document,StringField,IntField
from pydantic import BaseModel

class Group(Document):
    name=StringField()
    description=StringField()

class Employee(Document):
    id=IntField()
    firstname=StringField()
    lastname=StringField()
    title=StringField()
    salary=IntField()
    group=StringField()
