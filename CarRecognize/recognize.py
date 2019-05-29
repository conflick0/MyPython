import cv2
import requests

# Replace <Subscription Key> with your valid subscription key.
subscription_key = ""
assert subscription_key


vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"

ocr_url = vision_base_url + "ocr"

# Set image_url to the URL of an image that you want to analyze.
image_url = "https://www.cardu.com.tw/image_upload/news/28/U20151119083338.jpg"
#"https://img.incar.tw/files/styles/media_gallery_large/public/media/i/m/g/0/7/1/8/img_0718_2.jpg" #car3

headers = {'Ocp-Apim-Subscription-Key': subscription_key}
params  = {'language': 'unk', 'detectOrientation': 'true'}
data    = {'url': image_url}
response = requests.post(ocr_url, headers=headers, params=params, json=data)
response.raise_for_status()

analysis = response.json()

line_infos = [region["lines"] for region in analysis["regions"]]
word_infos = []
for line in line_infos:
    for word_metadata in line:
        for word_info in word_metadata["words"]:
            word_infos.append(word_info)

print(word_infos)

box_list = []
for word in word_infos:
    pos = []
    bound = word["boundingBox"].split(',')  # ['304', '304', '88', '29']
    for b in bound:
        pos.append(int(b))
    text = word["text"]
    box_list.append([pos, text])


img = cv2.imread('./img/car2.jpg')
for box in box_list:
    cv2.rectangle(img, (box[0][0], box[0][1]), (box[0][0] + box[0][2], box[0][1] + box[0][3]), (0, 255, 0), 2)
    cv2.putText(img, box[1], (box[0][0] - 20, box[0][1] - 20), 0, 1, (0, 255, 0), 2)


cv2.imshow('My Image', img)

# press any key to close the window
cv2.waitKey(0)
cv2.destroyAllWindows()



