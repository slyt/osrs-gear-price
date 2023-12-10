# TODO: Load dataframe from pickle
# TODO: Calculate the price per stat for each item
# TODO: Plot price per stat for the highest stats for each stat category
import matplotlib.pyplot as plt
import pandas as pd

# open pickle file
df = pd.read_pickle("data/dataframe.pkl")


stats = [
    "attack_stab",
    "attack_slash",
    "attack_crush",
    "attack_magic",
    "attack_ranged",
    "defence_stab",
    "defence_slash",
    "defence_crush",
    "defence_magic",
    "defence_ranged",
    "melee_strength",
    "ranged_strength",
    "magic_damage",
]

# for each stat, calculate the price per stat for each item based on avgHighPrice an avgLowPrice
# new column name is stat + '_price_per_stat_low' and stat + '_price_per_stat_high'

# if NaN in either avgLowPrice or avgHighPrice column, use the other column
df["avgLowPrice"] = df["avgLowPrice"].fillna(df["avgHighPrice"])
df["avgHighPrice"] = df["avgHighPrice"].fillna(df["avgLowPrice"])
df["avgPrice"] = (df["avgLowPrice"] + df["avgHighPrice"]) / 2

for stat in stats:
    df[stat + "_price_per_stat_low"] = df["avgLowPrice"] / df[stat]
    df[stat + "_price_per_stat_high"] = df["avgHighPrice"] / df[stat]


# for each stat, calculate the average between the high and low price per stat
for stat in stats:
    df[stat + "_price_per_stat_avg"] = (
        df[stat + "_price_per_stat_low"] + df[stat + "_price_per_stat_high"]
    ) / 2

# get unique values for the slot column
slot_values = [
    "2h",
    "shield",
    "weapon",
    "body",
    "legs",
    "neck",
    "head",
    "feet",
    "ring",
    "hands",
    "cape",
    "ammo",
]

# for each stat, get the top 25 items for each slot and stat and their price per stat
for stat in stats:
    for slot in slot_values:
        print(f"stat: {stat} -- slot: {slot}")
        # get the top items for each slot
        df_top = df[df["slot"] == slot].sort_values(by=[stat], ascending=False).head(25)
        # only show in df if the stat is greater than 0
        df_top = df_top[df_top[stat] > 0]
        # print the top 10 items for each slot
        stat_price_per_stat_low = stat + "_price_per_stat_low"
        stat_price_per_stat_high = stat + "_price_per_stat_high"
        price_per_stat_avg = stat + "_price_per_stat_avg"
        print(
            df_top[
                [
                    "name",
                    "id",
                    stat,
                    "avgHighPrice",
                    "avgLowPrice",
                    "avgPrice",
                    price_per_stat_avg,
                ]
            ]
        )
        print()
        # visualize the top 25 items for each slot
        if df_top.empty:
            print(f"df_top is empty for stat: {stat} and slot: {slot}")
        else:
            fig, ax = plt.subplots(figsize=(10, 10))
            df_top.plot(
                ax=ax,
                x="name",
                y=[price_per_stat_avg, stat],
                kind="barh",
                title=f"Top {slot} items by {stat} price per stat",
            )
            ax.set_xlabel(f"{stat} price per stat", fontsize=12)
            ax.set_ylabel("Item Name", fontsize=12)
            ax.set_xscale("log")
            plt.tight_layout()

            # annotate each bar with its value
            for p in ax.patches:
                ax.annotate(
                    f"{p.get_width():,.0f}", (p.get_width() * 1.005, p.get_y() * 1.005)
                )

            plt.show()
