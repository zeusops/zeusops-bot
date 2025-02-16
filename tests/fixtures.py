"""Reusable test fixtures, that we may need between multiple tests"""

from zeusops_bot.models import ConfigFile, ModDetail

BASE_CONFIG: ConfigFile = {"game": {"scenarioId": "old-value", "mods": []}}

MODLIST: list[ModDetail] = [
    {"modId": "595F2BF2F44836FB", "name": "RHS - Status Quo", "version": "0.10.4075"},
    {"modId": "5EB744C5F42E0800", "name": "ACE Chopping", "version": "1.2.0"},
    {"modId": "60EAEA0389DB3CC2", "name": "ACE Trenches", "version": "1.2.0"},
]
