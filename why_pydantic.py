## 1st Step Building a PYDANTIC Model Where we will make our schema
from pydantic import BaseModel,EmailStr,AnyUrl,Field, field_validator,model_validator,computed_field
from typing import List, Dict,Optional,Annotated
class Paitent(BaseModel): ## Paitent cls ihherit from BaseModel cls
    ## Schema define
    ## By deafault all of these fields are required if dont give them value it will throw an error

    ## We can also add metadata(details about the field) by using Annotated
    name: Annotated[str, Field(max_length=50, title = "Name of the paitent", description = "Paitent name have to less than 50 characters",example=['Somrat'])]
    email: EmailStr ##Emailstr is a type provided by pydantic to validate email format
    age : int
    weight: Annotated[float, Field(gt=0,lt=500, strict=True)]##Field is used to add validation rules, here gt means greater than and lt means less than  
    married : bool = False ## default value is False
    allergies: Optional[List[str]] = None ##have to import list from typing module Optional means this file is not must required and default value is none
    contact_details: Dict[str,str] ##also have to import Dict from typing module
    linkdin_url : AnyUrl  ##AnyUrl is a type provided by pydantic to validate URL format
    height: float


    @field_validator('email')
    @classmethod
    def validate_email(cls,value):
        valid_domains = ['gmail.com', 'yahoo.com', 'outlook.com']
        doamin_name = value.split("@")[-1]
        if doamin_name not in valid_domains:
            raise ValueError(f"Email domain must be one of {valid_domains}")
    
    @field_validator('name')
    @classmethod
    def transorm_name(cls, value):
        return value.upper()
    
    @field_validator('age', mode = 'after') ## typecast the value if its before it will use same value given by user
    @classmethod
    def validate_age(cls, value):
        if 0 < value < 100:
            return value
        else:
            raise ValueError("Age must be between 0 and 100")
        
    @model_validator(mode='after') ## this will run after all the field validators
    @classmethod
    def validate_paitent(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_deatils:
            raise ValueError('Paitent older thean 60 have a must emergency contact') 
        return model

    @computed_field
    @property
    def calculate_bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2),2)
        return bmi

def insert_paitent_data(paitent : Paitent): #Passing the oobject of paitnet cls
    print(paitent.name)
    print(paitent.age)
    print(paitent.married)
    print(paitent.allergies)
    print(paitent.calculate_bmi)
    print('inserted')


## Intiant the Paitent Model with data

paitent = {'name':"Somrat",'email':'abc@gmail.com','height': 1.72,'age':30, 'weight':75.2,'married':True, 
           'allergies':['polen','dust'], 'contact_details':{'email':'abc@gmail.com','phone':'1234563'}
           ,'linkdin_url': 'https://www.linkedin.com/in/somrat/'}

## Create a Paitent object using the Paitent model
paitent1 = Paitent(**paitent) ##Unpacking the dictionary

insert_paitent_data(paitent1)