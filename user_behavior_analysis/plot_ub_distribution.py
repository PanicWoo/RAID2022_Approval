import json
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as font_manager


def read_filenames():
    with open("../data/ub_result/pairs.json", "r") as f:
        pairs = json.load(f)

    filenames = list(pairs)
    count = 0
    for f in pairs:
        count += pairs[f][-1]
    return filenames


def count_total():
    fns = read_filenames()
    total_count = 0
    user_list = []
    for fn in fns:
        with open("../data/ub_result/%s.json" % (fn), "r") as f:
            res = json.load(f)
            count = len(list(res))
            user_list += list(res)
            print(fn, " ", len(list(res)))
        total_count += count
    unique_total = len(list(set(user_list)))

    print(total_count)
    print(unique_total)


def statistic(filename):
    with open("../data/ub_result/%s.json" % (filename), "r") as f:
        res = json.load(f)
    one_to_one = 0
    one_to_one_UA = 0
    one_to_many = 0
    one_to_many_UA = 0
    many_to_one = 0
    many_to_many = 0
    only_approval = 0
    many_to_many_users = []
    one_to_one_users = []
    one_to_many_users = []
    only_approval_users = []
    user_count = 0
    for sender in res:
        if int(list(res[sender])[0]) > 12936339:
            continue
        user_count += 1
        a_count = 0
        t_count = 0
        for blk in res[sender]:
            a_count += (
                res[sender][blk]["UA"] + res[sender][blk]["ZA"] + res[sender][blk]["OA"]
            )
            t_count += res[sender][blk]["Transfer"]

        if res[sender][list(res[sender])[-1]]["Transfer"] >= 1:
            is_last_action_transfer = True
        else:
            is_last_action_transfer = False

        if res[sender][list(res[sender])[0]]["UA"] == 1:
            is_UA_first = True
        else:
            is_UA_first = False

        # if a_count == 1 and t_count == 1:
        #     one_to_one += 1
        #     if is_UA_first:
        #         one_to_one_UA += 1
        #         one_to_one_users.append(sender)
        # elif a_count == 1 and t_count > 1 and :
        if a_count == 1:
            if t_count == 1:
                one_to_one += 1
                if is_UA_first:
                    one_to_one_UA += 1
                    one_to_one_users.append(sender)
            elif t_count == 0:
                only_approval += 1
            else:
                one_to_many += 1
                if is_UA_first:
                    one_to_many_UA += 1
                    one_to_many_users.append(sender)
        else:
            if t_count == 0:
                only_approval += 1
            elif t_count == 1 and is_last_action_transfer:
                many_to_one += 1
            else:
                many_to_many += 1
                many_to_many_users.append(sender)

        if only_approval > 1:
            only_approval_users.append(sender)

    print(filename)
    print(user_count)
    print(
        "  ",
        "one_to_one: ",
        one_to_one,
        one_to_one * 100 / user_count,
        one_to_one_UA * 100 / one_to_one,
    )
    print(
        "  ",
        "one_to_many: ",
        one_to_many,
        one_to_many * 100 / user_count,
        one_to_many_UA * 100 / one_to_many,
    )
    print("  ", "only_approval: ", only_approval, only_approval * 100 / user_count)
    print("  ", "many_to_one: ", many_to_one, many_to_one * 100 / user_count)
    print("  ", "many_to_many: ", many_to_many, many_to_many * 100 / user_count)
    # print("  ", "one_to_one: ", one_to_one, one_to_one * 100 / len(list(res)))
    # print("  ", "one_to_many: ", one_to_many, one_to_many * 100 / len(list(res)))
    # print("  ", "only_approval: ", only_approval, only_approval * 100 / len(list(res)))
    # print("  ", "many_to_one: ", many_to_one, many_to_one * 100 / len(list(res)))
    # print("  ", "many_to_many: ", many_to_many, many_to_many * 100 / len(list(res)))
    if filename == "USDC_Compound":
        print("many_to_many", many_to_many_users[:5])
        print("one_to_many", one_to_many_users[:5])
        print("one_to_one", one_to_one_users[:5])
        print("only approval", only_approval_users[:5])

    print("  ", "total_users: ", len(list(res)))

    return {
        "one_to_one": one_to_one,
        "one_to_many": one_to_many,
        "many_to_one": many_to_one,
        "many_to_many": many_to_many,
        "only_approval": only_approval,
        "total": one_to_one + one_to_many + many_to_one + many_to_many + only_approval,
    }


def plot(filenames):
    # load and process data
    # init data
    x = np.arange(len(filenames))
    x_tick_1 = []
    x_tick_2 = []
    for i in x:
        x_tick_1.append(i - 0.375)
        x_tick_1.append(i + 0.375)
        x_tick_2.append(i)
    y = {
        "one_to_one": [],
        "one_to_many": [],
        "many_to_one": [],
        "many_to_many": [],
        "only_approval": [],
    }
    y_total = []
    x_ticklabels = []
    y_ticks = [0, 25, 50, 75, 100]
    legends = list(y)
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
        size=18,
    )
    # load data
    count = 1
    for f in filenames:
        x_ticklabels.append("Pair " + str(count))
        count += 1
        raw_data = statistic(f)
        for key in list(raw_data)[:-1]:
            y[key].append(raw_data[key] * 100 / raw_data["total"])
        y_total.append(raw_data["total"])

    # plot setting
    # fig = plt.figure(frameon=False, figsize=(16, 8), dpi=95)
    fig, ax1 = plt.subplots(figsize=(16, 6))
    # plt.figure(frameon=False, figsize=(16, 8), dpi=95)
    ax1.yaxis.grid()  # horizontal lines
    ax2 = ax1.twinx()
    width = 0.15

    # plot data in grouped manner of bar type

    # plot 1
    ax1.bar(x - width * 2, y["one_to_one"], width, color=colors[0], hatch="..")
    ax1.bar(x - width, y["one_to_many"], width, color=colors[1], hatch="//")
    ax1.bar(x, y["only_approval"], width, color=colors[2], hatch="|")
    ax1.bar(x + width, y["many_to_one"], width, color=colors[3], hatch="*")
    ax1.bar(x + width * 2, y["many_to_many"], width, color=colors[4], hatch="..")

    ax1.set_xticks(x_tick_1)
    ax1.set_xticks(x_tick_2, minor=True)
    ax1.set_xticklabels(x_ticklabels, minor=True, fontproperties=font)
    ax1.set_xticklabels([])
    ax1.set_xlabel("Token-Spender Pairs", fontname="Times New Roman", fontsize=20)
    ax1.tick_params(axis="x", which="minor", length=0)
    ax1.set_ylabel(
        "Behavior Mode Distribution (%)", fontname="Times New Roman", fontsize=20
    )

    ax1.set_yticks(np.arange(0, 110, 10))
    ax1.set_yticklabels(
        ["0", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100"],
        fontproperties=font,
    )
    ax1.legend(
        [
            "Mode1 (one_to_one)",
            "Mode2 (one_to_many)",
            "Mode3 (many_to_zero)",
            "Mode4 (many_to_one)",
            "Mode5 (compound)",
        ],
        prop=legend_font,
    )
    # ax1.yaxis.set_major_formatter(mtick.PercentFormatter())

    # plot 2
    ax2.plot(x, y_total, linestyle="--", marker="o", color="tab:red")
    ax2.tick_params(axis="y", labelcolor="tab:red")
    ax2.set_yticks(np.arange(0, 360000, 50000))
    ax2.set_yticklabels(
        ["0K", "50K", "100K", "150K", "200K", "250K", "300K", "350K"],
        fontproperties=font,
    )
    color = "tab:red"
    ax2.set_ylabel(
        "# of Sender", color=color, fontname="Times New Roman", fontsize=20
    )  # we already handled the x-label with ax1

    # plt.show()
    plt.savefig("../figures/ub_.pdf")


if __name__ == "__main__":
    # count_total()
    filenames = read_filenames()
    plot(filenames)
    # for f in filenames:
    #     statistic(f)
