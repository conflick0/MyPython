import cv2
import requests
import time


def get_license(img_name,image_url):
    # Replace <Subscription Key> with your valid subscription key.
    subscription_key = ""
    assert subscription_key

    vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"

    text_recognition_url = vision_base_url + "read/core/asyncBatchAnalyze"

    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    params = {'mode': 'Handwritten'}
    data = {'url': image_url}
    response = requests.post(
        text_recognition_url, headers=headers, params=params, json=data)
    response.raise_for_status()

    # The recognized text isn't immediately available, so poll to wait for completion.
    analysis = {}
    poll = True
    while (poll):
        response_final = requests.get(
            response.headers["Operation-Location"], headers=headers)
        analysis = response_final.json()
        print(analysis)
        time.sleep(1)
        if ("recognitionResults" in analysis):
            poll = False
        if ("status" in analysis and analysis['status'] == 'Failed'):
            poll = False

    polygons = []
    if ("recognitionResults" in analysis):
        # Extract the recognized text, with bounding boxes.
        polygons = [(line["boundingBox"], line["text"])
                    for line in analysis["recognitionResults"][0]["lines"]]
    print(polygons)
    show_img(polygons, img_name)


def show_img(polygons, img_name):
    img = cv2.imread('./img/'+img_name+'.jpg')
    for box in polygons:
        cv2.rectangle(img, (box[0][0], box[0][1]), (box[0][4], box[0][5]), (0, 255, 0), 2)
        cv2.putText(img, box[1], (box[0][0] - 20, box[0][1] - 20), 0, 1, (0, 255, 0), 2)

    cv2.imshow(img_name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def downloadImg(name, url):
    folder_path = r'./img/' + name + '.jpg'

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
    imgBaseUrl = "https://raw.githubusercontent.com/conflick0/MyPython/master/CarRecognize/img/"

    for i in range(1, 11):
        imgName = "car" + str(i)
        imgURL = (imgBaseUrl + imgName + ".jpg")
        downloadImg(imgName, imgURL)
        get_license(imgName, imgURL)
        time.sleep(1)

