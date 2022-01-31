from __future__ import annotations
from email.policy import default

from io import TextIOWrapper
from typing import List
import os

from rich.console import Console as RichConsole
from rich.table import Table as RichTable
import click
import more_itertools

from . import arcade, draw


console = RichConsole()
jwt = os.getenv("ARCADE_JWT")

if jwt is None:
    console.print("[red]ERROR: you need to set [yellow]ARCADE_JWT[/yellow] env var[/red]")
    exit(1)

def display_stars(stars: List[arcade.Star]) -> None:
    table = RichTable()
    table.add_column("x", style="yellow")
    table.add_column("y", style="yellow")
    table.add_column("star type", style="cyan")

    for star in stars:
        x, y, type_ = star
        table.add_row(str(x), str(y), str(type_))
    
    console.print(table)


@click.group()
def arcade_cli():
    pass


@arcade_cli.command(name="show")
@click.option("--force-print", is_flag=True, help="print stars, even if there is a lot")
@click.argument("file", type=click.File("r"))
def show_star_file(file: TextIOWrapper, force_print: bool) -> None:
    """
    Show stars in file.

    \b
    Arguments:
        file: file to render
    """
    stars = arcade.load_stars_from_file(file)

    if len(stars) > 1000 and not force_print:
        console.print("[red]to many stars, not going to print them[/red]")
        console.print("[red]if you do want to print them, use [yellow]--force-print[/yellow] flag[/red]")
    else:
        display_stars(stars)

    console.print(f"amount of stars: [bold cyan]{len(stars)}[/bold cyan]")

@arcade_cli.command(name="download")
@click.option("--show", is_flag=True, help="print stars to terminal")
@click.argument("output_file", type=click.File("w+"))
@click.argument("bucket", type=int)
def download_stars(bucket: int, output_file: TextIOWrapper | None, show: bool) -> None:
    """
    Load stars from your extension buckets.

    \b
    Arguments:
        bucket: a number for your bucket.
        output_file: file to store stars in
    """

    stars = arcade.get_stars_from_bucket(jwt, bucket)

    if isinstance(stars, str):
        console.print(f"[red]ERROR:[/red] [yellow]{stars}[/yellow]")
        return

    if show:
        display_stars(stars)

    console.print(f"loaded [bold cyan]{len(stars)}[/bold cyan] stars from save bucket [bold cyan]{bucket}[/bold cyan]")

    if output_file is not None:
        arcade.store_stars_in_file(stars, output_file)
        console.print("saved stars to file.")

@arcade_cli.command(name="upload")
@click.argument("file", type=click.File("r"))
@click.argument("bucket", type=int)
def upload_stars(file: TextIOWrapper, bucket: int) -> None:
    """
    Upload stars to your extension buckets.

    Arguments:
        file: file containing stars
        bucket: bucket to upload to
    """
    stars = arcade.load_stars_from_file(file)
    arcade.save_stars_to_bucket(jwt, bucket, stars)

    console.print(f"sent [bold cyan]{len(stars)}[/bold cyan] stars to save bucket [bold cyan]{bucket}[/bold cyan]")

@arcade_cli.command(name="draw")
@click.argument("file", type=click.File("r"))
def draw_stars(file: TextIOWrapper) -> None:
    """
    Draw stars in the sky!

    Arguments:
        file: .csv with stars to draw :D 
    """
    stars = arcade.load_stars_from_file(file)

    console.print(f"sending [yellow]{len(stars)}[/yellow] stars to the arcade in total")

    for stars_group in more_itertools.chunked(stars, 9000):
        console.print(f"sending [yellow]{len(stars_group)}[/yellow] stars to the arcade")
        arcade.draw_in_stars(jwt, stars_group)
    
    console.print("[green]DONE[/green]")

@arcade_cli.command(name="modify")
@click.option("-s", "--scale", type=float, default=1, help="scale, for example to half the size --scale 2")
@click.option("-x", "--x-offset", type=float, default=0, help="move stars on x-axsis")
@click.option("-y", "--y-offset", type=float, default=0, help="move stars on y-axsis")
@click.argument("input_file", type=click.File("r"))
@click.argument("output_file", type=click.File("w+"))
def modify_stars(input_file: TextIOWrapper, output_file: TextIOWrapper, scale: float, x_offset: float, y_offset: float) -> None:
    """
    Modify stars in a file

    Arguments:
        input_file: source file of stars
        output_file: file to save stars in
    """
    stars = arcade.load_stars_from_file(input_file)
    stars = [
        (x / scale + x_offset, y / scale + x_offset, type_)
        for x, y, type_ in stars
    ]

    arcade.store_stars_in_file(stars, output_file)

    console.print("modified stars")

@arcade_cli.group(name="render")
def render_group():
    """Draw stars based on given input."""


@render_group.command(name="math")
@click.option("--start", type=float, default=0, help="where the input to the formula should start")
@click.option("--end", type=float, default=1, help="where the input to the formula should end")
@click.option("--step", type=float, default=0.01, help="how much the input to the formula should be stepped by")
@click.option("--star", "--type", type=int, default=1, help="the star type to use")
@click.argument("output_file", type=click.File("w+"))
@click.argument("formula")
def render_math(output_file: TextIOWrapper, formula: str, start: float, end: float, step: float, star: int):
    """
    Render a math formula as stars.

    if you use another range than 0-1, after caulcating all positions will be scaled down to fit.

    \b
    Arguments:
        formula: formula to render, use x as the x pos
        output_file: file to store stars in
    """
    stars = draw.draw_formula(formula, start, end, step, star)
    arcade.store_stars_in_file(stars, output_file)