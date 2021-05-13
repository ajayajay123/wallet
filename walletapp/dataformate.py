if __name__ == "__main__":
    # file = open('/test/dataformate.json')
    # data_formate = json.load(file)
    # print(str(data_formate.get('fun_add_user')))
    # Deploy Add_Voter Start_Voting
    # deploy_contract add_voter start vote end winner vote_count
    add_user_data = {
        "is_wallet": True,
        "uid": "34422fsjn", "fun": "add_user", "id": "daslbkkjda", "host": "localhost:9000", "name": "name is here",
        "other_detail": "detail is here"}

    contract_id = "address_c3"
    deploy_conract_data = {
        "is_wallet": True,
        "uid": "adjkla",
        "fun": "deploy_contract",
        "id": "c4",
        "host": "localhost",
        "contract_name": "voting",
        "params": {
            "candidate": ["add1", "add2"
                          ]
        }
    }
    add_voter = {
        "is_wallet": True,
        "uid": "adjkla",
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
        "is_wallet": True,
        "uid": "adjkla",
        "fun": "execute",
        "id": "c3",
        "host": "localhost",
        "contract_name": "voting",
        "contract_id": contract_id,
        "operation": "start",
    }

    vote = {
        "is_wallet": True,
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
        "is_wallet": True,
        "uid": "adjkla",
        "fun": "execute",
        "id": "c3",
        "host": "localhost",
        "contract_name": "voting",
        "contract_id": contract_id,
        "operation": "end",
    }

    winner = {
        "is_wallet": True,
        "uid": "adjkla",
        "fun": "execute",
        "id": "c3",
        "host": "localhost",
        "contract_name": "voting",
        "contract_id": contract_id,
        "operation": "winner",
    }

    vote_count = {
        "is_wallet": True,
        "uid": "adjkla",
        "fun": "execute",
        "id": "c3",
        "host": "localhost",
        "contract_name": "voting",
        "contract_id": contract_id,
        "operation": "vote_count",
    }
