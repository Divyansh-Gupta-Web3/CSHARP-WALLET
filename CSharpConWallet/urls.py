"""This module define the mapping between URLs and views"""

from django.urls import path
from CSharpConWallet import views

urlpatterns = [
    path("", views.index, name="index"),
    path("getpass", views.get_pass, name="get_pass"),
    path("createWallet", views.create_wallet, name="create_wallet"),
    path("login", views.signin, name="signin"),
    path("verify", views.verify, name="verify"),
    path("recover", views.recover, name="recover"),
    path("createRecovery", views.create_recovery, name="create_recovery"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("send", views.send, name="send"),
    path("request", views.request_m, name="request"),
    path("history", views.history, name="history"),
    path("settings", views.settings, name="settings"),
    path("support", views.support, name="support"),
    path("faqs", views.faq, name="faq"),
    path("vault", views.collection, name="collection"),
    path("logoutpage/", views.logoutpage, name="logout"),
    path("messages", views.inbox, name="inbox"),
    path("notifications", views.notifications, name="notifications"),
    path("verifyAccount/<slug:token>", views.verify_email, name="verify_email"),
    path("NFTData/<slug:token>", views.NFTData, name="NFT-verify"),
    path("doctorlogin", views.doctorlogin, name="doctorlogin"),
    path("test", views.test, name="test"),
    path("HealthcareVault", views.nftdata, name="nftdata"),
    path("API", views.make_report, name="API"),
]

handler404 = "CSharpConWallet.views.error"
