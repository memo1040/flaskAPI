from mock_data import mock_data

# Dictionary

me = {
    "name": "Guillermo",
    "last": "Monge",
    "age": 32,
    "hobbies": [],
    "address": {
        "street": "Delta",
        "city": "San Diego"
    }
}

print(me["name"])

# print full name
print(me["name"] + " " + me["last"])

# pint city
print(me["address"]["city"])

# modify existing
me["age"] = 34

# create new
me["new"] = 1
print(me)





#list

names = []

names.append("Guillermo")
names.append("Jake")
names.append("Krystle")

print(names)


# get elements
print(names[0])
print(names[2])


# for loop
for name in names:
    print(name)








ages = [12,32,456,10,23,678,4356,2,46,789,23,67,13]


# 1 - youngest
# Create a variable with the first (or any) number from the list
# Travel the list and compare each number with your variable
# If it finds a younger number, update your variable to be that number
# Print the variable

youngest = ages[-1]
for age in ages:
    if age < youngest:
        youngest = age

print(youngest)



# print the title for every product
# travel mock_data list
# get and print the title from the product (dict)

for item in mock_data:
    print(item["title"])