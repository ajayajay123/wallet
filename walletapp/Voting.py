from enum import Enum


class State(Enum):
    PREPARING = 1
    STARTED = 2
    ENDED = 3


class Voting:

    def __init__(self, developer_address, candidates: list):
        self.developer_address = developer_address
        self.candidates = {}
        for candidate in candidates:
            self.candidates[candidate] = 0
        self.votters = {}
        self.state = State.PREPARING

    def add_right_to_vote(self, my_address, voter_address_list: list):
        if my_address != self.developer_address:
            raise Exception('you are not owner of this contract')
        elif self.state != State.PREPARING:
            raise Exception('state of voting is not preparing')

        result = []
        for voter_address in voter_address_list:
            try:
                result_of_adding = self.add_right_to_vote_single(voter_address)
            except Exception as e:
                result_of_adding = str(e)

            result.append(result_of_adding)
        return result
        pass

    def add_right_to_vote_single(self, voter_address):

        if self.votters.get(voter_address) is not None:
            raise Exception(voter_address+" is already register")
        self.votters[voter_address] = False
        return voter_address + " is register"

    def vote(self, voter_address, candidate_address):
        print("voting to {0} by {1}".format(candidate_address, voter_address))
        if self.state != State.STARTED:
            raise Exception('Voting is not started')
        count_of_candidate = self.candidates.get(candidate_address)
        if count_of_candidate is None:
            raise Exception('Candidate is not valid')
        elif self.votters.get(voter_address) is None or self.votters.get(voter_address):
            raise Exception('Voter is not valid')
        self.candidates[candidate_address] = count_of_candidate + 1
        self.votters[voter_address] = True
        return "success"
        pass

    def start_vote(self, my_address):
        if my_address != self.developer_address:
            raise Exception('permission not allowed')
        elif self.state != State.PREPARING:
            raise Exception('Voting is already stared')
        self.state = State.STARTED
        return "success"
        pass

    def winner_address(self, my_address):
        if my_address != self.developer_address:
            raise Exception('permission not allowed')
        elif self.state != State.ENDED:
            raise Exception('Voting is not ending')
        winner_candidate = ''
        winner_candidate_count = -1
        for candidate in self.candidates:
            count_of_candidate = self.candidates.get(candidate)
            if count_of_candidate > winner_candidate_count:
                winner_candidate = candidate
                winner_candidate_count = count_of_candidate
        return winner_candidate
        pass

    def get_voting_count(self, my_address):
        if my_address != self.developer_address:
            raise Exception('permission not allowed')
        elif self.state != State.ENDED:
            raise Exception('Voting is not ending')

        return self.candidates
        pass

    def end_vote(self, my_address):
        if my_address != self.developer_address:
            raise Exception('permission not allowed')
        elif self.state != State.STARTED:
            raise Exception('Voting is not Started')
        self.state = State.ENDED
        return "success"
        pass


if __name__ == '__main__':
    voting_app = Voting("me", ['ajay', 'bijay', 'sujan', 'siva'])
    print(voting_app.add_right_to_vote("me", ['ram', 'ram']))
