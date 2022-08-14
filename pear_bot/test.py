#  test.py

from pear_bot import bot_functions
import pandas as pd

test_prompts = [
    "prompt 1",
    "prompt 2",
    "prompt 3",
    "prompt 4",
    "prompt 5"
]
test_answers = [
    "test title 1",
    "test desc 1",
    "✅",
    "test title 2",
    "test desc 2"
]

test_msg_list = [
    123454321,
    "test title 1",
    "test desc 1",
    "✅",
    "test title 2",
    "test desc 2"
]


class TestMessage:
    id = 987654321


class TestUser:
    name = ""
    mention = ""


test_users = [TestUser() for i in range(8)]
for i, user in enumerate(test_users):
    user.id = i * 997654
    user.name = "user" + str(i)
    user.mention = ""


def test_export():
    print()
    bot_functions.export_data(TestMessage, test_answers)
    contents = pd.read_csv(r'root_message.csv')
    assert contents is not None


def test_import():
    print()
    contents = bot_functions.import_data()
    assert contents is not None


def test_create_prompt_embed():
    for i, prompt in enumerate(test_prompts):
        embed = bot_functions.create_prompt_embed(i, test_prompts, test_answers)
        if i == 0:
            assert embed.title == test_answers[0]


def test_set_pair_embed():
    print(" >> TESTED WITH USER LIST LENGTH OF " + str(len(test_users)))
    embed = bot_functions.set_pair_embed(test_users, test_msg_list)
    if len(test_users) > 2:
        assert embed.title == test_msg_list[4]
        assert embed.description is not None


def test_config_fields():
    for i, prompt in enumerate(test_prompts):
        embed = bot_functions.create_prompt_embed(i, test_prompts, test_answers)
        #  config = bot_functions.config_fields(i, embed, test_answers)
        if i == 0:
            assert embed.title == test_answers[0]
        elif i == 1 or i == 2 or i == 3:
            assert embed.title == test_answers[0]
            assert embed.fields.count(1) is not None
        else:
            assert embed.title == test_answers[0]
            assert embed.fields.count(2) is not None
