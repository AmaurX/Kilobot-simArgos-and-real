import matplotlib.pyplot as plt


font = {'family': 'serif',
        'color':  'k',
        'weight': 'normal',
        'size': 10,
        }


def main():
    x = [5, 10, 20, 30, 50, 100]
    y_20_075 = [5.80, 5.52, 5.25, 5.10, 4.77, 4.13]
    y_18_075 = [5.98, 5.68, 5.39, 5.12, 4.84, 4.17]
    y_16_075 = [5.82, 5.79, 5.45, 5.26, 4.94, 4.22]
    y_14_075 = [6.33, 5.83, 5.66, 5.40, 5.01, 4.28]
    y_12_075 = [6.59, 6.28, 5.85, 5.64, 5.17, 4.37]
    y_10_075 = [6.50, 6.52, 6.12, 5.81, 5.31, 4.47]
    y_optimal = [5.80, 5.52, 5.25, 5.10, 4.84, 4.47]
    plt.figure(figsize=(10, 5))
    label = "rho = 0.75 and alpha = 2.0"
    plt.plot(x, y_20_075, '-o', linewidth=1, label=label)

    label = "rho = 0.75 and alpha = 1.8"
    plt.plot(x, y_18_075, '-o', linewidth=1, label=label)

    label = "rho = 0.75 and alpha = 1.6"
    plt.plot(x, y_16_075, '-o', linewidth=1, label=label)

    label = "rho = 0.75 and alpha = 1.4"
    plt.plot(x, y_14_075, '-o', linewidth=1, label=label)

    label = "rho = 0.75 and alpha = 1.2"
    plt.plot(x, y_12_075, '-o', linewidth=1, label=label)

    label = "rho = 0.75 and alpha = 1.0"
    plt.plot(x, y_10_075, '-o', linewidth=1, label=label)

    label = "rho = 0.75 and optimal alpha"
    plt.plot(x, y_optimal, '-o', linewidth=4, label=label)

    # plt.text(105, 62700, "alpha = 2.0", fontdict=font)
    # plt.text(105, 57800, "alpha = 1.8", fontdict=font)
    # plt.text(105, 70900, "alpha = 1.6", fontdict=font)
    # plt.text(105, 66600, "alpha = 1.4", fontdict=font)
    # plt.text(105, 51500, "alpha = 1.2", fontdict=font)
    # plt.text(105, 45900, "alpha = 1.0", fontdict=font)

    plt.legend()
    plt.xlabel("Number N of robots")
    ylabel = r'$WMSD\ (in\ 10^{-5} \ m^2/s^2)$'
    plt.ylabel(ylabel)
    plt.title("Average WMSD with rho = 0.75")
    plt.savefig("average_WMSD_N_alpha_rho=0,75.png")


if __name__ == '__main__':
    main()
