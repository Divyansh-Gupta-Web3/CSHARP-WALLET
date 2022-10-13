"""This module receive a web request and return a web response"""  # pylint: disable=C0302

import uuid
import json
from datetime import datetime
import datetime as dateT
import logging
import base64
import requests
import pyshorteners
from django.core.paginator import Paginator
from django.core.cache import cache
from django.http import HttpResponseBadRequest, HttpResponse
from django.db.models import Max
from django.core.cache import cache
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from CSharpConWallet.used_module import (
    UserReport,
    Contacts,
    get_user_model,
    login_required,
    redirect,
    render,
    PurestakeMainnet,
    PurestakeTestnet,
    VerifyWords,
    NetAPI,
    authenticate,
    AssetTransferTxn,
    wait_for_confirmation,
    messages,
    indexer,
    sample,
    logout,
    transaction,
    mnemonic,
    GetpassField,
    account,
    get_passphrase,
    login,
    FAQs,
    qrcode,
    BytesIO,
    decode_address,
    encode_address,
    HttpResponseRedirect,
    Messages,
    TokenRequests,
    get_object_or_404,
    Support,
    AssetConfigTxn,
    Email_verify,
    admin_data,
    HealthRecords,
)

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.INFO)

asset_id_testnet = 85344041
asset_id_mainnet = 711565009


def addDays():
    """_summary_

    Returns: date
    """
    newDate = datetime.now() - dateT.timedelta(1)
    return newDate


def test(request):
    """_summary_

    Args: request (object): request object

     Returns: renders test.html
    """
    cache.set("my_key", "hello, world!")
    print(cache.get("my_key"))
    if request.method == "POST":
        test = request.POST.get("submit")
        cache.set("my_key", "test", timeout=10)
        print(cache.get("my_key"))
        return HttpResponseRedirect("test2")

    return render(request, "test.html")


@login_required(login_url="signin")
def nftdata(request):
    """_summary_

    Args: request (object): request object

     Returns: renders test.html
    """
    if cache.get("my_key") is None:
        return redirect("/vault")
    elif cache.get("my_key") == "nftdata":
        request.session["acceptid"] = "noid"
        session_net = request.session["name"]
        add = str(request.user.Address)
        role = get_user_model().objects.get(username=request.user.username)
        if role.is_superuser:
            user_role = "admin"
        else:
            user_role = "user"
        if request.session["name"] == "mainnet":
            trxndata = trxn_notif_mainnet(request)
            algord = PurestakeMainnet()
            asset_id = asset_id_mainnet
        else:
            trxndata = trxn_notify_testnet(request)
            algord = PurestakeTestnet()
            asset_id = asset_id_testnet
        algodclient = algord.algodclient
        account_info = algodclient.account_info(add)
        idx = 0
        for _ in account_info["assets"]:
            scrutinized_asset = account_info["assets"][idx]
            idx = idx + 1
            if scrutinized_asset["asset-id"] == asset_id:
                assets_token = json.dumps(scrutinized_asset["amount"])
                break
        notification_paginator = Paginator(trxndata, 5)
        notification_page_number = request.GET.get("page")
        notification_page_obj = notification_paginator.get_page(
            notification_page_number
        )
        total_balance = format((int(assets_token) / 1000), ".3f")
        cent = format(float(total_balance) / 10, ".2f")
        balance = {
            "inUSD": cent,
            "balance": total_balance,
            "trxn_data": notification_page_obj,
            "session_net": session_net,
            "user_role": user_role,
            "addDays": addDays(),
        }
        filtered_msg = msg_notif(request)
        balance["filtered_msg"] = filtered_msg
        count_msg = Messages.objects.filter(User=request.user, is_read=False).count()
        balance["count_msg"] = count_msg
        report = requests.get("http://127.0.0.1:8000/API").json()
        balance["report"] = report
        return render(request, "nftdata.html", balance)


def error(request, exception):
    """_summary_

    Args: request (object): request object

     Returns: renders error.html
    """
    return render(request, "404.html")


def recent_actions(request):
    """_summary_

    Args: request (object): request object

     Returns: renders recent_actions.html
    """
    # check user is superuser or not
    if request.user.is_superuser:
        return render(request, "admin/recent_actions.html")
    else:
        return render(request, "login.html")


def user_details(request):
    request.session["acceptid"] = "noid"
    session_net = request.session["name"]
    add = str(request.user.Address)
    role = get_user_model().objects.get(username=request.user.username)
    if role.is_superuser:
        user_role = "admin"
    else:
        user_role = "user"
    if request.session["name"] == "mainnet":
        trxndata = trxn_notif_mainnet(request)
        algord = PurestakeMainnet()
        asset_id = asset_id_mainnet
    else:
        trxndata = trxn_notify_testnet(request)
        algord = PurestakeTestnet()
        asset_id = asset_id_testnet
    algodclient = algord.algodclient
    account_info = algodclient.account_info(add)
    idx = 0
    for _ in account_info["assets"]:
        scrutinized_asset = account_info["assets"][idx]
        idx = idx + 1
        if scrutinized_asset["asset-id"] == asset_id:
            assets_token = json.dumps(scrutinized_asset["amount"])
            break
    notification_paginator = Paginator(trxndata, 5)
    notification_page_number = request.GET.get("page")
    notification_page_obj = notification_paginator.get_page(notification_page_number)
    total_balance = format((int(assets_token) / 1000), ".3f")
    cent = format(float(total_balance) / 10, ".2f")
    que_ans = FAQs.objects.all()
    balance = {"inUSD": cent, "balance": total_balance, "data": que_ans}
    balance["trxn_data"] = notification_page_obj
    balance["session_net"] = session_net
    balance["addDays"] = addDays()
    balance["role"] = user_role
    filtered_msg = msg_notif(request)
    balance["filtered_msg"] = filtered_msg
    count_msg = Messages.objects.filter(User=request.user, is_read=False).count()
    balance["count_msg"] = count_msg
    current_user = request.user
    count_request = TokenRequests.objects.filter(
        recipient=current_user, is_rejected=False, is_accepted=False
    ).count()
    balance["count_request"] = count_request
    notif_request = request_notif(request)
    balance["notif_request"] = notif_request
    return balance


def verify_email(request, token):

    """_summary_

    Args: request (object): request object

     Returns: renders verify_email.html
    """
    try:
        acc_verify = Email_verify.objects.filter(email_verify_token=token).values(
            "User"
        )
        s_data = list(acc_verify)[0]["User"]
        user = get_user_model().objects.filter(id=s_data).values("Address")
        address = list(user)[0]["Address"]
        logging.info(address)
        acc_verify = Email_verify.objects.filter(email_verify_token=token).first()
        if acc_verify.verify == True:
            messages.success(request, "Your Account Has Been Verified")
            return redirect(("signin"))
        else:
            acc_verify.verify = True
            acc_verify.save()
            messages.success(request, "Your Account Has Been Verified")
            return redirect(("signin"))
    except:
        messages.error(request, "Your Account Has Not Been Verified")
        return redirect(("signin"))


def doctorlogin(request):
    """_summary_

    Args: request (object): request object

    Returns: renders index.html
    """
    next = request.GET["next"]
    if request.method == "POST":
        name = request.POST.get("accname")
        pwd = request.POST.get("password")
        user = authenticate(request, username=name, password=pwd)
        if user is not None:
            login(request, user)
            if user.role == "Doctor":
                request.session["name"] = "testnet"
                return HttpResponseRedirect(next)
            else:
                messages.error(request, "You are not authorized to access this page")
        else:
            messages.error(request, "Invalid Credentials")
    return render(request, "login.html", {"role": "Doctor"})


@login_required(login_url="doctorlogin")
def NFTData(request, token):
    balance = user_details(request)
    search_user = get_user_model().objects.get(user_token=token)
    if search_user:
        user_name = search_user.id
        address = search_user.Address
        role = request.user.role
        get_nftdata = HealthRecords.objects.filter(User=user_name).values(
            "personal", "emergency", "NFT_image"
        )
        if get_nftdata:
            personal = list(get_nftdata)[0]["personal"]
            emergency = list(get_nftdata)[0]["emergency"]
        # call Report From API
        report = requests.get("http://127.0.0.1:8000/API").json()
        balance["report"] = report
        balance["personal"] = personal
        balance["emergency"] = emergency
        balance["role"] = role
        algord = PurestakeTestnet()
        algod_client = algord.algodclient
        account_info = algod_client.account_info(address)
        idx = 0
    else:
        return redirect("dashboard")
    return render(request, "doctor.html", balance)


def base64_encode(string):
    """_summary_

    Args: string: string that needs to encoded

    Returns: encoded data
    """
    return base64.b64encode(string.encode("ascii")).decode("ascii")


def base64_decode(string):
    """_summary_

    Args: string: string that needs to decoded

    Returns: decoded data
    """
    return base64.b64decode(string.encode("ascii")).decode("ascii")


def base32_encode(string):
    """_summary_

    Args: string: string that needs to encoded

    Returns: encoded data
    """
    return base64.b32encode(string.encode("ascii")).decode("ascii")


def base32_decode(string):
    """_summary_

    Args: string: string that needs to decoded

    Returns: decoded data
    """
    return base64.b32decode(string.encode("ascii")).decode("ascii")


def json_notify(request):
    """_summary_

    Args: request (object): request object

     Returns: renders json_notify.html
    """

    add = str(request.user.Address)
    algord = PurestakeTestnet()
    algodclient = algord.algodclient
    account_info = algodclient.account_info(add)
    idx = 0
    for _ in account_info["assets"]:
        scrutinized_asset = account_info["assets"][idx]
        idx = idx + 1
        if scrutinized_asset["asset-id"] == asset_id_testnet:
            # assets_token = json.dumps(scrutinized_asset["amount"])
            break
    json_data = []
    dbdata = admin_data.objects.filter(key="PureStake").values("values")
    algod_token = list(dbdata)[0]["values"]
    algod_address = "https://testnet-algorand.api.purestake.io/idx2"
    purestake_token = {"X-API-Key": algod_token}
    acl = indexer.IndexerClient(algod_token, algod_address, headers=purestake_token)
    response = acl.search_transactions(address=add)
    amts = response["transactions"]
    current_user = request.user
    get_request = TokenRequests.objects.filter(
        recipient=current_user, is_rejected=False, is_accepted=False
    ).values("date", "token", "sender", "recipient")
    if get_request:
        for i in range(len(get_request)):
            s_data = list(get_request)[i]["date"]
            serial = datetime.strftime(s_data, "%Y-%m-%d %H:%M:%S")
            token = list(get_request)[i]["token"]
            sender = list(get_request)[i]["sender"]
            recipient = list(get_request)[i]["recipient"]
            request_date = {
                "date": serial,
                "amount": token,
                "sender": sender,
                "recipient": recipient,
                "trxn_type": "Request",
            }
            json_data.append(request_date)
    for amt in amts:
        round_time = amt["round-time"]
        timestamp = int(round_time)
        dt_object = datetime.fromtimestamp(timestamp)
        datetime_serial = datetime.strftime(dt_object, "%Y-%m-%d %H:%M:%S")
        sender = amt["sender"]
        txn_type = amt.get("tx-type")
        if txn_type == "pay":
            amoun = amt["payment-transaction"]["amount"]
            amount = format(float(amoun / 1000000), ".3f")
            receiver = amt["payment-transaction"]["receiver"]
            if sender == add:
                tnxtype = "Sent"
            else:
                tnxtype = "Received Algo"

        elif txn_type == "acfg":
            receiver = "Asset " + str(amt["created-asset-index"])
            tnxtype = "NFT"
            amount = format(0.000, ".3f")
        else:
            asset_t = amt.get("asset-transfer-transaction")
            amoun = asset_t.get("amount")
            amount = format(amoun / 1000, ".3f")
            receiver = asset_t.get("receiver")
            if txn_type == "Pay":
                tnxtype = "Pay"
            else:
                if sender == add:
                    tnxtype = "Sent"
                else:
                    tnxtype = "Received"
        txn_data = {
            "date": datetime_serial,
            "amount": amount,
            "sender": sender,
            "receiver": receiver,
            "type": tnxtype,
        }
        json_data.append(txn_data)
    return json_data


def request_notif(request):
    """_summary_

    Args: request (object): request object

    Returns: renders get_request
    """
    current_user = request.user
    get_request = (
        TokenRequests.objects.filter(
            recipient=current_user, is_rejected=False, is_accepted=False
        )
        .annotate(last=Max("date"))
        .order_by("-last")
    )
    # pylint: disable=E1101,C0301
    return get_request


def msg_notif(request):
    """_summary_

    Args: request (object): request object

     Returns: renders Notification_page_obj
    """
    message = Messages.get_messages(User=request.user)
    notification_paginator = Paginator(message, 5)
    notification_page_number = request.GET.get("page")
    notification_page_obj = notification_paginator.get_page(notification_page_number)
    return notification_page_obj


def trxn_notif_mainnet(request):  # pylint: disable=R0914,R0915
    """_summary_

    Args: request (object): request object

     Returns: renders send.html
    """
    add = str(request.user.Address)

    algord = PurestakeMainnet()
    algodclient = algord.algodclient
    account_info = algodclient.account_info(add)
    idx = 0
    for _ in account_info["assets"]:
        scrutinized_asset = account_info["assets"][idx]
        idx = idx + 1
        if scrutinized_asset["asset-id"] == asset_id_mainnet:
            # assets_token = json.dumps(scrutinized_asset["amount"])
            break
    trxn_data = []
    dbdata = admin_data.objects.filter(key="PureStake").values("values")
    algod_token = list(dbdata)[0]["values"]
    algod_address = "https://mainnet-algorand.api.purestake.io/idx2"
    purestake_token = {"X-API-Key": algod_token}
    acl = indexer.IndexerClient(algod_token, algod_address, headers=purestake_token)
    response = acl.search_transactions(address=add)
    amts = response["transactions"]
    sno = 0
    # current_user = request.user
    for amt in amts:
        cnfround = amt["confirmed-round"]
        sender = amt["sender"]
        round_time = amt["round-time"]
        tx_id = amt["id"]
        timestamp = int(round_time)
        dt_object = datetime.fromtimestamp(timestamp)
        fees = amt["fee"]
        fee = float(fees / 1000000)
        txn_type = amt.get("tx-type")
        if txn_type == "pay":
            receiver = amt["payment-transaction"]["receiver"]
            if sender == add:
                tnxtype = "Sent"
            else:
                tnxtype = "Received Algo"
            sno = sno + 1
        elif txn_type == "acfg":
            receiver = "Asset " + str(amt["created-asset-index"])
            txn_type = "NFT"
            amount = format(0.000, ".3f")
        else:
            asset_t = amt.get("asset-transfer-transaction")
            amoun = asset_t.get("amount")
            amount = format(amoun / 1000, ".3f")
            receiver = asset_t.get("receiver")
            if txn_type == "Pay":
                tnxtype = "Pay"
            else:
                if sender == add:
                    tnxtype = "Sent"
                else:
                    tnxtype = "Received"
            sno = sno + 1
        txn_data = {
            "sno": sno,
            "id": tx_id,
            "cnfround": cnfround,
            "amount": amount,
            "receiver": receiver,
            "sender": sender,
            "fee": fee,
            "tnxtype": tnxtype,
            "time": dt_object,
        }
        trxn_data.append(txn_data)

    return trxn_data


def trxn_notify_testnet(request):  # pylint: disable=R0914,R0915
    """_summary_

    Args: request (object): request object

     Returns: renders send.html
    """
    add = str(request.user.Address)
    algord = PurestakeTestnet()
    algodclient = algord.algodclient
    account_info = algodclient.account_info(add)
    idx = 0
    for _ in account_info["assets"]:
        scrutinized_asset = account_info["assets"][idx]
        idx = idx + 1
        if scrutinized_asset["asset-id"] == asset_id_testnet:
            break
    trxn_data = []
    dbdata = admin_data.objects.filter(key="PureStake").values("values")
    algod_token = list(dbdata)[0]["values"]
    algod_address = "https://testnet-algorand.api.purestake.io/idx2"
    purestake_token = {"X-API-Key": algod_token}
    acl = indexer.IndexerClient(algod_token, algod_address, headers=purestake_token)
    response = acl.search_transactions(address=add)
    amts = response["transactions"]
    sno = 0
    current_user = request.user
    get_request = (
        TokenRequests.objects.filter(
            recipient=current_user, is_rejected=False, is_accepted=False
        )
        .annotate(last=Max("date"))
        .order_by("-last")
        .values("sender", "token", "date")
    )
    for i in range(len(get_request)):
        sender = get_request[i]["sender"]
        get_username = get_user_model().objects.filter(id=sender).values("username")
        sender_username = get_username[0]["username"]
        token = get_request[i]["token"]
        date = get_request[i]["date"]
        request_token = {
            "sender_username": sender_username,
            "token": token,
            "date": date,
            "type": "Request",
        }
        trxn_data.append(request_token)
    for amt in amts:
        cnfround = amt["confirmed-round"]
        sender = amt["sender"]
        round_time = amt["round-time"]
        tx_id = amt["id"]
        timestamp = int(round_time)
        dt_object = datetime.fromtimestamp(timestamp)
        fees = amt["fee"]
        fee = float(fees / 1000000)
        txn_type = amt.get("tx-type")
        if txn_type == "pay":
            amoun = amt["payment-transaction"]["amount"]
            amount = format(float(amoun / 1000000), ".3f")
            receiver = amt["payment-transaction"]["receiver"]
            if sender == add:
                tnxtype = "Sent"
            else:
                tnxtype = "Received Algo"
            sno = sno + 1
        elif txn_type == "acfg":
            receiver = "Asset " + str(amt["created-asset-index"])
            tnxtype = "NFT"
            amount = format(0.000, ".3f")
        else:
            asset_t = amt.get("asset-transfer-transaction")
            amoun = asset_t.get("amount")
            amount = format(amoun / 1000, ".3f")
            receiver = asset_t.get("receiver")
            if txn_type == "Pay":
                tnxtype = "Pay"
            else:
                if sender == add:
                    tnxtype = "Sent"
                else:
                    tnxtype = "Received"
            sno = sno + 1
        txn_data = {
            "sno": sno,
            "id": tx_id,
            "cnfround": cnfround,
            "amount": amount,
            "receiver": receiver,
            "sender": sender,
            "fee": fee,
            "tnxtype": tnxtype,
            "time": dt_object,
        }
        trxn_data.append(txn_data)
    notif = json_notify(request)
    json_path = str(current_user) + ".json"
    with open("static/user_json/" + (json_path), "w+", encoding="utf-8") as outfile:
        json.dump(notif, outfile)
    return trxn_data


@login_required(login_url="signin")
def inbox(request):  # pylint: disable=R0914,R0915
    """_summary_

    Args: request (object): request object

     Returns: renders inbox.html
    """
    request.session["report"] = ""
    request.session["test"] = "none"
    request.session["acceptid"] = "noid"
    add = str(request.user.Address)
    if request.session["name"] == "mainnet":
        trxndata = trxn_notif_mainnet(request)
        algord = PurestakeMainnet()
        asset_id = asset_id_mainnet
    else:
        trxndata = trxn_notify_testnet(request)
        algord = PurestakeTestnet()
        asset_id = asset_id_testnet
    algodclient = algord.algodclient
    account_info = algodclient.account_info(add)
    idx = 0
    for _ in account_info["assets"]:
        scrutinized_asset = account_info["assets"][idx]
        idx = idx + 1
        if scrutinized_asset["asset-id"] == asset_id:
            assets_token = json.dumps(scrutinized_asset["amount"])
            break

    message = Messages.get_messages(User=request.user)
    active_direct = None
    directs = None
    if message:
        msg = message[0]
        active_direct = msg["user"].username
        directs = Messages.objects.filter(
            User=request.user, recipient=msg["user"]
        )  # pylint: disable=E1101

    context = {
        "directs": directs,
        "messages": message,
        "active_direct": active_direct,
    }
    filtered_msg = msg_notif(request)
    context["filtered_msg"] = filtered_msg
    notif_request = request_notif(request)
    count_msg = Messages.objects.filter(
        User=request.user, is_read=False
    ).count()  # pylint: disable=E1101
    context["count_msg"] = count_msg
    current_user = request.user
    count_request = TokenRequests.objects.filter(
        recipient=current_user, is_rejected=False, is_accepted=False
    ).count()  # pylint: disable=E1101,C0301
    context["count_request"] = count_request
    notif_request = request_notif(request)
    context["notif_request"] = notif_request
    notification_paginator = Paginator(trxndata, 5)
    notification_page_number = request.GET.get("page")
    notification_page_obj = notification_paginator.get_page(notification_page_number)
    total_balance = format((int(assets_token) / 1000), ".3f")
    cent = format(float(total_balance) / 10, ".2f")
    context["trxn_data"] = notification_page_obj
    context["inUSD"] = cent
    context["addDays"] = addDays()
    user = get_user_model()
    if "favid" in request.GET:
        pid = request.GET.get("favid")
        try:
            users_fav = user.objects.filter(Address=pid).values(
                "username", "profile_pic"
            )
            to_user = list(users_fav)[0]["username"]
            to_user_profile = list(users_fav)[0]["profile_pic"]
            logging.info(to_user_profile)
            from_user = request.user
            directs_message = Messages.objects.filter(
                User=from_user, recipient__username=to_user
            )  # pylint: disable=E1101,C0301
            directs_message.update(is_read=True)
            directs_msg = (
                Messages.objects.filter(User=from_user, recipient__username=to_user)
                .annotate(last=Max("date"))
                .order_by("last")
            )  # pylint: disable=E1101,C0301
            body = request.POST.get("body")
            if request.method == "POST":
                to_user = user.objects.get(username=to_user)
                Messages.send_message(from_user, to_user, body)
                redirect_url = request.build_absolute_uri()
                return HttpResponseRedirect(redirect_url)
            add = str(request.user.Address)
            context["direct_msg"] = directs_msg
            context["sender"] = to_user
            context["sender_pic"] = to_user_profile
            context["pid"] = pid
        except:  # pylint: disable=W0702
            messages.warning(request, "This Address is not registered with us")
            return redirect("dashboard")

    return render(request, "inbox.html", context)


def notifications(request):  # pylint: disable=R0914,R0915
    """_summary_

    Args: request (object): request object

     Returns: renders notification.html
    """
    request.session["report"] = ""
    request.session["test"] = "none"
    request.session["acceptid"] = "noid"
    add = str(request.user.Address)
    if request.session["name"] == "mainnet":
        trxndata = trxn_notif_mainnet(request)
    else:
        trxndata = trxn_notify_testnet(request)
    balance = user_details(request)
    notification_paginator = Paginator(trxndata, 10)
    notification_page_number = request.GET.get("page")
    notification_page_obj = notification_paginator.get_page(notification_page_number)

    next_five = list(trxndata)[:5]
    balance["txn_datas"] = notification_page_obj
    balance["trxn_data"] = next_five
    balance["add"] = add

    return render(request, "notifications.html", balance)


def index(request):
    """_summary_

    Args: request (object): request object

    Returns: renders index.html
    """
    request.session["name"] = "testnet"
    return render(request, "index.html")


@login_required(login_url="signin")
def collection(request):  # pylint: disable=R0914,R0915
    """_summary_
    It will run iff user is logged in.
    Otherwise you will be redirected to signin page.

    Args: request (object): request object

    Returns: renders collection.html
    """
    request.session["acceptid"] = "noid"
    profile_pic = request.user.profile_pic
    img = str(profile_pic)
    nft_id = "0"
    request.session["nft_id"] = ""
    request.session["nft_unit_name"] = ""
    request.session["nft_name"] = ""
    request.session["svg"] = ""
    request.session["PIN"] = ""
    request.session["report"] = ""
    request.session["test"] = "none"
    request.session["personal"] = False
    request.session["emergency"] = False

    def print_created_asset(algodclient, account, assetid):
        account_info = algodclient.account_info(account)
        idx = 0
        for my_account_info in account_info["created-assets"]:
            scrutinized_asset = account_info["created-assets"][idx]
            idx = idx + 1
            if scrutinized_asset["index"] == assetid:
                nft_id = scrutinized_asset["index"]
                asset_detail = json.dumps(my_account_info["params"], indent=4)
                resp = json.loads(asset_detail)
                nft_unit_name = resp["unit-name"]
                nft_name = resp["name"]
                request.session["nft_id"] = nft_id
                request.session["nft_unit_name"] = nft_unit_name
                request.session["nft_name"] = nft_name
                usertoken = request.user.user_token
                nft_verify_link = "https://wallet.mpayz.io//NFTData/" + str(
                    usertoken
                )
                factory = qrcode.image.svg.SvgImage
                img = qrcode.make((nft_verify_link), image_factory=factory, box_size=15)
                stream = BytesIO()
                img.save(stream)
                svg_qr = stream.getvalue().decode()
                request.session["svg"] = svg_qr
                break

    if request.session["name"] == "mainnet":
        print("this feature is currently not available on mainnet")

    else:
        encrypted = str(request.user.passphrase)
        dcode32 = base32_decode(encrypted)
        user_passphrase = base64_decode(dcode32)
        to_user_id = HealthRecords.objects.filter(User=request.user).values(
            "NFT_id", "NFT_image", "PIN"
        )
        if to_user_id:
            nft_id = list(to_user_id)[0]["NFT_id"]
            logging.info(nft_id)
            img = list(to_user_id)[0]["NFT_image"]
            pin = list(to_user_id)[0]["PIN"]
            request.session["PIN"] = pin
            get_nftdata = HealthRecords.objects.get(User=request.user)
            if get_nftdata:
                request.session["personal"] = get_nftdata.personal
                request.session["emergency"] = get_nftdata.emergency
        public_key = mnemonic.to_public_key(user_passphrase)
        private_key = mnemonic.to_private_key(user_passphrase)
        algord = PurestakeTestnet()
        algod_client = algord.algodclient
        params = algod_client.suggested_params()
        if nft_id == "0":
            print("no nft")
        else:
            assetid = int(nft_id)
            print_created_asset(algod_client, public_key, assetid)

        if request.method == "POST" and "nft" in request.POST:
            NFT_name = request.POST.get("name")
            assetname = request.POST.get("desc")
            if "image" in request.FILES:
                profile_pic = request.FILES["image"]
            # create NFT in testnet
            type_tiny = pyshorteners.Shortener()
            long_url = "https://wallet.mpayz.io/" + img
            tiny_url = type_tiny.tinyurl.short(long_url)
            txn = AssetConfigTxn(
                sender=public_key,
                sp=params,
                total=1,
                default_frozen=True,
                unit_name=NFT_name,
                asset_name=assetname,
                manager=public_key,
                reserve=public_key,
                freeze="MMTNTTOQRYSWYZPISJZS43GS5L4YH2SHDEHV4WSQJQLV5ORABVAW4E5EKI",
                clawback=public_key,
                strict_empty_address_check=False,
                url=tiny_url,
                decimals=0,
            )
            stxn = txn.sign(private_key)
            txid = algod_client.send_transaction(stxn)
            wait_for_confirmation(algod_client, txid, 4)
            try:
                ptx = algod_client.pending_transaction_info(txid)
                asset_id = ptx["asset-index"]
                nftdata = HealthRecords.objects.create(
                    User=request.user,
                    NFT_id=asset_id,
                    NFT_image=profile_pic,
                    NFT_trxn_hash=txid,
                )
                nftdata.save()
                assetid = int(asset_id)
                print_created_asset(algod_client, public_key, assetid)
                messages.success(request, "NFT created successfully")
                return redirect("/vault")
                # print_created_asset_test(algod_client, public_key, asset_id)
            except:  # pylint: disable=W0702,C0103
                messages.error(request, "Something went wrong")
                return redirect("/vault")
        if request.method == "POST" and "nftdata" in request.POST:
            personal = False
            emergency = False
            if request.POST.get("personal"):
                personal = True
            if request.POST.get("emergency"):
                emergency = True
            # update HealthRecords
            nftdata = HealthRecords.objects.get(User=request.user)
            nftdata.personal = personal
            nftdata.emergency = emergency
            nftdata.save()
            return redirect("/vault")
        if request.method == "POST" and "setPIN" in request.POST:
            print("this is setPIN")
            p1 = request.POST.get("p1")
            p2 = request.POST.get("p2")
            p3 = request.POST.get("p3")
            p4 = request.POST.get("p4")
            p11 = request.POST.get("p11")
            p22 = request.POST.get("p22")
            p33 = request.POST.get("p33")
            p44 = request.POST.get("p44")
            if p1 == p11 and p2 == p22 and p3 == p33 and p4 == p44:
                nftdata = HealthRecords.objects.get(User=request.user)
                nftdata.PIN = p1 + p2 + p3 + p4
                nftdata.save()
                return redirect("/vault")

        if request.method == "POST" and "chkPIN" in request.POST:
            p1 = request.POST.get("p1")
            p2 = request.POST.get("p2")
            p3 = request.POST.get("p3")
            p4 = request.POST.get("p4")
            nftdata = HealthRecords.objects.get(User=request.user)
            if nftdata.PIN == p1 + p2 + p3 + p4:
                cache.set("my_key", "nftdata", timeout=5)
                return HttpResponseRedirect("HealthcareVault")
            else:
                messages.error(request, "Invalid PIN")
        if request.method == "POST" and "" in request.POST:
            print("empty reload")
        if request.method == "POST" and "resetpin" in request.POST:
            currentPass = request.POST.get("currentPass")
            pin1 = request.POST.get("pin1")
            pin2 = request.POST.get("pin2")
            name = str(request.user.username)
            validate = authenticate(request, username=name, password=currentPass)
            if validate:
                if pin1 == pin2:
                    nftdata = HealthRecords.objects.get(User=request.user)
                    nftdata.PIN = pin1
                    nftdata.save()
                    messages.success(request, "PIN updated successfully")
                    return redirect("/vault")
                else:
                    messages.error(request, "Something went wrong")
                    return redirect("/vault")
            else:
                messages.error(request, "Something went wrong")
                return redirect("/vault")
    print(request.session["test"])
    balance = user_details(request)
    balance["id"] = nft_id
    balance["nft_id"] = request.session["nft_id"]
    balance["nft_unit_name"] = request.session["nft_unit_name"]
    balance["nft_name"] = request.session["nft_name"]
    balance["svg"] = request.session["svg"]
    balance["nft_image"] = img
    # call Report From API
    balance["personal"] = request.session["personal"]
    balance["emergency"] = request.session["emergency"]
    balance["PIN"] = request.session["PIN"]
    balance["flag"] = request.session["test"]
    balance["report"] = request.session["report"]
    return render(request, "collections.html", balance)


@login_required(login_url="signin")
def send(request):  # pylint: disable=R0914,R0912,R0915
    """_summary_

    It will run iff user is logged in.
    Otherwise you will be redirected to signin page.

    Args: request (object): request object

    Returns: renders send.html
    """
    request.session["report"] = ""
    request.session["test"] = "none"
    balance = {}
    add = str(request.user.Address)
    name = str(request.user.username)
    private = str(request.user.privateKey)
    role = get_user_model().objects.get(username=request.user.username)
    if role.is_superuser:
        user_role = "admin"
    else:
        user_role = "user"
    if request.session["name"] == "mainnet":
        trxndata = trxn_notif_mainnet(request)
        algord = PurestakeMainnet()
        asset_id = asset_id_mainnet
    else:
        trxndata = trxn_notify_testnet(request)
        algord = PurestakeTestnet()
        asset_id = asset_id_testnet
    algodclient = algord.algodclient
    account_info = algodclient.account_info(add)
    idx = 0
    for _ in account_info["assets"]:
        scrutinized_asset = account_info["assets"][idx]
        idx = idx + 1
        if scrutinized_asset["asset-id"] == asset_id:
            assets_token = json.dumps(scrutinized_asset["amount"])
            break
    if request.method == "POST":
        address = request.POST.get("address")
        amount = request.POST.get("amount")
        pwd = request.POST.get("password")
        user = authenticate(request, username=name, password=pwd)
        if user is not None:
            amt = float(amount) * 1000
            amount = int(amt)
            try:
                params = algodclient.suggested_params()
                params.fee = 1000
                params.flat_fee = True
                txn = AssetTransferTxn(
                    sender=add,
                    sp=params,
                    receiver=address,
                    amt=amount,
                    index=asset_id,
                )
                stxn = txn.sign(private)
                txid = algodclient.send_transaction(stxn)
                logging.info(txid)
                request.session["txid"] = txid
                # Wait for the transaction to be confirmed
                wait_for_confirmation(algodclient, txid)
                messages.success(request, txid)
                if request.session["acceptid"] == "noid":
                    logging.info("there is no accept id")
                else:
                    accept_id = request.session["acceptid"]
                    request_obj = TokenRequests.objects.get(
                        unique_id=accept_id
                    )  # pylint: disable=E1101
                    request_obj.is_accepted = True
                    request_obj.save()
                    print("accepted")
                    request.session["acceptid"] = "noid"
                return redirect("send")
            except:  # pylint: disable=W0702,C0103

                def write_json(new_data, filename="static/JsonFile/txn_failed.json"):
                    with open(filename, "r+") as file:
                        file_data = json.load(file)
                        file_data.append(new_data)
                        file.seek(0)
                        json.dump(file_data, file, indent=4)

                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                Add_failed_msg = {"datetime": dt_string, "status": "failed"}
                write_json(Add_failed_msg)
                tid = request.session["txid"]
                messages.error(request, tid)
                return redirect("send")
        else:
            messages.error(request, "Incorrect Password")
    notification_paginator = Paginator(trxndata, 5)
    notification_page_number = request.GET.get("page")
    notification_page_obj = notification_paginator.get_page(notification_page_number)
    total_balance = format((int(assets_token) / 1000), ".3f")
    cent = format(float(total_balance) / 10, ".2f")
    balance["inUSD"] = cent
    balance["addDays"] = addDays()
    if "favid" in request.GET:
        pid = request.GET.get("favid")
        balance["favid"] = pid
    if request.session["acceptid"] == "noid":
        logging.info("there is no accept id")
    else:
        accept_id = request.session["acceptid"]
        request_obj = TokenRequests.objects.get(
            unique_id=accept_id
        )  # pylint: disable=E1101
        balance["request_obj"] = request_obj
    balance["trxn_data"] = notification_page_obj
    session_net = request.session["name"]
    balance["session_net"] = session_net
    balance["role"] = user_role
    fav_con = Contacts.objects.filter(
        user__username=request.user.username
    )  # pylint: disable=E1101
    balance["contacts"] = fav_con
    filtered_msg = msg_notif(request)
    balance["filtered_msg"] = filtered_msg
    count_msg = Messages.objects.filter(
        User=request.user, is_read=False
    ).count()  # pylint: disable=E1101
    balance["count_msg"] = count_msg
    current_user = request.user
    count_request = TokenRequests.objects.filter(
        recipient=current_user, is_rejected=False, is_accepted=False
    ).count()  # pylint: disable=E1101,C0301
    balance["count_request"] = count_request
    notif_request = request_notif(request)
    balance["notif_request"] = notif_request
    return render(request, "send.html", balance)


@login_required(login_url="signin")
def request_m(request):  # pylint: disable=C0103,R0914,R0912,R0915
    """_summary_

    It will run iff user is logged in.
    Otherwise you will be redirected to signin page.

    Args: request (object): request object

    Returns: renders request.html
    """
    request.session["report"] = ""
    request.session["test"] = "none"
    request.session["acceptid"] = "noid"
    add = str(request.user.Address)
    balance = user_details(request)
    if "favid" in request.GET:
        pid = request.GET.get("favid")
        balance["favid"] = pid
    fav_con = Contacts.objects.filter(
        user__username=request.user.username
    )  # pylint: disable=E1101
    balance["contacts"] = fav_con
    current_user = request.user
    get_request = (
        TokenRequests.objects.filter(recipient=current_user)
        .annotate(last=Max("date"))
        .order_by("-last")
    )  # pylint: disable=E1101
    send_request = (
        TokenRequests.objects.filter(sender=current_user)
        .annotate(last=Max("date"))
        .order_by("-last")
    )  # pylint: disable=E1101
    total_request = get_request | send_request
    balance["get_request"] = total_request
    user = get_user_model()
    from_user = request.user
    if request.method == "POST":
        address = request.POST.get("address")
        request_tokne = request.POST.get("amount")
        try:
            users_fav = user.objects.filter(Address=address).values("username")
            to_user = list(users_fav)[0]["username"]
            to_user = user.objects.get(username=to_user)
            TokenRequests.send_token(from_user, to_user, request_tokne)
            # redirect_url = request.build_absolute_uri()
            messages.success(request, "Request sent successfully")
            return HttpResponseRedirect("request")
        except:  # pylint: disable=W0702
            messages.warning(request, "This address is not registered with us")
            return redirect("request")
    else:
        HttpResponseBadRequest()
    if "Acceptid" in request.GET:
        acceptid = request.GET.get("Acceptid")
        # request_obj=TokenRequests.objects.get(unique_id=acceptid)
        request.session["acceptid"] = acceptid
        return redirect("send")
    if "declineid" in request.GET:
        rejectid = request.GET.get("declineid")
        request_obj = TokenRequests.objects.get(
            unique_id=rejectid
        )  # pylint: disable=E1101
        request_obj.is_rejected = True
        request_obj.save()
        logging.info("ok")
        return redirect("request")
    return render(request, "request.html", balance)


@login_required(login_url="signin")
def history(request):  # pylint: disable=C0103,R0914,R0912,R0915
    """_summary_

    It will run iff user is logged in.
    Otherwise you will be redirected to signin page.

    Args: request (object): request object

    Returns: renders history.html
    """
    request.session["report"] = ""
    request.session["test"] = "none"
    request.session["acceptid"] = "noid"
    request.session["search"] = ""
    request.session["startdate"] = ""
    request.session["enddate"] = ""
    add = str(request.user.Address)
    name = str(request.user.username)
    role = get_user_model().objects.get(username=request.user.username)
    if role.is_superuser:
        user_role = "admin"
    else:
        user_role = "user"
    if request.session["name"] == "mainnet":
        trxndata = trxn_notify_testnet(request)
        algord = PurestakeMainnet()
        algodclient = algord.algodclient
        account_info = algodclient.account_info(add)
        idx = 0
        for _ in account_info["assets"]:
            scrutinized_asset = account_info["assets"][idx]
            idx = idx + 1
            if scrutinized_asset["asset-id"] == asset_id_mainnet:
                assets_token = json.dumps(scrutinized_asset["amount"])
                break
        total_balance = format((int(assets_token) / 1000), ".3f")
        cent = format(float(total_balance) / 10, ".2f")
        trxn_data = []
        dbdata = admin_data.objects.filter(key="PureStake").values("values")
        algod_token = list(dbdata)[0]["values"]
        algod_address = "https://mainnet-algorand.api.purestake.io/idx2"
        purestake_token = {"X-API-Key": algod_token}
        acl = indexer.IndexerClient(algod_token, algod_address, headers=purestake_token)
        response = acl.search_transactions(address=add)
        amts = response["transactions"]
        sno = 0
        for amt in amts:
            cnfround = amt["confirmed-round"]
            sender = amt["sender"]
            round_time = amt["round-time"]
            tx_id = amt["id"]
            timestamp = int(round_time)
            dt_object = datetime.fromtimestamp(timestamp)
            fees = amt["fee"]
            fee = float(fees / 1000000)
            txn_type = amt.get("tx-type")
            if txn_type == "pay":
                amoun = amt["payment-transaction"]["amount"]
                amount = format(float(amoun / 1000000), ".3f")
                receiver = amt["payment-transaction"]["receiver"]
                if sender == add:
                    tnxtype = "Sent"
                else:
                    tnxtype = "Received Algo"
                sno = sno + 1
            elif txn_type == "acfg":
                receiver = "Asset " + str(amt["created-asset-index"])
                tnxtype = "NFT"
                amount = format(0.000, ".3f")
            else:
                asset_t = amt.get("asset-transfer-transaction")
                amoun = asset_t.get("amount")
                amount = format(amoun / 1000, ".3f")
                receiver = asset_t.get("receiver")
                if txn_type == "Pay":
                    tnxtype = "Pay"
                else:
                    if sender == add:
                        tnxtype = "Sent"
                    else:
                        tnxtype = "Received"
                sno = sno + 1
            txn_data = {
                "sno": sno,
                "id": tx_id,
                "cnfround": cnfround,
                "amount": amount,
                "receiver": receiver,
                "sender": sender,
                "fee": fee,
                "tnxtype": tnxtype,
                "time": dt_object,
            }
            trxn_data.append(txn_data)
    else:
        add = str(request.user.Address)
        name = str(request.user.username)
        # trxndata = trxn_notif_mainnet(request)
        trxndata = trxn_notify_testnet(request)
        algord = PurestakeTestnet()
        algodclient = algord.algodclient
        account_info = algodclient.account_info(add)
        idx = 0
        for _ in account_info["assets"]:
            scrutinized_asset = account_info["assets"][idx]
            idx = idx + 1
            if scrutinized_asset["asset-id"] == asset_id_testnet:
                assets_token = json.dumps(scrutinized_asset["amount"])
                break
        total_balance = format((int(assets_token) / 1000), ".3f")
        cent = format(float(total_balance) / 10, ".2f")
        trxn_data = []
        dbdata = admin_data.objects.filter(key="PureStake").values("values")
        algod_token = list(dbdata)[0]["values"]
        algod_address = "https://testnet-algorand.api.purestake.io/idx2"
        purestake_token = {"X-API-Key": algod_token}
        acl = indexer.IndexerClient(algod_token, algod_address, headers=purestake_token)
        response = acl.search_transactions(address=add)
        amts = response["transactions"]
        sno = 0
        for amt in amts:
            cnfround = amt["confirmed-round"]
            sender = amt["sender"]
            round_time = amt["round-time"]
            tx_id = amt["id"]
            timestamp = int(round_time)
            dt_object = datetime.fromtimestamp(timestamp)
            fees = amt["fee"]
            fee = float(fees / 1000000)
            txn_type = amt.get("tx-type")
            if txn_type == "pay":
                amoun = amt["payment-transaction"]["amount"]
                amount = format(float(amoun / 1000000), ".3f")
                receiver = amt["payment-transaction"]["receiver"]
                if sender == add:
                    tnxtype = "Sent"
                else:
                    tnxtype = "Received Algo"
                sno = sno + 1
            elif txn_type == "acfg":
                receiver = "Asset " + str(amt["created-asset-index"])
                tnxtype = "NFT"
                amount = format(0.000, ".3f")
            elif (
                txn_type == "axfer"
                and amt["asset-transfer-transaction"]["asset-id"] == asset_id_testnet
            ):
                asset_t = amt.get("asset-transfer-transaction")
                amoun = asset_t.get("amount")
                amount = format(amoun / 1000, ".3f")
                receiver = asset_t.get("receiver")
                if txn_type == "Pay":
                    tnxtype = "Pay"
                else:
                    if sender == add:
                        tnxtype = "Sent"
                    else:
                        tnxtype = "Received"
                sno = sno + 1
            txn_data = {
                "sno": sno,
                "id": tx_id,
                "cnfround": cnfround,
                "amount": amount,
                "receiver": receiver,
                "sender": sender,
                "fee": fee,
                "tnxtype": tnxtype,
                "time": dt_object,
            }
            trxn_data.append(txn_data)
    if request.method == "POST" and "search-id" in request.POST:
        s_data = request.POST.get("searchInput")
        request.session["search"] = s_data
        if s_data:
            search_data = []
            for data in trxn_data:
                if s_data in data["id"]:
                    search_data.append(data)
                trxn_data = search_data

    if request.method == "POST" and "search-date" in request.POST:
        start_date = request.POST.get("startdate")
        end_date = request.POST.get("enddate")
        if start_date and end_date:
            request.session["startdate"] = start_date
            request.session["enddate"] = end_date
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            converted = int(start_date.timestamp())
            end_date = datetime.strptime(end_date, "%Y-%m-%d") + dateT.timedelta(1)
            converted1 = int(end_date.timestamp())
            search_date = []
            for data in trxn_data:
                if data["time"].timestamp() in range(converted, converted1):
                    search_date.append(data)
            trxn_data = search_date
        else:
            return redirect("/history")
    paginator = Paginator(trxn_data, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    search_trxn = request.session["search"]
    logging.info(search_trxn)
    next_five = list(trxn_data)[:5]
    notification_paginator = Paginator(trxndata, 5)
    notification_page_number = request.GET.get("page")
    notification_page_obj = notification_paginator.get_page(notification_page_number)
    session_net = request.session["name"]
    filtered_msg = msg_notif(request)
    count_msg = Messages.objects.filter(User=request.user, is_read=False).count()
    current_user = request.user

    return render(
        request,
        "history.html",
        {
            # "notif_request": notif_request,
            "sno": sno,
            "trxn_data": notification_page_obj,
            "inUSD": cent,
            "balance": total_balance,
            "add": add,
            "name": name,
            "table": page_obj,
            "session_net": session_net,
            "filtered_msg": filtered_msg,
            "count_msg": count_msg,
            "search_trxn": search_trxn,
            "addDays": addDays(),
            "start_date": request.session["startdate"],
            "end_date": request.session["enddate"],
            "role": user_role,
        },
    )


@login_required(login_url="signin")
def settings(request):  # pylint: disable=R0914,R0912,R0915
    """_summary_

    It will run iff user is logged in.
    Otherwise you will be redirected to signin page.

    Args: request (object): request object

    Returns: renders settings.html
    """
    request.session["report"] = ""
    request.session["test"] = "none"
    request.session["acceptid"] = "noid"
    balance = user_details(request)
    if request.method == "POST":
        name = str(request.user.username)
        password = request.POST.get("password")
        repassword = request.POST.get("repassword")
        email = request.POST.get("email")
        current_password = request.POST.get("Currentpassword")
        if password == repassword:
            users = authenticate(request, username=name, password=current_password)
            if users is not None:  # pylint: disable=R1705
                user = get_user_model()
                user_setting = user.objects.get(username=request.user.username)
                if password == "":
                    logging.info("empty field")
                else:
                    user_setting.set_password(password)
                user_setting.email = email
                user_setting.save()
                if "image" in request.FILES:
                    img = request.FILES["image"]
                    user_setting.profile_pic = img
                    user_setting.save()
                messages.success(request, "Account Details Changed")
                login(request, user_setting)
                request.session["name"] = "testnet"
                return redirect("settings")
            else:
                messages.error(request, "Incorrect Password")
        else:
            messages.error(request, "Passwords do not match")
    return render(request, "settings.html", balance)


@login_required(login_url="signin")
def support(request):  # pylint: disable=R0914,R0912,R0915
    """_summary_

    It will run iff user is logged in.
    Otherwise you will be redirected to signin page.

    Args: request (object): request object

    Returns: renders support.html
    """
    request.session["report"] = ""
    request.session["test"] = "none"
    request.session["acceptid"] = "noid"
    add = str(request.user.Address)
    balance = user_details(request)
    user = get_user_model()
    # support Chat
    if add == "ACEVVEYURDJXSX2ASHIUUMJVG3XFNLKWA3Z7VTF6DGQ3KSPF6L7KEZKY6U":
        message = Support.get_messages(User=request.user)
        active_direct = None
        directs = None
        if message:
            msg = message[0]
            active_direct = msg["user"].username
            directs = Support.objects.filter(User=request.user, recipient=msg["user"])
        balance["directs"] = directs
        balance["messages"] = message
        balance["active_direct"] = active_direct

        if "favid" in request.GET:
            pid = request.GET.get("favid")
            users_fav = user.objects.filter(Address=pid).values(
                "username", "profile_pic"
            )
            to_user = list(users_fav)[0]["username"]
            to_user_profile = list(users_fav)[0]["profile_pic"]
            from_user = request.user
            directs_message = Support.objects.filter(
                User=from_user, recipient__username=to_user
            )
            directs_message.update(is_read=True)
            directs_msg = (
                Support.objects.filter(User=from_user, recipient__username=to_user)
                .annotate(last=Max("date"))
                .order_by("last")
            )
            logging.info(directs_msg)
            body = request.POST.get("body")
            if request.method == "POST":  # pylint: disable=R1705
                to_user = user.objects.get(username=to_user)
                Support.send_message(from_user, to_user, body)
                redirect_url = request.build_absolute_uri()
                return HttpResponseRedirect(redirect_url)
            else:
                HttpResponseBadRequest()
            add = str(request.user.Address)
            balance["direct_msg"] = directs_msg
            balance["sender"] = to_user
            balance["sender_pic"] = to_user_profile
            balance["pid"] = pid
    else:
        support_id = "ACEVVEYURDJXSX2ASHIUUMJVG3XFNLKWA3Z7VTF6DGQ3KSPF6L7KEZKY6U"
        users_fav = user.objects.filter(Address=support_id).values(
            "username", "profile_pic"
        )
        to_user = list(users_fav)[0]["username"]
        to_user_profile = list(users_fav)[0]["profile_pic"]
        from_user = request.user
        directs_message = Support.objects.filter(
            User=from_user, recipient__username=to_user
        )
        directs_message.update(is_read=True)
        directs_msg = (
            Support.objects.filter(User=from_user, recipient__username=to_user)
            .annotate(last=Max("date"))
            .order_by("last")
        )
        body = request.POST.get("body")
        if request.method == "POST":  # pylint: disable=R1705
            to_user = user.objects.get(username=to_user)
            Support.send_message(from_user, to_user, body)
            redirect_url = request.build_absolute_uri()
            return HttpResponseRedirect(redirect_url)
        else:
            HttpResponseBadRequest()
            add = str(request.user.Address)
            balance["direct_msg"] = directs_msg
            balance["sender"] = to_user
            balance["sender_pic"] = to_user_profile
    return render(request, "support.html", balance)


@login_required(login_url="signin")
def faq(request):  # pylint: disable=R0914,R0912,R0915
    """_summary_

    It will run iff user is logged in.
    Otherwise you will be redirected to signin page.

    Args: request (object): request object

    Returns: renders faq.html
    """
    request.session["report"] = ""
    request.session["test"] = "none"
    balance = user_details(request)
    return render(request, "faq.html", balance)


@login_required(login_url="signin")
def dashboard(request):  # pylint: disable=R0914,R0912,R0915
    """_summary_

    It will run iff user is logged in.
    Otherwise you will be redirected to signin page.

    Args: request (object): request object

    Returns: renders dashboard.html
    """
    request.session["report"] = ""
    request.session["test"] = "none"
    request.session["name"] = "testnet"
    last_login = get_user_model().objects.get(username=request.user.username)
    request.session["acceptid"] = "noid"
    session_net = "testnet"
    add = str(request.user.Address)
    name = str(request.user.username)
    net = NetAPI(request.session["name"])
    algodclient = net.data_data()
    account_info = algodclient.account_info(add)
    micro_algo = format(account_info.get("amount"))
    micro_algo_int = int(micro_algo)
    algos = micro_algo_int / 1000000
    idx = 0
    add = str(request.user.Address)
    name = str(request.user.username)
    if request.session["name"] == "testnet":
        trxndata = trxn_notify_testnet(request)
        algord = PurestakeTestnet()
        asset_id = asset_id_testnet
    else:
        trxndata = trxn_notif_mainnet(request)
        algord = PurestakeMainnet()
        asset_id = asset_id_mainnet
    algodclient = algord.algodclient
    account_info = algodclient.account_info(add)
    micro_algo = format(account_info.get("amount"))
    micro_algo_int = int(micro_algo)
    algos = micro_algo_int / 1000000
    idx = 0
    for _ in account_info["assets"]:
        scrutinized_asset = account_info["assets"][idx]
        idx = idx + 1
        if scrutinized_asset["asset-id"] == asset_id:
            assets_token = json.dumps(scrutinized_asset["amount"])
            break

    if request.method == "POST" and "testnet" in request.POST:
        request.session["name"] = "testnet"
        return redirect("dashboard")
    if request.method == "POST" and "mainnet" in request.POST:
        request.session["name"] = "mainnet"
        return redirect("dashboard")

    notification_paginator = Paginator(trxndata, 5)
    notification_page_number = request.GET.get("page")
    notification_page_obj = notification_paginator.get_page(notification_page_number)
    total_balance = format((int(assets_token) / 1000), ".3f")
    cent = format(float(total_balance) / 10, ".2f")
    balance = {
        "inUSD": cent,
        "balance": total_balance,
        "add": add,
        "name": name,
        "Algos": algos,
    }
    filtered_msg = msg_notif(request)
    balance["filtered_msg"] = filtered_msg
    count_msg = Messages.objects.filter(User=request.user, is_read=False).count()
    balance["count_msg"] = count_msg
    current_user = request.user
    count_request = TokenRequests.objects.filter(
        recipient=current_user, is_rejected=False, is_accepted=False
    ).count()
    role = get_user_model().objects.get(username=request.user.username)
    if role.is_superuser:
        user_role = "admin"
    else:
        user_role = "user"
    balance["count_request"] = count_request
    notif_request = request_notif(request)
    balance["notif_request"] = notif_request
    balance["trxn_data"] = notification_page_obj
    balance["session_net"] = session_net
    balance["lastLogin"] = last_login.last_login
    balance["addDays"] = addDays()
    balance["role"] = user_role
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make((add), image_factory=factory, box_size=10)
    stream = BytesIO()
    img.save(stream)
    balance["svg"] = stream.getvalue().decode()
    if request.method == "POST" and "addfav" in request.POST:
        user = get_user_model()
        contact_name = request.POST.get("name")
        contact_address = request.POST.get("Address")
        login_user = user.objects.get(username=request.user.username)
        users_fav = Contacts.objects.filter(
            user__username=request.user.username, contact_address=contact_address
        )
        if contact_address == add:
            messages.error(request, "You Can't Add Yourself As A Favorite")
        else:
            if users_fav.exists():
                messages.warning(request, "This Is Already One Of Your Favorite")
            else:
                try:
                    address = contact_address
                    p_k = decode_address(address)
                    addr = encode_address(p_k)
                    assert addr == address
                    logging.info("right Address")
                    try:
                        users_fav = user.objects.filter(Address=contact_address).values(
                            "profile_pic"
                        )
                        fav_img = list(users_fav)[0]["profile_pic"]
                        form = Contacts.objects.create(
                            user=login_user,
                            profile_pic=fav_img,
                            name=contact_name,
                            contact_address=contact_address,
                        )
                        form.save()
                        logging.info("contact save")
                        return redirect("dashboard")
                    except:
                        form = Contacts.objects.create(
                            user=login_user,
                            name=contact_name,
                            contact_address=contact_address,
                        )
                        form.save()
                        logging.info("contact save")
                        return redirect("dashboard")
                except:  # pylint: disable=W0702
                    messages.error(request, "Wrong Address")

    fav_con = Contacts.objects.filter(user__username=request.user.username)
    balance["contacts"] = fav_con
    # delete fav contact
    if "favid" in request.GET:
        pid = request.GET["favid"]
        prd = get_object_or_404(Contacts, user=request.user, contact_address=pid)
        prd.delete()
        return redirect("dashboard")

    return render(request, "dashboard.html", balance)


def verify(request):  # pylint: disable=R0914,R0912,R0915
    """_summary_

    Args:
        request (Object): request object

    Returns: renders the verify page
    """
    try:
        private_key, _ = account.generate_account()
        pas = format(mnemonic.from_private_key(private_key))
        passphrase = request.session["pas"]
        pas = passphrase.split()
        random_phrase = sample(pas, 5)
        logging.info(random_phrase)
        with open("allword.txt", "r", encoding="utf-8") as file:
            all_text = file.read()
            words = list(map(str, all_text.split()))
            random_word = sample(words, 10)
        random_keys = random_word + random_phrase
        shuffle_words = sample(random_keys, 15)
        list_to_str = " ".join([str(elem) for elem in shuffle_words])
        (
            word1,
            word2,
            word3,
            word4,
            word5,
            word6,
            word7,
            word8,
            word9,
            word10,
            word11,
            word12,
            word13,
            word14,
            word15,
        ) = list_to_str.split()
        random_fields = VerifyWords(
            word1,
            word2,
            word3,
            word4,
            word5,
            word6,
            word7,
            word8,
            word9,
            word10,
            word11,
            word12,
            word13,
            word14,
            word15,
        )
        holders = random_fields.verify_feilds()
        if request.method == "POST":
            p_1 = request.POST.get("word1")
            p_2 = request.POST.get("word2")
            p_3 = request.POST.get("word3")
            p_4 = request.POST.get("word4")
            p_5 = request.POST.get("word5")
            selected_words = [p_1, p_2, p_3, p_4, p_5]
            count = 0
            for i in range(0, 5):
                for j in range(0, 24):
                    if selected_words[i] == pas[j]:
                        count = count + 1
            if count == 5:  # pylint: disable=R1705
                messages.success(request, "Passphrase Verified")
                return redirect("create_wallet")
            else:
                messages.error(request, "Please Try Again")
                return redirect("verify")
    except:
        return redirect("get_pass")
    return render(request, "verify.html", holders)


def recover(request):
    """_summary_

    Args:
        request (Object): request object

    Returns: renders the recovery page
    """
    div = get_passphrase()
    if request.method == "POST":
        data = []
        for i in range(1, 26):
            data.append(request.POST.get("word" + str(i)))
        passphrase = " ".join([str(elem) for elem in data])
        try:
            mnemonic_phrase = passphrase
            privatekey = mnemonic.to_private_key(mnemonic_phrase)
            address = mnemonic.to_public_key(mnemonic_phrase)
            request.session["recover_memo"] = passphrase
            request.session["recover_addr"] = address
            request.session["recover_private"] = privatekey
            messages.success(request, "Your Account has been Recovered")
            return redirect("create_recovery")
        except:  # pylint: disable=W0702
            messages.error(request, "Wrong Passphrase! Please Try Again")
    return render(request, "recover.html", div)


def signin(request):  # pylint: disable=R0914,R0912,R0915
    """_summary_

    Args: request (object): request object

    Returns: renders login.html
    """
    cache.clear()
    user = get_user_model()
    # if request.user.is_authenticated:
    #     print("logged in")
    #     return redirect("dashboard")
    if request.method == "POST":
        name = request.POST.get("accname")
        pwd = request.POST.get("password")
        user = authenticate(request, username=name, password=pwd)
        if user is not None:
            check_user = get_user_model().objects.get(username=name)
            check_user_verify = Email_verify.objects.get(User=check_user)
            if check_user_verify.verify:
                login(request, user)
                if user.is_superuser:
                    request.session["name"] = "testnet"  # pylint: disable=R1705
                    return redirect("/admin")
                encrypted = str(request.user.passphrase)
                dcode32 = base32_decode(encrypted)
                passphrase = base64_decode(dcode32)
                private = str(request.user.privateKey)
                user_address = mnemonic.to_public_key(passphrase)
                # user_private = mnemonic.to_public_key(passphrase)
                algord = PurestakeTestnet()
                algodclient = algord.algodclient

                def print_asset_holding(algodclient, account_add, assetid):
                    """_summary_
                    Args:
                        algodclient: Instance of AlgodClient
                        account_add: Account address
                        assetid : Asset ID
                    """
                    account_info = algodclient.account_info(account_add)
                    idx = 0
                    for _ in account_info["assets"]:
                        scrutinized_asset = account_info["assets"][idx]
                        idx = idx + 1
                        if scrutinized_asset["asset-id"] == assetid:
                            logging.info(json.dumps(scrutinized_asset["amount"]))
                            break

                algod = PurestakeTestnet()
                algodclient = algod.algodclient
                dbdata = admin_data.objects.filter(key="AdminPhras").values("values")
                encrypted = list(dbdata)[0]["values"]
                dcode32 = base32_decode(encrypted)
                admin_memo = base64_decode(dcode32)
                account_private_key = mnemonic.to_private_key(admin_memo)
                account_public_key = mnemonic.to_public_key(admin_memo)
                params = algodclient.suggested_params()
                account_info = algodclient.account_info(user_address)
                holding = None
                idx = 0
                for _ in account_info["assets"]:
                    scrutinized_asset = account_info["assets"][idx]
                    idx = idx + 1
                    if scrutinized_asset["asset-id"] == asset_id_testnet:
                        logging.info("done")
                        holding = True
                        break
                if not holding:
                    # send algo
                    g_h = params.gh
                    first_valid_round = params.first
                    last_valid_round = params.last
                    fee = params.min_fee
                    send_amount = 500000
                    existing_account = account_public_key
                    send_to_address = user_address
                    t_x = transaction.PaymentTxn(
                        existing_account,
                        fee,
                        first_valid_round,
                        last_valid_round,
                        g_h,
                        send_to_address,
                        send_amount,
                        flat_fee=True,
                    )
                    signed_tx = t_x.sign(account_private_key)
                    tx_confirm = algodclient.send_transaction(signed_tx)
                    id = signed_tx.transaction.get_txid()
                    wait_for_confirmation(
                        algodclient, txid=signed_tx.transaction.get_txid()
                    )
                    # add asset
                    params = algodclient.suggested_params()
                    params.fee = 1000
                    params.flat_fee = True
                    txn = AssetTransferTxn(
                        sender=user_address,
                        sp=params,
                        receiver=user_address,
                        amt=0,
                        index=asset_id_testnet,
                    )
                    stxn = txn.sign(private)
                    txid = algodclient.send_transaction(stxn)
                    logging.info(txid)
                    wait_for_confirmation(algodclient, txid)
                    # send token
                    params = algodclient.suggested_params()
                    params.fee = 1000
                    params.flat_fee = True
                    txn = AssetTransferTxn(
                        sender=account_public_key,
                        sp=params,
                        receiver=user_address,
                        amt=1000000,
                        index=asset_id_testnet,
                    )
                    stxn = txn.sign(account_private_key)
                    txid = algodclient.send_transaction(stxn)
                    logging.info(txid)
                    wait_for_confirmation(algodclient, txid)
                print_asset_holding(algodclient, user_address, asset_id_testnet)

                request.session["name"] = "testnet"
                if "next" in request.GET:
                    return redirect(request.GET.get("next"))
                else:
                    return redirect("dashboard")
            else:
                messages.error(request, "Please Verify Your Email")
        else:
            messages.error(request, "Your Password or Username is Incorrect")
    return render(request, "login.html")


def get_pass(request):  # pylint: disable=R0914,R0912,R0915
    """_summary_

    Args: request (object): request object

    Returns: renders the get_pass.html page
    """
    private_key, address = account.generate_account()
    addr = format(address)
    private = format(private_key)
    pas = format(mnemonic.from_private_key(private_key))
    (
        word1,
        word2,
        word3,
        word4,
        word5,
        word6,
        word7,
        word8,
        word9,
        word10,
        word11,
        word12,
        word13,
        word14,
        word15,
        word16,
        word17,
        word18,
        word19,
        word20,
        word21,
        word22,
        word23,
        word24,
        word25,
    ) = pas.split()
    word_field = GetpassField(
        word1,
        word2,
        word3,
        word4,
        word5,
        word6,
        word7,
        word8,
        word9,
        word10,
        word11,
        word12,
        word13,
        word14,
        word15,
        word16,
        word17,
        word18,
        word19,
        word20,
        word21,
        word22,
        word23,
        word24,
        word25,
    )
    holders = word_field.getpass_words()
    request.session["pas"] = pas
    request.session["addr"] = addr
    request.session["private"] = private
    return render(request, "getPass.html", holders)


def create_wallet(request):  # pylint: disable=R0914,R0912,R0915
    """_summary_

    Args: request (object): request object

    Returns: renders the create_wallet.html page
    """
    try:
        unencrypted = request.session["pas"]
        encode64 = base64_encode(unencrypted)
        passphrase = base32_encode(encode64)
        address = request.session["addr"]
        private_key = request.session["private"]
        if request.method == "POST":
            user = get_user_model()
            name = request.POST.get("accname")
            email = request.POST.get("email")
            pwd = request.POST.get("password")
            if "image" in request.FILES:
                img = request.FILES["image"]
            try:
                detail = user.objects.create_user(
                    username=name,
                    password=pwd,
                    email=email,
                    passphrase=passphrase,
                    Address=address,
                    privateKey=private_key,
                    profile_pic=img,
                )
                detail.save()
                uid = uuid.uuid4()
                verify_email = Email_verify(User=detail, email_verify_token=uid)
                verify_email.save()
                subject = "Verify your email"
                message = (
                    "Please verify your email by clicking the link below \n"
                    + "https://wallet.mpayz.io//verifyAccount/"
                    + str(uid)
                )
                form_email = "MPayzToken@gmail.com"
                recipient_list = [email]
                send_mail(subject, message, form_email, recipient_list)
                messages.warning(
                    request,
                    "Thank for registering. Please verify your entered Email ID. We have an email to verify your entered email ID.",
                )
                return redirect("signin")
            except Exception:  # pylint: disable=W0702,W0703
                messages.error(request, "This account name is Taken")
    except:
        return redirect("get_pass")
    return render(request, "createWallet.html")


def create_recovery(request):
    """_summary_

    Args: request (object): request object

    Returns: renders the recovery page
    """
    passphrase = request.session["recover_memo"]
    address = request.session["recover_addr"]
    private_key = request.session["recover_private"]
    if request.method == "POST":
        try:
            user = get_user_model()
            name = request.POST.get("accname")
            email = request.POST.get("email")
            pwd = request.POST.get("password")
            if "image" in request.FILES:
                img = request.FILES["image"]
            try:
                detail = user.objects.create_user(
                    username=name,
                    password=pwd,
                    email=email,
                    passphrase=passphrase,
                    Address=address,
                    privateKey=private_key,
                    profile_pic=img,
                )
                detail.save()
                messages.success(request, "Your Account has been Added")
                return redirect("signin")
            except Exception:  # pylint: disable=W0702,W0703
                messages.error(request, "This account name is Taken")
        except Exception:  # pylint: disable=W0702,W0703
            messages.error(request, "Somthing went Wrong!")
    return render(request, "createrecovery.html")


def logoutpage(request):
    """_summary_

    Args: request (object): request object

     Returns: renders send.html
    """
    if request.user.is_authenticated:
        logout(request)
    return redirect("signin")


def user_task():
    """_summary_
    get all transactions from algorand server
    """

    user_address = []
    user_data = get_user_model().objects.all().values("Address")
    for i in range(len(user_data)):
        Address = user_data[i]["Address"]
        user_address.append(Address)

    user_trxn = []
    dbdata = admin_data.objects.filter(key="PureStake").values("values")
    algod_token = list(dbdata)[0]["values"]
    algod_address = "https://testnet-algorand.api.purestake.io/idx2"
    purestake_token = {"X-API-Key": algod_token}
    acl = indexer.IndexerClient(algod_token, algod_address, headers=purestake_token)
    for i in range(len(user_address)):
        add = user_address[i]
        response = acl.search_transactions(address=user_address[i])
        amts = response["transactions"]
        for amt in amts:
            sender = amt["sender"]
            round_time = amt["round-time"]
            timestamp = int(round_time)
            dt_object = datetime.fromtimestamp(timestamp)
            datetime_serial = datetime.strftime(dt_object, "%Y-%m-%d %H:%M:%S")
            txn_type = amt.get("tx-type")
            if sender != add and txn_type == "axfer":
                asset_t = amt.get("asset-transfer-transaction")
                amoun = asset_t.get("amount")
                amount = format(amoun / 1000, ".3f")
                trxn_hist = {"datetime": datetime_serial, "amount": amount}
                user_trxn.append(trxn_hist)

    json_path = "trxn.json"
    with open("static/JsonFile/" + (json_path), "w+", encoding="utf-8") as outfile:
        json.dump(user_trxn, outfile)

    # get all user info from database
    user_data = list(
        get_user_model().objects.all().values("id", "last_login", "date_joined")
    )
    user_all_data = []
    for i in range(len(user_data)):
        id = user_data[i]["id"]
        if user_data[i]["last_login"] is not None:
            lastlogin = user_data[i]["last_login"]
            last_login = datetime.strftime(lastlogin, "%Y-%m-%d %H:%M:%S")
        else:
            last_login = "null"
        datejoined = user_data[i]["date_joined"]
        date_joined = datetime.strftime(datejoined, "%Y-%m-%d %H:%M:%S")
        user_all_data.append(
            {"id": id, "last_login": last_login, "date_joined": date_joined}
        )
    json_path = "user.json"
    with open("static/JsonFile/" + (json_path), "w+", encoding="utf-8") as outfile:
        json.dump(user_all_data, outfile)

    # get all requets from database
    all_user_request = []
    user_request = list(
        TokenRequests.objects.all()
        .values("token", "is_rejected", "is_accepted", "date")
        .order_by("date")
    )
    for i in range(len(user_request)):
        token = user_request[i]["token"]
        is_rejected = user_request[i]["is_rejected"]
        is_accepted = user_request[i]["is_accepted"]
        date = user_request[i]["date"]
        date = datetime.strftime(date, "%Y-%m-%d %H:%M:%S")
        if is_rejected is True and is_accepted is False:
            status = "Rejected"
        elif is_rejected is False and is_accepted is True:
            status = "Accepted"
        else:
            status = "Pending"
        all_user_request.append({"token": token, "status": status, "date": date})
    json_path = "request.json"
    with open("static/JsonFile/" + (json_path), "w+", encoding="utf-8") as outfile:
        json.dump(all_user_request, outfile)


@api_view(["GET"])
def make_report(request):
    """_summary_
    make report API
    """
    report_data = UserReport()
    return Response(report_data)
