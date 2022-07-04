import json
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as font_manager


def RA_plot():
    def load_data(token_name):
        with open("../data/risk_result/Result_%s.json" % (token_name), "r") as f:
            data = json.load(f)

        y = data["riskAmount_axis"][-2365855:]

        return y

    # load data
    s_block = 10570485
    e_block = 12936339
    x = [i for i in range(e_block - s_block + 1)]

    y_dai = [y / 10e18 for y in load_data("DAI")]
    y_usdc = [y / 10e6 for y in load_data("USDC")]
    y_usdt = [y / 10e6 for y in load_data("USDT")]

    # plot setting
    fig, ax1 = plt.subplots(figsize=(10, 10))
    ax1.yaxis.grid()  # horizontal lines
    # width = 0.15

    font = font_manager.FontProperties(
        family="Times New Roman",
        #    weight='bold',
        style="normal",
        size=24,
    )
    legend_font = font_manager.FontProperties(
        family="Times New Roman",
        #    weight='bold',
        style="normal",
        size=28,
    )
    y_tick_font = font_manager.FontProperties(
        family="Times New Roman",
        #    weight='bold',
        style="normal",
        size=24,
    )

    # plotting
    ax1.plot(x, y_dai, color="#F3B836", linewidth=4.0)
    ax1.plot(x, y_usdc, color="#2A77CA", linewidth=1.5)
    ax1.plot(x, y_usdt, color="#50AF95", linewidth=0.5)

    # formating
    x_ticks = [0, 2365854 - 1]
    x_ticklabels = ["10570485" + "\n (2020-08-01)", "12936339" + "\n (2021-07-31)"]
    y_ticks = np.arange(0, 3.3e8, 8e7)
    y_ticklabels = ["0", "80", "160", "240", "320"]

    ax1.set_xticks(x_ticks)
    ax1.set_xticklabels(x_ticklabels, fontproperties=font)
    ax1.set_yticks(y_ticks)
    ax1.set_yticklabels(y_ticklabels, fontproperties=y_tick_font)

    ax1.set_ylabel("Token Amount (Million)", fontname="Times New Roman", fontsize=24)
    ax1.set_xlabel("Block Number", fontname="Times New Roman", fontsize=24)

    ax1.legend(
        ["DAI", "USDC", "USDT"],
        prop=legend_font,
    )

    plt.savefig("../figures/RA.pdf")


def RL_plot_single():
    # load data
    def load_data(token_name):
        with open("./risk_result/DistributionInfo_%s.json" % (token_name), "r") as f:
            data = json.load(f)
        y_no_risk = data["noRisk"][:-1]
        y_low_risk = data["lowRisk"][:-1]
        y_high_risk = data["highRisk"][:-1]
        return y_no_risk, y_low_risk, y_high_risk

    s_block = 10570485
    e_block = 12936339
    x = [i for i in range(e_block - s_block + 1)]
    y_dai_no, y_dai_low, y_dai_high = load_data("DAI")
    y_usdc_no, y_usdc_low, y_usdc_high = load_data("USDC")
    y_usdt_no, y_usdt_low, y_usdt_high = load_data("USDT")

    # plot setting
    fig, axs = plt.subplots(3, 1, figsize=(10, 10))
    ax_dai = axs[0]
    ax_usdt = axs[1]
    ax_usdc = axs[2]
    ax_dai.yaxis.grid()
    ax_usdt.yaxis.grid()
    ax_usdc.yaxis.grid()
    # plt.figure(frameon=False, figsize=(16, 8), dpi=95)

    font = font_manager.FontProperties(
        family="Times New Roman",
        #    weight='bold',
        style="normal",
        size=24,
    )
    legend_font = font_manager.FontProperties(
        family="Times New Roman",
        #    weight='bold',
        style="normal",
        size=28,
    )
    y_tick_font = font_manager.FontProperties(
        family="Times New Roman",
        #    weight='bold',
        style="normal",
        size=24,
    )

    # plotting
    ax_dai.plot(x, y_dai_no, color="tab:green", linewidth=4.0, ls="-.")
    ax_dai.plot(x, y_dai_low, color="tab:orange", linewidth=4.0, ls="--")
    ax_dai.plot(x, y_dai_high, color="tab:red", linewidth=4.0, ls="-")

    ax_usdt.plot(x, y_usdt_no, color="tab:green", linewidth=4.0, ls="-.")
    ax_usdt.plot(x, y_usdt_low, color="tab:orange", linewidth=4.0, ls="--")
    ax_usdt.plot(x, y_usdt_high, color="tab:red", linewidth=4.0, ls="-")

    ax_usdc.plot(x, y_usdc_no, color="tab:green", linewidth=4.0, ls="-.")
    ax_usdc.plot(x, y_usdc_low, color="tab:orange", linewidth=4.0, ls="--")
    ax_usdc.plot(x, y_usdc_high, color="tab:red", linewidth=4.0, ls="-")

    # formating
    x_ticks = [
        0,
        # 473171,
        # 946342,
        # 1419513,
        # 1892684,
        2365854 - 1,
    ]
    x_ticklabels = [
        "10570485" + "\n (2020-08-01)",
        # "11043656",
        # "11516827",
        # "11989998",
        # "12463169",
        "12936339" + "\n (2021-07-31)",
    ]

    ax_dai.set_xticks(())
    ax_dai.set_yticks(np.arange(0, 200e3 + 1, 50e3))
    ax_dai.set_yticklabels(["0", "50", "100", "150", "200"], fontproperties=y_tick_font)

    ax_usdc.set_xticks(x_ticks)
    ax_usdc.set_xticklabels(x_ticklabels, fontproperties=font)
    ax_usdc.set_yticks(np.arange(0, 600e3 + 1, 150e3))
    ax_usdc.set_yticklabels(
        ["0", "150", "300", "450", "600"], fontproperties=y_tick_font
    )

    ax_usdt.set_xticks(())
    ax_usdt.set_yticks(np.arange(0, 800e3 + 1, 200e3))
    ax_usdt.set_yticklabels(
        ["0", "200", "400", "600", "800"], fontproperties=y_tick_font
    )

    ax_dai.set_ylabel("User Count (K)", fontname="Times New Roman", fontsize=24)
    ax_usdt.set_ylabel("User Count (K)", fontname="Times New Roman", fontsize=24)
    ax_usdc.set_ylabel("User Count (K)", fontname="Times New Roman", fontsize=24)
    ax_usdc.set_xlabel("Block Number", fontname="Times New Roman", fontsize=24)

    ax_dai.legend(["No Risk", "Low Risk", "High Risk"], prop=legend_font, loc=2)

    ax_dai.set_title("DAI", fontname="Times New Roman", fontweight="bold", size=24)
    ax_usdc.set_title("USDC", fontname="Times New Roman", fontweight="bold", size=24)
    ax_usdt.set_title("USDT", fontname="Times New Roman", fontweight="bold", size=24)

    # plt.show()
    plt.savefig("../figures/RL_single.pdf")


def RL_plot_total():

    # load data
    with open("../data/risk_result/DistributionInfoTotal.json", "r") as f:
        data = json.load(f)

    s_block = 10570485
    e_block = 12936339
    x = [i for i in range(e_block - s_block + 1)]
    y_no_risk = data["noRisk"]
    y_low_risk = data["lowRisk"]
    y_high_risk = data["highRisk"]

    # plot setting
    fig, ax1 = plt.subplots(figsize=(16, 9))
    ax1.yaxis.grid()  # horizontal lines

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

    # plotting
    ax1.plot(x, y_no_risk, color="tab:green", linewidth=4.0)
    ax1.plot(x, y_low_risk, color="tab:orange", linewidth=4.0)
    ax1.plot(x, y_high_risk, color="tab:red", linewidth=4.0)

    # formating
    x_ticks = [0, 473171, 946342, 1419513, 1892684, 2365854 - 1]
    x_ticklabels = [
        "10570485" + "\n (2020-08-01)",
        "11043656",
        "11516827",
        "11989998",
        "12463169",
        "12936339" + "\n (2021-07-31)",
    ]

    ax1.set_xticks(x_ticks)
    ax1.set_xticklabels(x_ticklabels, fontproperties=font)

    ax1.set_ylabel("Token Amount (Million)", fontname="Times New Roman", fontsize=20)
    ax1.set_xlabel("Block Number", fontname="Times New Roman", fontsize=20)

    ax1.legend(
        ["No Risk", "Low Risk", "High Risk"],
        prop=legend_font,
    )

    plt.show()
    plt.savefig("../figures/RL_total.pdf")


# RL_plot_single()
# RA_plot()
# RL_plot_total()
