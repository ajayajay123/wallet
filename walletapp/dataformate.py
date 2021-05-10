if __name__ == "__main__":
    add_user_data = {"uid": "34422", "fun": "add_user", "id": "daslbkkjda", "host": "localhost:9000", "name": "name is here",
                     "other_detail": "detail is here"}

    contract_id = "address_c3"
    deploy_contract_data = {
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
