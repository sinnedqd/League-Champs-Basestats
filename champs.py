from collections import OrderedDict
from operator import itemgetter
from pytest_bdd import scenarios, when, then
from riotwatcher import LolWatcher
import pytest

lol_watcher = LolWatcher('RGAPI-ff1d3c7a-90c9-4e4b-954c-404ab6543f55')
scenarios('../DeployingWorking/League-Champs-Basestats/league_champion.feature')

my_region = 'na1'


def get_champ_data_list():
    versions = lol_watcher.data_dragon.versions_for_region(my_region)
    champions_version = versions['n']['champion']
    current_champ_list = lol_watcher.data_dragon.champions(champions_version)
    champion_data_list = OrderedDict(current_champ_list['data'])
    return champion_data_list

@pytest.fixture
@when('my API is queried with "<base_stat>"')
def best_champ_for_stat(base_stat):
    data_list = get_champ_data_list()
    sorted_list = OrderedDict()
    print(data_list)
    for champ in data_list:
        sorted_list[champ] = data_list[champ]['stats'][base_stat]
    sorted_list = sorted(sorted_list.items(), key = lambda x: int(x[1]), reverse=True)
    print(sorted_list[0])
    return sorted_list[0]

@then('the champion returned should be "<champion>"')
def base_stat_returns_champion(sorted_list, champion):
    assert sorted_list[0] == champion
