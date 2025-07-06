## 1st Step Building a PYDANTIC Model Where we will make our schema
from pydantic import BaseModel

class Paitent(BaseModel): ## Paitent cls ihherit from BaseModel cls
    ## Schema define
    name: str
    age : int


def insert_paitent_data(paitent : Paitent): #Passing the oobject of paitnet cls
    print(paitent.name)
    print(paitent.age)
    print('inserted')


## Intiant the Paitent Model with data

paitent = {'name':"Somrat", 'age':30}

## Create a Paitent object using the Paitent model
paitent1 = Paitent(**paitent) ##Unpacking the dictionary

insert_paitent_data(paitent1)