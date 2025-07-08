from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str

class Pitent(BaseModel):
    id: int
    name: str
    adress: Address



addresdict = {'street': '123 Main St', 'city': 'Springfield', 'state': 'IL', 'zip_code': '62701'}

adreess1 = Address(**addresdict)

paitentdict = {'id': 1, 'name': 'John Doe', 'adress': adreess1}

paitent1 = Pitent(**paitentdict)

print(paitent1)
print(paitent1.adress.city)

## Serialization
temp = paitent1.model_dump(include={'id', 'name'}) ## make the model into a dict

temp1 = paitent1.model_dump_json() ## make the model into a json string
print(temp)