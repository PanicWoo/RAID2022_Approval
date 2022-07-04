# libraries and data
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from matplotlib import ticker
from matplotlib.font_manager import FontProperties
import matplotlib.font_manager as font_manager
import matplotlib.ticker as mtick
import numpy as np
import json


def load_spender_sender_token_data():

    # conn, cur = psqlConnector().connect_approval()

    with open("./data/date_to_blk.json", "r") as f:
        date_to_blk = json.load(f)
    loaded_data = {}
    for date in date_to_blk:
        blk = date_to_blk[date]
        query = (
            "SELECT count(*), count(distinct spender), count(distinct sender), count(distinct token)\
            FROM txn_approval where blocknumber <= %s"
            % (blk)
        )

        cur.execute(query)
        records = cur.fetchall()
        conn.commit()
        (_, spender_count, sender_count, token_count) = records[0]

        break

    return


def plot_trend_staked_bar():
    from matplotlib import rc

    # process the data
    with open("./data/trend_mon.json", "r") as f:
        data = json.load(f)

    keys = list(data.keys())
    months = []
    bars_max = []
    bars_min = []
    bars_rest = []
    for key in keys:
        months.append(key[2:])
        bars_max.append(data[key]["Max"] * 1e-6)
        bars_min.append(data[key]["Min"] * 1e-6)
        bars_rest.append(data[key]["Rest"] * 1e-6)

    with open("./data/date_to_blk.json", "r") as f:
        date_to_blk = json.load(f)

    x_ticks = []
    for date in date_to_blk:
        if date[:7] in keys:
            x_ticks.append(date_to_blk[date])

    # Heights of bars1 + bars2
    bars = np.add(bars_max, bars_rest).tolist()

    # The position of the bars on the x-axis
    r = np.arange(len(months))

    # Names of group and bar width
    names = months
    barWidth = 1
    # fig = plt.figure(frameon=False, figsize=(16, 7.5), dpi=100)
    fig = plt.figure(frameon=False, figsize=(10, 8), dpi=100)
    plt.grid(axis="y")
    # Create green bars (middle), on top of the firs ones
    plt.bar(
        r,
        bars_min,
        bottom=bars,
        color="#2EA9DF",
        edgecolor="white",
        width=barWidth,
        label="Zero",
    )
    # Create green bars (middle), on top of the firs ones
    plt.bar(
        r,
        bars_rest,
        bottom=bars_max,
        color="#7DB9DE",
        edgecolor="white",
        width=barWidth,
        label="Other",
    )
    # Create brown bars
    plt.bar(
        r,
        bars_max,
        color="#006284",
        edgecolor="white",
        width=barWidth,
        label="Unlimited",
    )

    plt.axvline(51.5, color="red")
    plt.text(
        49,  # 50.5,
        7,
        "UniswapV2 Released (2020-05)",
        fontname="Times New Roman",
        weight="bold",
        color="black",
        rotation=90,
        fontsize=24,
    )

    # Custom X axis
    # plt.xticks(r, names, fontweight='bold')
    plt.xlabel("Block Number", fontname="Times New Roman", fontsize=26)
    plt.ylabel(
        # "Accumulative Count of Approval Transactions",
        "Approval Transaction Count (Million)",
        fontname="Times New Roman",
        fontsize=26,
    )

    # Show graphic
    # plt.show()
    plt.xticks(
        [r[0], r[10], r[21], r[32], r[43], r[54], r[-1]],
        # ["2016-02", "2016-12", "2017-11", "2018-10", "2019-09", "2020-08", "2021-07"],
        [
            x_ticks[0],  # str(x_ticks[0]) + "\n (2016-02-29)",
            x_ticks[10],
            x_ticks[21],
            x_ticks[32],
            x_ticks[43],
            x_ticks[54],
            x_ticks[-1],  # str(x_ticks[-1]) + "\n (2021-07-31)",
        ],
        rotation=0,
        fontname="Times New Roman",
        fontsize=20,
    )
    plt.yticks(
        [0, 5, 10, 15, 20, 25],
        ["0", "5", "10", "15", "20", "25"],
        fontname="Times New Roman",
        fontsize=20,
    )
    font = font_manager.FontProperties(
        family="Times New Roman",
        #    weight='bold',
        style="normal",
        size=26,
    )
    plt.legend(prop=font)

    plt.savefig("../sigmatric22_paper/pdfs/trend_mon.pdf")
    plt.savefig("./trend_mon.pdf")


def plot_entity_trend():
    with open("./data/trend_mon_entities.json", "r") as f:
        line_data = json.load(f)

    with open("./data/trend_ua_rate.json", "r") as f:
        bar_data = json.load(f)

    with open("./data/date_to_blk.json", "r") as f:
        date_to_blk = json.load(f)

    # x,y values
    x = np.arange(len(line_data))
    x_ticks = []
    mons = []
    y_bar_spender = []
    y_bar_sender = []
    y_bar_token = []
    y_line_spender = []
    y_line_sender = []
    y_line_token = []

    for mon in line_data:
        mons.append(mon)
        y_line_spender.append(line_data[mon]["Spender"])
        y_line_sender.append(line_data[mon]["Sender"])
        y_line_token.append(line_data[mon]["Token"])

    for mon in bar_data:
        y_bar_spender.append(bar_data[mon]["Spender"] * 100)
        y_bar_sender.append(bar_data[mon]["Sender"] * 100)
        y_bar_token.append(bar_data[mon]["Token"] * 100)

    for date in date_to_blk:
        if date[:7] in mons:
            x_ticks.append(date_to_blk[date])

    # settings
    width = 0.4
    colors = ["#FF5A5F", "#FFB400", "#007A87", "#FFAA91", "#7B0051"]
    font = font_manager.FontProperties(
        family="Times New Roman",
        #    weight='bold',
        style="normal",
        size=16,
    )
    legend_font = font_manager.FontProperties(
        family="Times New Roman",
        #    weight='bold',
        style="normal",
        size=20,
    )
    y_tick_font = font_manager.FontProperties(
        family="Times New Roman",
        #    weight='bold',
        style="normal",
        size=16,
    )

    # init plt
    fig, axs = plt.subplots(3, figsize=(16, 8))
    bar_spender_ax = axs[1]
    line_spender_ax = bar_spender_ax.twinx()
    bar_token_ax = axs[2]
    line_token_ax = bar_token_ax.twinx()
    bar_sender_ax = axs[0]
    line_sender_ax = bar_sender_ax.twinx()
    bar_spender_ax.yaxis.grid()
    bar_sender_ax.yaxis.grid()
    bar_token_ax.yaxis.grid()

    # plotting
    #    spender
    bar_spender_ax.bar(
        x,
        y_bar_spender,
        width,
        color=colors[1],
        label="UAR for Spender",
        # fill=False,
        hatch="//",
    )
    line_spender_ax.plot(
        x,
        y_line_spender,
        linestyle="-",
        marker="",
        color="tab:red",
        label="Accumulative Count of Spender",
    )
    #    token
    bar_token_ax.bar(
        x,
        y_bar_token,
        width,
        color=colors[2],
        label="UAR for Token",
        # fill=False,
        # hatch="+",
    )
    line_token_ax.plot(
        x,
        y_line_token,
        linestyle="-",
        marker="",
        color="tab:red",
        label="Accumulative Count of Token",
    )
    #    sender
    bar_sender_ax.bar(
        x,
        y_bar_sender,
        width,
        color="#1C6DD0",
        label="UAR for Sender",
        # fill=False,
        hatch="..",
    )
    line_sender_ax.plot(
        x,
        y_line_sender,
        linestyle="-",
        marker="",
        color="tab:red",
        label="Accumulative Count of Sender",
    )

    # Formating

    # ticks and labels
    #     Spender
    bar_spender_ax.set_xticks(())
    bar_spender_ax.set_yticks(np.arange(0, 110, 20))
    bar_spender_ax.set_yticklabels(
        ["0", "20", "40", "60", "80", "100"], fontproperties=y_tick_font
    )
    line_spender_ax.set_yticks(np.arange(0, 210000, 40000))
    line_spender_ax.set_yticklabels(
        ("0K", "40K", "80K", "120K", "160K", "200K"),
        fontproperties=y_tick_font,
        color="tab:red",
    )

    bar_spender_ax.set_ylabel("UAR (%)", fontname="Times New Roman", fontsize=20)
    line_spender_ax.set_ylabel(
        "#  of  Spender", fontname="Times New Roman", fontsize=20
    )
    #     Token
    # bar_token_ax.set_xticks(())
    bar_token_ax.set_xticks((x[0], x[10], x[21], x[32], x[43], x[54], x[-1]))
    bar_token_ax.set_xticklabels(
        (
            str(x_ticks[0]) + "\n (2016-02-29)",
            x_ticks[10],
            x_ticks[21],
            x_ticks[32],
            x_ticks[43],
            x_ticks[54],
            str(x_ticks[-1]) + "\n (2021-07-31)",
        ),
        fontproperties=font,
    )
    bar_token_ax.set_yticks(np.arange(0, 110, 20))
    # bar_token_ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    bar_token_ax.set_yticklabels(
        ["0", "20", "40", "60", "80", "100"], fontproperties=y_tick_font
    )
    line_token_ax.set_yticks(np.arange(0, 110000, 20000))
    line_token_ax.set_yticklabels(
        ("0K", "20K", "40K", "60K", "80K", "100K"),
        fontproperties=y_tick_font,
        color="tab:red",
    )
    bar_token_ax.set_ylabel("UAR (%)", fontname="Times New Roman", fontsize=20)
    line_token_ax.set_ylabel("#  of  Token", fontname="Times New Roman", fontsize=20)
    bar_token_ax.set_xlabel("Block Number", fontname="Times New Roman", fontsize=20)
    #     Sender
    bar_sender_ax.set_xticks(())
    bar_sender_ax.set_yticks(np.arange(0, 110, 20))
    bar_sender_ax.set_yticklabels(
        ["0", "20", "40", "60", "80", "100"], fontproperties=y_tick_font
    )
    line_sender_ax.set_yticks(np.arange(0, 6000000, 1000000))
    line_sender_ax.set_yticklabels(
        (" 0", "1M", "2M", "3M", "4M", "5M"),
        fontproperties=y_tick_font,
        color="tab:red",
    )
    # bar_sender_ax.set_xlabel("Block Number", fontname="Times New Roman", fontsize=20)
    bar_sender_ax.set_ylabel("UAR (%)", fontname="Times New Roman", fontsize=20)
    line_sender_ax.set_ylabel("#  of  Sender", fontname="Times New Roman", fontsize=20)

    # legend
    bar1, bar1_label = bar_sender_ax.get_legend_handles_labels()
    ln1, ln1_label = line_sender_ax.get_legend_handles_labels()
    bar_sender_ax.legend(
        bar1 + ln1, bar1_label + ln1_label, loc="upper center", prop=legend_font
    )

    bar2, bar2_label = bar_spender_ax.get_legend_handles_labels()
    ln2, ln2_label = line_spender_ax.get_legend_handles_labels()
    bar_spender_ax.legend(
        bar2 + ln2, bar2_label + ln2_label, loc="upper center", prop=legend_font
    )

    bar3, bar3_label = bar_token_ax.get_legend_handles_labels()
    ln3, ln3_label = line_token_ax.get_legend_handles_labels()
    bar_token_ax.legend(
        bar3 + ln3, bar3_label + ln3_label, loc="upper center", prop=legend_font
    )

    # plt.show()
    # plt.savefig("./trend_entities.pdf")
    # plt.savefig("./fixed_pdfs/trend_entities.pdf")


# plot_trend_staked_bar()
# plot_entity_trend()
