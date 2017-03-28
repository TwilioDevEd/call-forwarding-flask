from models import StateSenator, Zip
import json

def senators_from_json(senator_data):
    senators = []
    senators_dict = json.loads(senator_data)
    import pdb; pdb.set_trace()
    for i in senators_dict['state_senators']:
        name = i['name'],
        state = i['state'],
        phone = i['phone']
        senators.append(StateSenator(name=name, state=state, phone_number=phone))
    import pdb; pdb.set_trace()
    return senators
