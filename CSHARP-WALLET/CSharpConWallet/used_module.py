"""This module provides all the required packages"""

from random import sample
from io import BytesIO
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from algosdk import mnemonic, account, transaction
from algosdk.v2client import algod, indexer
from algosdk.encoding import decode_address, encode_address
from algosdk.future.transaction import (
    wait_for_confirmation,
    AssetTransferTxn,
    AssetConfigTxn,
)
import qrcode
import qrcode.image.svg
from CSharpConWallet.field import (
    get_passphrase,
    PurestakeTestnet,
    PurestakeMainnet,
    VerifyWords,
    GetpassField,
    NetAPI,
    UserReport,
)
from CSharpConWallet.models import (
    FAQs,
    Contacts,
    Messages,
    TokenRequests,
    Support,
    Email_verify,
    admin_data,
    HealthRecords,
)
from CSharpConWallet.forms import AddContactForms
