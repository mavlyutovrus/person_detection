__author__ = 'Guggi'

import urllib2
import urllib
import unirest
import json
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
from PIL import Image, ImageDraw, ImageFont

register_openers()

api_key = "YOUR_API_KEY" #you need to exchange the YOUR_API_KEY with your own API key from animetrics
mashape_key = "YOUR_MASHAPE_KEY" 


def detect_faces(image_fname):
    # request
    data, headers = multipart_encode({"image": open(image_fname, "rb"), "selector": "FACE"})
    headers["X-Mashape-Key"] = mashape_key
    request = urllib2.Request("https://animetrics.p.mashape.com/detect?api_key=" + api_key, data, headers)
    response = urllib2.urlopen(request).read()
    return json.loads(response)


# returned_json = detect_faces("13.JPG")
# print json.dumps(returned_json, indent=4, sort_keys=True)


def draw_text(img, text, top, left, text_height):
    from PIL import Image, ImageDraw, ImageFont
    font = ImageFont.load_default()
    draw = ImageDraw.Draw(img)
    text_image = Image.new("RGB", draw.textsize(text, font=font), "black")
    text_image_draw = ImageDraw.Draw(text_image)
    text_image_draw.text((0, 0), text, font=font, fill=(0, 255, 0))
    del text_image_draw
    new_width = (float(text_height) / text_image.size[1]) * text_image.size[0]
    new_width = int(new_width)
    text_image = text_image.resize((new_width, text_height))
    img.paste(text_image, (left, top, left + text_image.size[0], top + text_image.size[1]))
    del draw
    return img

def show_faces(big_image, left, top, height, width, text):
    draw = ImageDraw.Draw(big_image)
    draw.line((left, top, left, top + height), fill='green', width=5)
    draw.line((left, top, left + width, top), fill='green', width=5)
    draw.line((left + width, top, left + width, top + height), fill='green', width=5)
    draw.line((left, top + height, left + width, top + height), fill='green', width=5)

    # font = ImageFont.truetype("arial.ttf", 20)
    # draw.text((left, top + height + 1), selected_candidate, fill='green', font=font)
    del draw
    if text:
        big_image = draw_text(big_image, text, top + height, left, 50)
    return big_image




def get_timestamp():
    import time
    import datetime
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
    timestamp = str(st)
    return timestamp


def make_filename(person_name):
    return get_timestamp() + "_" + person_name + ".jpg"


def recognize_and_save_person(image_fname):
    faces_data = detect_faces(image_fname)["images"][0]
    if not faces_data["faces"]:
        print "NO FACES DETECTED! Finishing..."
        return
    im = Image.open(image_fname)
    for face in faces_data["faces"]:
        query_uri = """https://animetrics.p.mashape.com/recognize?
                        api_key=%s&
                        gallery_id=%s&
                        image_id=%s&
                        height=%d&
                        width=%d&
                        topLeftX=%d&
                        topLeftY=%d
                        """ % (api_key, "Designers", faces_data["image_id"],
                               face["height"], face["width"], face["topLeftX"], face["topLeftY"])
        query_uri = query_uri.replace("\t", "").replace(" ", "").replace("\n", "")
        response = unirest.get(query_uri,
                               headers={
                                   "X-Mashape-Key": mashape_key,
                                   "Accept": "application/json"
                               }
                               )
        candidates_probs = response.body["images"][0]["candidates"]
        max_prob, selected_candidate = max([(prob, cand_name) for cand_name, prob in candidates_probs.items()])
        im = show_faces(im, face["topLeftX"], face["topLeftY"], face["height"], face["width"], selected_candidate + ":" + str(max_prob)[:4])
        import time
        time.sleep(3)
    im.save("recognized/" + image_fname.split("/")[-1])


import os

folder = "GoPro/"
for fname in os.listdir(folder):
    if fname.endswith(".jpg") or fname.endswith(".JPG") or fname.endswith(".JPEG"):
        print fname
        recognize_and_save_person(folder + fname)
