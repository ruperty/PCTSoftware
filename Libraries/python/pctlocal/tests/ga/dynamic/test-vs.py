import json

items = json.loads('[{"id":1, "text": "Item 1"}, {"id":2, "text": "Item 2"}]')

for item in items:
    print(item['id'])

def greet(greeting, name):
    """[summary]

    Args:
        greeting ([type]): [description]
        name ([type]): [description]

    Returns:
        [type]: [description]
    """

    return f'{greeting} {name}'


print(greet('hello', 'world'))