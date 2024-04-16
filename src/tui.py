import os
from rich.console import Console
from rich.table import Table, Column


class Tui:
    def __init__(self):
        self.console = Console()
        self.status = None

    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_title(self, title):
        self.console.print("{title}\n".format(title=title))

    def list_menu_options(self, options):
        self.console.print("[blue bold underline]Menu")
        self.console.print('    '.join(
            ["[violet bold]{input}[/violet bold]) {label}".format(
                input=option[0],
                label=option[1]
            ) for option in options]
        ))
        self.console.print("\nMenu format: \"[violet bold]<selection>[/violet bold]\", vote format: \""
                           "[violet bold]<option>[/violet bold] [violet bold]<weight>[/violet bold]\"", end=': ')

    def list_presets(self, presets):
        self.console.print("[blue bold underline]Choose preset")

        for preset in presets:
            self.console.print(
                "[violet bold]{index}[/violet bold]) {title}".format(
                    index=preset["index"]+1,
                    title=preset["title"]
                ), highlight=False
            )

    def list_options(self, options):
        self.console.print("[blue bold underline]Options")

        for option in options:
            self.console.print(
                "[violet bold]{id}[/violet bold]) {name}".format(
                    id=option.id,
                    name=option.name
                ), highlight=False
            )

        self.console.print("")

    def list_weights(self, weights):
        self.console.print("[blue bold underline]Weights")

        for weight in weights:
            self.console.print(
                "[violet bold]{id}[/violet bold]) {name}".format(
                    id=weight.id,
                    name=weight.name
                ), highlight=False
            )

        self.console.print()

    def print_results(self, results):
        table = Table(
            Column(header="Place", justify="center"),
            Column(header="Name", justify="left"),
            Column(header="Score", justify="center"),
            title="Results"
        )

        for result in results:
            table.add_row(str(result.place), str(result.name), str(result.score))

        self.console.print(table)
        self.console.print()

    def print_votes_by_weight(self, results):
        table = Table(
            Column(header="Name", justify="center"),
            Column(header="Weight", justify="left"),
            Column(header="Votes", justify="center"),
            title="Votes by weight"
        )

        for result in results:
            table.add_row(str(result.name), str(result.weight), str(result.votes_count))

        self.console.print(table)
        self.console.print()

    def print_status_message(self):
        if self.status is None:
            return

        if self.status['success'] is True:
            self.console.print("[green]{}\n".format(self.status['message']))
        else:
            self.console.print("[red]{}\n".format(self.status['message']))

        self.status = None
