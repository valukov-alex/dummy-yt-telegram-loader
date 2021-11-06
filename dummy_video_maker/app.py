from flask import Flask, request, Response
from make_dummy_video import make_dummy_video
import json
from Constant import Constant
import os

app = Flask(__name__)


def read_file(path):
    with open(path, "r") as f:
        data = f.read()
    return data


def make_metadata_from_title(title):
    metadata = {
        "title": title,
        "description": "Test description",
        "tags": ["test1", "test2", "test3"]
    }
    return metadata


@app.route('/make_video')
def make_video():
    id_data = request.args.get("id")
    folder = os.path.join(Constant.DATA_FOLDER, id_data)
    if not os.path.exists(folder):
        return Response("Folder {} not found".format(id_data), status=404)
    
    title_path = os.path.join(folder, "title.txt")
    if not os.path.exists(title_path):
        return Response("File title.txt not found in folder {}".format(id_data), status=404)

    is_image = False
    img_name = None
    for filename in os.listdir(folder):
        if "image" == filename.split(".")[0]:
            img_name = filename
    if img_name is None:
        return Response("File image.* not found in folder {}".format(id_data), status=404)
    
    img_path = os.path.join(folder, img_name)
    video_path = os.path.join(folder, "video.avi")


    try:
        make_dummy_video(img_path, video_path)
    except Exception as e:
        raise e
        return Response("Something wrong while making video, error:\n{}".format(e), status=405)
    
    metadata = make_metadata_from_title(read_file(title_path))

    with open(os.path.join(folder, "metadata.json"), "w") as f:
        json.dump(metadata, f,indent=4, ensure_ascii=False)
    
    response_dict = {
        "video_path": video_path,
    }
    response_json = json.dumps(response_dict)
    return Response(response_json, status=200, mimetype="application/json")

if __name__ == "__main__":
    app.run(port=Constant.PORT)
