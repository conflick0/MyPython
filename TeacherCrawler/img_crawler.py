import requests
from bs4 import BeautifulSoup
import tkinter as tk

def get_teacher_data(url):
    dict = {}
    html = requests.get(url)
    html.encoding = 'utf-8'
    sp = BeautifulSoup(html.text, 'html.parser')
    data = sp.select("#content")

    lis = data[0].find_all("li")[::4]
    links = data[0].find_all("a")[1::3]
    imgs = data[0].select("img")[0::2]

    for name, position, img in zip(links, lis, imgs):
        dict.setdefault(name.string+position.string.lstrip("職稱: "), img.get("src"))

    return dict


def downloadImg(name, url):
    folder_path = r'./teacher_img/' + name + '.jpg'

    try:
        html = requests.get(url)  # use 'get' to get photo link path , requests = send request
    except Exception as e:
        print('[!]Error : ' + str(e))
    else:
        img_name = folder_path

        with open(img_name, 'wb') as file:  # write into file by byte

            file.write(html.content)

            file.flush()

        file.close()  # close file


if __name__ == '__main__':

    root = tk.Tk()
    root.title('crawler')
    root.geometry("900x500")    # window size
    root.config(background="#262626")

    listbox = tk.Listbox(root, font=("time", 20, "bold"), width=200, background="#262626", foreground="white")
    listbox.pack()

    url = "http://www.csie.tku.edu.tw/members/teacher.php?class=110"
    teacher_dict = get_teacher_data(url)
    for name, url in teacher_dict.items():
        print(name, url)
        listbox.insert(tk.END, name+" "+url)
        downloadImg(name, url)

    root.mainloop()



