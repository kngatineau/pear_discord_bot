#  test.py

from pear_bot import bot_functions
import pandas as pd
import math

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

test_colours = [
    0xff0000,
    0xffa700,
    0xfff400,
    0xa3ff00,
    0x2cba00
]


class TestMessage:
    id = 987654321


class TestUser:
    name = ""
    mention = ""


def generate_test_users(user_count):
    test_users = [TestUser() for i in range(user_count)]

    for i, user in enumerate(test_users):
        user.id = i * 997654
        user.name = "user" + str(i)
        user.mention = ""
    return test_users


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
    test_answers_loop = []
    for i, prompt in enumerate(test_prompts):
        test_answers_loop.append(test_answers[i])
        embed = bot_functions.create_prompt_embed(i, prompt, test_answers_loop)
        if len(test_answers_loop) < 5:
            assert embed.title == f"Configuration - Step {i + 1} of 5"
            assert embed.description == prompt
        else:
            assert embed.title == test_answers[0]
            assert embed.description == test_answers[1]


def test_pair_logic_even():
    pair = bot_functions.pair_logic(generate_test_users(8))
    assert pair.count('\U0001F538') == len(generate_test_users(8)) / 2

def test_pair_logic_odd():
    pair = bot_functions.pair_logic(generate_test_users(9))
    assert pair.count('\U0001F538') == math.ceil(len(generate_test_users(9)) / 2)


def test_set_pair_embed_gt_two():
    print(" >> TESTED WITH USER LIST LENGTH OF " + str(len(generate_test_users(8))))
    embed = bot_functions.set_pair_embed(generate_test_users(8), test_msg_list)
    if len(generate_test_users(8)) > 2:
        assert embed.title == test_msg_list[4]
        assert embed.description is not None


def test_set_pair_embed_lt_two():
    embed = bot_functions.set_pair_embed(generate_test_users(1), test_msg_list)
    if len(generate_test_users(1)) < 2:
        assert embed.description == "No pairings available. Try again when more users react to the host message."


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
