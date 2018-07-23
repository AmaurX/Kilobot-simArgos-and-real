import matplotlib.pyplot as plt


font = {'family': 'serif',
        'color':  'k',
        'weight': 'normal',
        'size': 10,
        }


def main():
    x = [5, 10, 20, 30, 50, 100]
    y_20_075 = [28900, 29700, 36300, 37600, 41500, 62700]
    y_18_075 = [41600, 33100, 40000, 40200, 40100, 57800]
    y_16_075 = [36300, 34900, 43000, 40700, 46300, 70900]
    y_14_075 = [33900, 35500, 37800, 45200, 42300, 66600]
    y_12_075 = [35600, 32600, 41200, 41700, 49400, 51500]
    y_10_075 = [51300, 39500, 41100, 37100, 43000, 45900]
    plt.figure(figsize=(10, 5))
    label = "rho = 0.75 and alpha = 2.0"
    plt.plot(x, y_20_075, '-o', linewidth=3, label=label)

    label = "rho = 0.75 and alpha = 1.8"
    plt.plot(x, y_18_075, '-o', linewidth=1, label=label)

    label = "rho = 0.75 and alpha = 1.6"
    plt.plot(x, y_16_075, '-o', linewidth=1, label=label)

    label = "rho = 0.75 and alpha = 1.4"
    plt.plot(x, y_14_075, '-o', linewidth=1, label=label)

    label = "rho = 0.75 and alpha = 1.2"
    plt.plot(x, y_12_075, '-o', linewidth=1, label=label)

    label = "rho = 0.75 and alpha = 1.0"
    plt.plot(x, y_10_075, '-o', linewidth=3, label=label)

    # plt.text(105, 62700, "alpha = 2.0", fontdict=font)
    # plt.text(105, 57800, "alpha = 1.8", fontdict=font)
    # plt.text(105, 70900, "alpha = 1.6", fontdict=font)
    # plt.text(105, 66600, "alpha = 1.4", fontdict=font)
    # plt.text(105, 51500, "alpha = 1.2", fontdict=font)
    # plt.text(105, 45900, "alpha = 1.0", fontdict=font)

    plt.legend()
    plt.xlabel("Number N of robots")
    plt.ylabel("Average first passage time (in ticks)")
    plt.title("Average first passage time with rho = 0.75")
    plt.savefig("average_first_passage_time_N_alpha_rho=0,75.png")


if __name__ == '__main__':
    main()
