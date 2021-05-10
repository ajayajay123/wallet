from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .interface import wallet_pb2, wallet_pb2_grpc
import grpc, json, random
import time
from .models import User, Transaction, Contract
from hashlib import md5
import traceback

address = "localhost:9000"
user_session = {}
user_session_rev = {}
node_certificate = {}
user_key = {}


# Create your views here.

def generate_tocken():
    return md5(str(random.random()).encode()).hexdigest()


def home(request):
    return render(request, './index.html')


def dashboard(request):
    return render(request, './index.html')


def operation(request):
    return render(request, './index.html')


@api_view(['POST', 'GET'])
def home_api(request):
    try:
        data = request.data
        print(data)
        user = User.objects.filter(id=data.get('user_id'), password=data.get('password')).first()
        if user is None:
            return Response({"msg": "invalid username or password"})
        session = generate_tocken()
        prev_session = user_session_rev.get(user.user_id)
        if prev_session is not None:
            del user_session[prev_session]
        user_session[session] = user.user_id
        user_session_rev[user.user_id] = session
        return Response({"tocken": session})
    except Exception as exe:
        print(exe)
        return Response({"msg": "Incorect Data"})
    pass


@api_view(['POST'])
def get_key_api(request):
    pass


@api_view(['POST'])
def operation_api(request):
    data = request.data
    res = gen_fun(data)
    return Response(res)
    pass


def gen_fun(data):
    fun = data.get('fun')
    try:
        if fun == "add_user":
            res = add_user(data)
            pass
        elif fun == "deploy_contract":
            sub_operation = data.get('operation')
            res = deploy_contract(data)
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
    contract_name = data.get('name')
    user_id = "gov_user"
    uid = generate_uid()
    user: User = User.objects.filter(user_id=user_id).first()
    contract = Contract()
    contract.name = contract_name
    contract.contract_id = address + "_" + uid
    contract.user = user
    contract.save()

    candidates = data.get("candidates")
    del data["candidates"]

    data['params'] = {"candidate": candidates}

    data = get_new_data_transaction(data, uid, "http://127.0.0.1:8000/setup-user/", user)
    res = get_client(address).capp_execute(wallet_pb2.WalletData(data=json.dumps(data)))
    return res


def add_user(data):
    uid = generate_uid()
    user = add_user_model(data.get("user_id"), data.get('password'))
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


def get_client(address) -> wallet_pb2_grpc.WalletStub:
    channel = grpc.insecure_channel(address)
    stub = wallet_pb2_grpc.WalletStub(channel=channel)
    return stub


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
    data = json.loads(request.body.decode())
    print("callback recive", data)
    tran: Transaction = Transaction.objects.filter(uid=data.get('uid')).first()
    user: User = tran.user

    user.public_key = data.get('key').get('public')
    user.private_key = data.get('key').get('private')
    user.save()
    tran.hash = data.get('hash')
    tran.output = data.get('output')
    tran.save()
    return JsonResponse({"msg": "okay"})
    pass


def setup():
    return
    print("setup started")
    gov_user_model = User()
    gov_user_model.user_id = "gov_user"
    gov_user_model.password = "default"
    # gov_user_model.type = 1
    gov_user_model.save()

    node_user_model = User()
    node_user_model.user_id = "node_user"
    node_user_model.password = "default"
    # node_user_model.type = 2
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