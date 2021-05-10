from django.test import TestCase
import requests
from walletapp.models import User, Transaction

# Create your tests here.
if __name__ == "__main__":
    user = User()
    user.user_id = "gov_user"
    user.save()
    tran = Transaction()
    tran.uid = "jalkjfdal"
    tran.save()


if __name__ == "__main1__":
    url = "http://127.0.0.1:8000/operation/"
    data = {"name ": "ajay"}
    res = requests.post(url=url, data=data)
    print(res, res.text)

    add_user_data = {"uid": "34422", "fun": "add_user", "id": "daslbkkjda", "host": "localhost:9000",
                     "name": "name is here",
                     "other_detail": "detail is here"}

    contract_id = "address_c3"
    deploy_conract_data = {
        "fun": "deploy_contract",
        "id": "c3",
        "host": "localhost",
        "contract_name": "voting",
        "params": {
            "candidate": ["add1", "add2"
                          ]
        }
    }
    add_voter = {
        "fun": "execute",
        "id": "c3",
        "host": "localhost",
        "contract_name": "voting",
        "contract_id": contract_id,
        "operation": "add_voter",
        "params": {
            "voter_list": ["ajay", "bijay", "ram"]
        }
    }

    start_voting = {
        "uid": "adjkla",
        "fun": "execute",
        "id": "c3",
        "host": "localhost",
        "contract_name": "voting",
        "contract_id": contract_id,
        "operation": "start",
    }

    vote = {
        "uid": "adjkla",
        "fun": "execute",
        "id": "ajay",
        "host": "localhost",
        "contract_name": "voting",
        "contract_id": contract_id,
        "operation": "vote",
        "params": {
            "candidate": "add1",
            "address": "ajay"
        }
    }

    end = {
        "fun": "execute",
        "id": "c3",
        "host": "localhost",
        "contract_name": "voting",
        "contract_id": contract_id,
        "operation": "end",
    }

    winner = {
        "fun": "execute",
        "id": "c3",
        "host": "localhost",
        "contract_name": "voting",
        "contract_id": contract_id,
        "operation": "winner",
    }

    vote_count = {
        "fun": "execute",
        "id": "c3",
        "host": "localhost",
        "contract_name": "voting",
        "contract_id": contract_id,
        "operation": "vote_count",
    }
