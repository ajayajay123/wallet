
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import blockchain_api
from . import page_views

router = routers.SimpleRouter()
# router.register(r'/', walletapp_view.home)

urlpatterns = [



    # Api
    path("add-user/", blockchain_api.add_user_new),
    path("contract/", blockchain_api.smart_contract_new),
    path("start/", blockchain_api.start_new),
    path("end/", blockchain_api.end_new),
    path("vote/", blockchain_api.vote_new),
    path("add/", blockchain_api.add_voter_new),
    path("winner/", blockchain_api.winner_new),
    path("count/", blockchain_api.count_new),
    path("uid/", blockchain_api.get_uid_map),

    # callback
    path("user-callback/", blockchain_api.user_callback),
    path("deploy-callback/", blockchain_api.deploy_callback),
    path("execute-callback/", blockchain_api.execute_callback),
    path('get-user-token/', blockchain_api.get_user_token),
]

page_url = [

    path("", page_views.home),
    path('add-user', page_views.add_user),
    path('add-voter', page_views.add_voter),
    path('contract', page_views.contract),
    path('get-vote-count', page_views.get_vote_count),
    path('vote', page_views.vote),
    path('login/', page_views.login),



]

token_ditail = {}
blockchain_api.token_detail = token_ditail
page_views.token_detail = token_ditail

