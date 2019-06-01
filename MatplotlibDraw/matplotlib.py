import matplotlib.pyplot as plt
import csv


def read_data(file_name):
    data_list = []
    with open(file_name, newline='', encoding='utf-8') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            data_list.append(row)

    return data_list


def process_data(data_list):
    data_dict = {}
    titles = data_list.pop(0)  # get csv title
    for t in titles:
        data_dict[t] = []

    # get col data and put into dict
    for data in data_list:
        for elem, key in zip(data, data_dict):
            data_dict[key].append(float(elem))

    return data_dict


def draw_stock_graph(data_dict):
    plt.title("stock")
    plt.xlabel("time(day)")
    plt.ylabel("stock value(dollar)")

    for key in data_dict:
        plt.plot(data_dict[key], "-", label=key)

    plt.legend(loc='upper right')
    plt.show()


def draw_anscombe_i_graph(data_dict):
    plt.title("anscombe_i")
    plt.xlabel("x")
    plt.ylabel("y")

    plt.scatter(data_dict['x'], data_dict['y'])
    plt.show()


if __name__ == '__main__':

    # draw stock.csv result
    file_name = "stock.csv"
    data_list = read_data(file_name)
    data_dict = process_data(data_list)
    draw_stock_graph(data_dict)

    # draw anscombe_i.csv result
    file_name = "anscombe_i.csv"
    data_list = read_data(file_name)
    data_dict = process_data(data_list)
    draw_anscombe_i_graph(data_dict)



