from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .interface import wallet_pb2, wallet_pb2_grpc
import grpc, json, random
import time
from .models import User, Transaction, Contract
from .forms import Login
from hashlib import md5
import traceback
from .Voting import Voting

address = "localhost:9000"
user_session = {"test": "gov_user"}
user_session_rev = {}
node_certificate = {}
user_key = {}

user = []
contract = {}


def get_client(wallet_address) -> wallet_pb2_grpc.WalletStub:
    channel = grpc.insecure_channel(wallet_address)
    stub = wallet_pb2_grpc.WalletStub(channel=channel)
    return stub


# Create your views here.

def generate_tocken():
    return md5(str(random.random()).encode()).hexdigest()


def home(request):
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            user_id = form.cleaned_data['user_id']
            password = form.cleaned_data['user_id']

        return HttpResponse("okay")
        pass
    else:
        form = Login()
        return render(request, './old-index.html', {'form': form})


def dashboard(request):
    token = request.COOKIES['token']
    user_type = [False, False, False]
    # index = user_session[token].get("user_type")
    user_id = user_session['test']
    user = User.objects.filter(user_id=user_id).first()
    if user is None:
        return HttpResponse("User not found")
    index = user.user_type
    user_type[index - 1] = True
    if index == 1:
        contract: Contract = Contract.objects.filter(user=user)
        return render(request, './dashboard.html', {'contract': contract, 'g': True})
    return render(request, './dashboard.html', {'g': user_type[0], 'r': user_type[1], 'n': user_type[2]})


def operation(request):
    return render(request, './old-index.html')


@api_view(['POST', 'GET'])
def home_api(request):
    try:
        data = request.data
        print("data is ", data)
        user = User.objects.filter(user_id=data.get('user_id'), password=data.get('password')).first()
        if user is None:
            return Response({"msg": "invalid username or password"})
        session = generate_tocken()
        prev_session = user_session_rev.get(user.user_id)
        if prev_session is not None:
            del user_session[prev_session]
        user_session[session] = {"user_id": user.user_id, "user_type": user.user_type}
        user_session_rev[user.user_id] = session
        return Response({"tocken": session})
    except Exception as exe:
        print(exe)
        return Response({"msg": "Incorect Data"})
    pass


@api_view(['POST'])
def get_key_api(request):
    data = request.data
    want_key = data.get('key')
    key = generate_tocken()
    print("data is ", data)
    if want_key == "add_user":
        user_key[key] = 3
        return Response({"key": key})
    return Response({"msg": "error"})
    pass


@api_view(['POST'])
def operation_api(request):
    data = request.data
    res = gen_fun(data)
    return Response(res)
    pass


def gen_fun(data):
    data = {'fun': 'deploy_contract', 'name': 'afasa', 'contract_list': ['afda', 'adfad', 'fdfdf']}
    fun = data.get('fun')
    print("gen_fun ", data)
    try:
        if fun == "add_user":
            res = add_user(data)
            pass
        elif fun == "deploy_contract":
            res = deploy_contract(data)
            return {"msg": res}
        elif fun == "execute":
            sub_operation = data.get('operation')
            if sub_operation == "add_voter":
                pass
            elif sub_operation == "vote":
                pass
            else:
                pass
        pass
        return {"msg": res}
    except Exception as exe:
        print(exe)
        traceback.print_exc()
        return {"msg": "error"}


def deploy_contract(data):
    print("deploy contract")
    contract_name = data.get('name')
    user_id = "gov_user"
    uid = generate_uid()
    user: User = User.objects.filter(user_id=user_id).first()
    contract = Contract()
    contract.name = contract_name
    contract.contract_id = "address" + "_" + uid
    contract.user = user
    contract.save()

    candidates = data.get("contract_list")
    del data["contract_list"]

    data['params'] = {"candidate": candidates}
    data['uid'] = uid
    data['contract_name'] = "voting"
    data['id'] = uid
    data = get_new_data_transaction(data=data, uid=uid, url="http://127.0.0.1:8000/setup-deploy/", user=user)
    print("data to be sent for deploy ", data)
    res = get_client(address).contract_execute(wallet_pb2.WalletData(data=json.dumps(data)))
    return res.data


def add_user(data):
    uid = generate_uid()
    #    user = add_user_model(data.get("user_id"), data.get('password'))
    del data['password']
    data['uid'] = uid
    data = get_new_data_transaction(data, uid, user, "http://127.0.0.1:8000/setup-user/")
    res = get_client(address).add_user(wallet_pb2.WalletData(data=json.dumps(data)))
    print("Add use res ", res)
    return res.data


def add_user_model(id, password):
    user = User(user_id=id, password=password)
    user.save()
    return user


def wallet_server_call(data):
    client = get_client(address)
    res = client.add_user(wallet_pb2.WalletData(data=json.dumps(data)))
    return res
    pass


# def get_client(address) -> wallet_pb2_grpc.WalletStub:
#     channel = grpc.insecure_channel(address)
#     stub = wallet_pb2_grpc.WalletStub(channel=channel)
#     return stub
#

def get_contract(user: User):
    contracts = Contract.objects.filter(user=user)
    return contracts


@api_view(['POST'])
def callback_of_server(request):
    pass


@api_view(['POST'])
def setup_execute_callback(request):
    pass


@api_view(['POST'])
def setup_deploy_callback(request):
    data = request.data
    print("callback deploy ", data)
    contract = Contract.objects.filter(contract_id=data.get("address_" + data.get('uid')))
    contract.status = 1
    contract.save()
    return Response({"msg": "okay"})
    pass


def generate_uid():
    return str(time.time_ns())


def get_new_data_transaction(data, uid, user, url):
    tran = Transaction()
    tran.user = user
    tran.uid = uid
    tran.output = "pending"
    tran.hash = "pending"
    tran.save()
    data['url'] = url
    return data
    pass


@api_view(['POST'])
def setup_user_callback(request):
    print("callbac is ", request.data)
    # data = json.loads(request.body.decode())
    # print("callback recive", data)
    # tran: Transaction = Transaction.objects.filter(uid=data.get('uid')).first()
    # user: User = tran.user
    #
    # user.public_key = data.get('key').get('public')
    # user.private_key = data.get('key').get('private')
    # user.save()
    # tran.hash = data.get('hash')
    # tran.output = data.get('output')
    # tran.save()
    return JsonResponse({"msg": "okay"})
    pass


def setup():
    return
    print("setup started")
    gov_user_model = User()
    gov_user_model.user_id = "gov_user"
    gov_user_model.password = "default"
    gov_user_model.user_type = 1
    gov_user_model.save()

    node_user_model = User()
    node_user_model.user_id = "node_user"
    node_user_model.password = "default"
    node_user_model.user_type = 2
    node_user_model.save()

    client = get_client(address)
    uid_gov = generate_uid()
    gov_user = {"uid": uid_gov,
                "fun": "add_user",
                "name": "gov_superuser",
                "url": "http://127.0.0.1:8000/setup-user/",
                "other_detail": {
                    "age": 23
                }}
    uid_node = generate_uid()
    node_registry_user = {"uid": uid_node,
                          "fun": "add_user",
                          "name": "gov_superuser",
                          "url": "http://127.0.0.1:8000/setup-user/",
                          "other_detail": {
                              "age": 55
                          }}
    tran_gov = Transaction()
    tran_gov.user = gov_user_model
    tran_gov.uid = uid_gov
    tran_gov.hash = "pending"
    tran_gov.time = str(time.time_ns())
    tran_gov.save()

    tran_node = Transaction()
    tran_node.user = node_user_model
    tran_node.uid = uid_node
    tran_node.hash = "pending"
    tran_gov.time = str(time.time_ns())
    tran_node.save()

    gov_res = client.add_user(wallet_pb2.WalletData(data=json.dumps(gov_user)))
    node_res = client.add_user(wallet_pb2.WalletData(data=json.dumps(node_registry_user)))
    print("node res ", node_res)
    print("gov_res ", gov_res)


if __name__ == "__main__":
    pass
