from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .interface import wallet_pb2, wallet_pb2_grpc
import grpc, json, random
from .Voting import Voting
import time
from threading import Thread
from .models import User

import asyncio
import websockets

uid_map = {}
add_user_token = ['test']
uid_user_map = {}
token_detail = {}

address = "localhost:9000"

user = []
contract = {}
loop = asyncio.get_event_loop()


def get_client(wallet_address) -> wallet_pb2_grpc.WalletStub:
    channel = grpc.insecure_channel(wallet_address)
    stub = wallet_pb2_grpc.WalletStub(channel=channel)
    return stub


def generate_uid():
    return str(time.time_ns())


@csrf_exempt
@api_view(['POST', 'GET'])
def get_uid_map(request):
    data = request.data
    uid = data.get('uid')
    # print("uid recive ", uid)
    return Response({"value": uid_map.get(uid)})


@csrf_exempt
@api_view(['POST', 'GET'])
def get_user_token(request):
    data = request.data
    uid = generate_uid()
    add_user_token.append(uid)
    return Response({"token": uid})


@csrf_exempt
@api_view(['POST', 'GET'])
def add_user_new(request):
    data = request.data
    print(type(data), data)
    uid = generate_uid()
    uid_map[uid] = "no"
    token = data.get('token')
    if token not in add_user_token:
        return Response(json.dumps({"msg": "Invalid Token", "error": True}))
    user_id = data.get('user_id')
    password = data.get('password')
    try:
        user_mode = User(user_id=user_id, password=password)
        user_mode.save()
    except Exception as exe:
        print(exe)
        Response(json.dumps({"msg": "User already Exist", "error": True}))
    uid_user_map[uid] = user_id
    user = {"uid": uid,
            "fun": "add_user",
            "address": user_id,
            "name": "normal",
            "url": "http://192.168.1.7:8000/api/user-callback/",
            "other_detail": {
                "age": 23
            }}
    client = get_client(address)
    res = client.add_user(wallet_pb2.WalletData(data=json.dumps(user)))
    print("response of add user is ", res)
    return Response(json.dumps({"msg": "added", "uid": uid}))
    pass


@api_view(['POST', 'GET'])
@csrf_exempt
def smart_contract_new(request):
    uid = generate_uid()
    data = request.data
    id = data.get('id')
    uid_map[uid] = "no"
    candidates = data.get('candidates')
    for candidate in candidates:
        can = User.objects.filter(user_id=candidate).first()
        if can is None or can.public_key is None:
            return Response({"msg": "Invalid Candidates ", "error": True})
    deploy_conract_data = {
        "is_wallet": True,
        "uid": uid,
        "fun": "deploy_contract",
        "id": id,
        "host": "localhost",
        "url": "http://192.168.1.7:8000/api/deploy-callback/",
        "contract_name": "voting",
        "params": {
            "candidate": candidates
        }
    }
    client = get_client(address)
    res = client.contract_execute(wallet_pb2.WalletData(data=json.dumps(deploy_conract_data)))
    print("response of deploy contract is ", res)
    return Response({"msg": "created ", "uid": uid})
    pass


@api_view(['POST', 'GET'])
@csrf_exempt
def add_voter_new(request):
    uid = generate_uid()
    data = request.data
    uid_map[uid] = "no"
    print("request data is", type(data), data)
    contract_id = "address_" + data.get('id')
    voter_list = data.get('voter_list')
    add_voter = {
        "is_wallet": True,
        "uid": uid,
        "fun": "execute",
        "id": "c4",
        "host": "localhost",
        "contract_name": "voting",
        "url": "http://192.168.1.7:8000/api/execute-callback/",
        "contract_id": contract_id,
        "operation": "add_voter",
        "params": {
            "voter_list": voter_list
        }
    }
    client = get_client(address)
    res = client.contract_execute(wallet_pb2.WalletData(data=json.dumps(add_voter)))
    print("response of add voter is ", res)
    return Response({"msg": "voter added", "uid": uid})

    pass


@api_view(['POST', 'GET'])
@csrf_exempt
def start_new(request):
    data = request.data
    uid = generate_uid()
    uid_map[uid] = "no"
    contract_id = "address_" + data.get('id')
    start_voting = {
        "is_wallet": True,
        "uid": uid,
        "fun": "execute",
        "id": "c3",
        "url": "http://192.168.1.7:8000/api/execute-callback/",
        "host": "localhost",
        "contract_name": "voting",
        "contract_id": contract_id,
        "operation": "start",
    }
    client = get_client(address)
    res = client.contract_execute(wallet_pb2.WalletData(data=json.dumps(start_voting)))
    print("response of add voter is ", res.data)
    return Response({"msg": "started", "uid": uid})
    pass


@api_view(['POST', 'GET'])
@csrf_exempt
def vote_new(request):
    token = request.COOKIES.get('token')
    # print(token_detail)
    user_id = token_detail.get(token).get('user_id')
    # print(user_id)
    uid = generate_uid()
    data = request.data
    uid_map[uid] = "no"
    candidate = data.get('candidate')
    me_address = user_id  # data.get('address')
    contract_id = "address_" + data.get("id")
    vote = {
        "is_wallet": True,
        "uid": uid,
        "fun": "execute",
        "id": "ajay",
        "url": "http://192.168.1.7:8000/api/execute-callback/",
        "contract_name": "voting",
        "contract_id": contract_id,
        "operation": "vote",
        "params": {
            "candidate": candidate,
            "address": me_address
        }
    }
    client = get_client(address)
    res = client.contract_execute(wallet_pb2.WalletData(data=json.dumps(vote)))
    print("response of add voter is ", res.data)
    return Response({"msg": "voted", "uid": uid})
    pass


@api_view(['POST', 'GET'])
@csrf_exempt
def end_new(request):
    data = request.data
    uid = generate_uid()
    uid_map[uid] = "no"
    contract_id = "address_" + data.get('id')
    end = {
        "is_wallet": True,
        "uid": uid,
        "fun": "execute",
        "id": "c3",
        "url": "http://192.168.1.7:8000/api/execute-callback/",
        "contract_name": "voting",
        "contract_id": contract_id,
        "operation": "end",
    }
    client = get_client(address)
    res = client.contract_execute(wallet_pb2.WalletData(data=json.dumps(end)))
    print("response of  end is ", res.data)
    return Response({"msg": "end", "uid": uid})
    pass


@api_view(['POST', 'GET'])
@csrf_exempt
def winner_new(request):
    data = request.data
    contract_id = "address_" + data.get('id')
    uid = generate_uid()
    uid_map[uid] = "no"
    print("data")
    winner = {
        "is_wallet": True,
        "uid": uid,
        "fun": "execute",
        "id": "c3",
        "url": "http://192.168.1.7:8000/api/execute-callback/",
        "contract_name": "voting",
        "contract_id": contract_id,
        "operation": "winner",
    }
    client = get_client(address)
    res = client.contract_execute(wallet_pb2.WalletData(data=json.dumps(winner)))
    print("response of winner is ", res.data)
    return Response({"msg": "winner", "uid": uid})
    pass


@api_view(['POST', 'GET'])
@csrf_exempt
def count_new(request):
    data = request.data
    contract_id = "address_" + data.get('id')
    uid = generate_uid()
    uid_map[uid] = "no"
    print("data")
    winner = {
        "is_wallet": True,
        "uid": uid,
        "fun": "execute",
        "id": "c3",
        "url": "http://192.168.1.7:8000/api/execute-callback/",
        "contract_name": "voting",
        "contract_id": contract_id,
        "operation": "vote_count",
    }
    client = get_client(address)
    res = client.contract_execute(wallet_pb2.WalletData(data=json.dumps(winner)))
    print("response of winner is ", res.data)
    return Response({"msg": "vote count", "uid": uid})
    pass


@api_view(['POST'])
def user_callback(request):
    print("callback user ", request.data)
    data = request.data
    uid = data.get("uid")
    uid_map[uid] = data
    print(uid_user_map, uid)
    user_id = uid_user_map.get(uid)
    prev_user: User = User.objects.filter(user_id=user_id).first()
    prev_user.public_key = data.get('key').get('public')
    prev_user.private_key = data.get('key').get('private')
    prev_user.save()

    return JsonResponse({"msg": "okay"})
    pass


@api_view(['POST'])
def deploy_callback(request):
    data = request.data
    print("callback deploy ", data)
    uid = data.get("uid")
    uid_map[uid] = data
    return Response({"msg": "okay"})
    pass


@api_view(['POST'])
def execute_callback(request):
    data = request.data
    print("callback execute ", data)

    uid = data.get("uid")
    uid_map[uid] = data
    # print(uid_map, data)
    return Response({"msg": "okay"})
    pass


async def hello(websocket, path):
    name = await websocket.recv()
    print(name)

    greeting = f"Hello {name}!"

    # await websocket.send(greeting)
    # print(f"> {greeting}")


start_server = websockets.serve(hello, "localhost", 20000)


def start_web_socket():
    loop.run_until_complete(start_server)
    print("web socket started")
    loop.run_forever()
    print("web socket Ended")
