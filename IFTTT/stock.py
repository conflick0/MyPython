import twstock


def get_stock(stock_code):
    stock_name = twstock.codes[stock_code].name   # get stock name
    stock = twstock.Stock(stock_code)  # get stock
    stock_price = stock.price[-1]   # today last stock price
    date = stock.date[-1]   # today date
    return "name: {}<br>\nprice: {}<br>\ndate: {}<br>\n".format(stock_name, stock_price, date)


if __name__ == "__main__":
    result = get_stock('3008')  # 3008 is stock code
    print(result)
