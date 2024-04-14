import toml
import os
import re
from peewee import *

from models import DATABASE_PATH, DATABASE, Info, Option, Weight, Vote
from tui import Tui

CONFIG_PATH = './../presets/warmup.toml'
PRESETS_DIR = '../presets'


class PyvoApp:

    def __init__(self):
        self.last_inserted_row = 0
        self.tui = Tui()
        self.preset = None

    def save_preset_file(self, path):
        self.last_inserted_row = Info.insert(
            key="file",
            value=path
        ).on_conflict(
            conflict_target=[Info.key],
            preserve=[Info.value]
        ).execute()

    def sync_info(self):
        if self.preset['title']:
            self.last_inserted_row = Info.insert(
                key="title",
                value=self.preset['title']
            ).on_conflict(
                conflict_target=[Info.key],
                preserve=[Info.value]
            ).execute()

    def sync_options(self):
        for index, option in enumerate(self.preset["options"]):
            self.last_inserted_row = Option.insert(
                id=index + 1,
                name=option["name"] if "name" in option else ""
            ).on_conflict(
                conflict_target=[Option.id],
                preserve=[Option.name]
            ).execute()

    def sync_weights(self):
        for index, weight in enumerate(self.preset["weights"]):
            self.last_inserted_row = Weight.insert(
                id=index + 1,
                name=weight["name"],
                weight=weight["weight"]
            ).on_conflict(
                conflict_target=[Weight.id],
                preserve=[Weight.name, Weight.weight]
            ).execute()

    def load_preset(self, preset_path):
        self.preset = toml.load(preset_path)

        self.sync_info()
        self.sync_options()
        self.sync_weights()

    # noinspection SpellCheckingInspection
    def run(self):
        if not os.path.exists(DATABASE_PATH):

            presets = [{
                'index': index,
                'file': preset_file,
                'title': toml.load("{dir}/{file}".format(dir=PRESETS_DIR, file=preset_file))["title"]
            } for index, preset_file in enumerate(os.listdir(PRESETS_DIR))]

            self.tui.clear_console()
            self.tui.list_presets(presets)
            selected_preset_index = int(input().split(' ')[0]) - 1

            DATABASE.create_tables([Info, Option, Weight, Vote])

            preset_path = "{dir}/{file}".format(dir=PRESETS_DIR, file=presets[selected_preset_index]['file'])
            self.load_preset(preset_path)
            self.save_preset_file(presets[selected_preset_index]['file'])

        exit_var = False
        while exit_var is False:
            self.tui.clear_console()

            title = Info.select(Info.value).where(Info.key == 'title').execute()

            if len(title) > 0:
                self.tui.print_title(title[0].value)

            self.tui.list_options(Option.select(Option.id, Option.name))
            self.tui.list_weights(Weight.select(Weight.id, Weight.name))
            self.tui.print_status_message()

            self.tui.list_menu_options([
                ('exit', 'Exit'),
                ('results', 'Results'),
                ('rmlast', 'Remove last vote'),
                ('relpreset', 'Reload preset')
            ])

            user_input = re.sub(r'\s+', ' ', str(input()).strip()).split(' ')
            self.tui.clear_console()

            if user_input[0].isnumeric():
                # If input is new vote
                if len(user_input) in (1, 2):
                    option, weight = None, None
                    if len(user_input) == 1:
                        self.tui.list_weights(Weight.select(Weight.id, Weight.name))
                        self.tui.console.print("Insert weight", end=': ')
                        user_input.append(input())

                    if len(user_input) == 2:
                        if user_input[0].isnumeric() and user_input[1].isnumeric():
                            option, weight = int(user_input[0]), int(user_input[1])

                    else:
                        self.tui.status = {
                            'message': "Invalid number of choices",
                            'success': False
                        }

                    if None not in (option, weight) and weight > 0 and option > 0:
                        with DATABASE.atomic():
                            try:
                                Weight.get(Weight.id == weight)
                                Option.get(Option.id == option)

                                inserted_row = Vote.insert(option_id=option, weight_id=weight).execute()
                                if inserted_row > self.last_inserted_row:
                                    self.tui.status = {
                                        'message': "Success (inserted vote: {no})".format(no=inserted_row),
                                        'success': True
                                    }
                                    self.last_inserted_row = inserted_row
                            except DoesNotExist:
                                self.tui.status = {
                                    'message': "Invalid choice",
                                    'success': False
                                }

                    else:
                        if None in (option, weight) or 0 in (weight, option):
                            self.tui.status = {
                                'message': "Invalid choice number",
                                'success': False
                            }
                else:
                    self.tui.status = {
                        'message': "Invalid number of parameters",
                        'success': False
                    }

            else:
                # If input command
                if user_input[0] == "exit":
                    return
                elif user_input[0] == "results":
                    results = (Option.select(Option.name, fn.SUM(fn.IFNULL(Weight.weight, 0)).alias('score'))
                               .join(Vote, JOIN.LEFT_OUTER)
                               .join(Weight, JOIN.LEFT_OUTER)
                               .group_by(Option.name)
                               .order_by(fn.SUM(Weight.weight).desc()))

                    for place, result in enumerate(results):
                        result.place = place + 1

                    self.tui.print_results(results)

                    votes_by_weight = (Weight.select(
                        Weight.name,
                        Weight.weight,
                        fn.COUNT(Vote.id).alias('votes_count')).join(Vote, JOIN.LEFT_OUTER).group_by(Weight.weight)
                    )

                    self.tui.print_votes_by_weight(votes_by_weight)

                    input()
                elif user_input[0] == "rpreset":
                    self.load_preset(self.preset)

                elif user_input[0] == "rmlast":
                    last_record = Vote.select().order_by(Vote.id.desc()).first()

                    if last_record:
                        last_record_id = last_record.id
                        last_record.delete_instance()
                        self.tui.status = {
                            'message': "Last vote removed (id: {})".format(last_record_id),
                            'success': True
                        }
                    else:
                        self.tui.status = {
                            'message': "No votes found",
                            'success': False
                        }

                elif user_input[0] == "relpreset":
                    file = Info.select(Info.value).where(Info.key == 'file').execute()

                    if len(title) > 0:
                        self.load_preset("{dir}/{file}".format(dir=PRESETS_DIR, file=file[0].value))

            self.tui.clear_console()

        exit(0)


if __name__ == '__main__':
    app = PyvoApp()
    app.run()
