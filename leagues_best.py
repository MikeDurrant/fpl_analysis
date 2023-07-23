#import libs
import sys
import asyncio


import aiohttp
from prettytable import PrettyTable

from fpl import FPL


async def main():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        players = await fpl.get_players()

    top_performers = sorted(
        players, key=lambda x: x.goals_scored + x.assists, reverse=True)

    player_table = PrettyTable()
    player_table.field_names = ["Player", "£", "G", "A", "G + A", "PPG", "MINS", "COPNR", "PEN_MISSES", "SELECT_BY"]
    player_table.align["Player"] = "l"

    for player in top_performers[:50]:
        goals = player.goals_scored
        assists = player.assists
        ppg = player.points_per_game
        mins = player.minutes
        copnr = player.chance_of_playing_next_round
        pen_misses = player.penalties_missed
        select_by = player.selected_by_percent
        player_table.add_row([player.web_name, f"£{player.now_cost / 10}",
                            goals, assists, goals + assists, ppg, mins, copnr, pen_misses, select_by])

    print(player_table)

if __name__ == "__main__":
     if sys.version_info >= (3, 7):
         # Python 3.7+
         asyncio.run(main())
     else:
         # Python 3.6
         loop = asyncio.get_event_loop()
         loop.run_until_complete(main())