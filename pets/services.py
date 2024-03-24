import base64

import ultralytics
import cv2
import torch
import numpy as np
import os
import torchvision.models as models
import torchvision.transforms as transfroms


def to_tensor(x, **kwargs):
    return x.transpose(2, 0, 1).astype('float32')


def get_embeddings(image):
    model = ultralytics.YOLO("yolov8n.pt")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    output = model(image)

    # 15: 'cat', 16: 'dog'
    names_of_categories = output[0].names
    number_of_objects = len(output[0].boxes)

    bboxes_cats = []
    bboxes_dogs = []

    for i in output[0].boxes:
        if i.cls == 15 and i.conf >= 0.70:
            bboxes_cats.append(i.xyxy.cpu().numpy())
        elif i.cls == 16 and i.conf >= 0.70:
            bboxes_dogs.append(i.xyxy.cpu().numpy())

    result_dir = 'ResultsOfHackathon'
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    net = models.mobilenet_v2(pretrained=True)
    net.classifier[1] = torch.nn.Identity()

    vectors = []

    for i, box in enumerate(bboxes_cats):
        cropped_image = image[int(box[0][1]):int(box[0][3]), int(box[0][0]):int(box[0][2]), :]
        cropped_image = cropped_image / 255
        image_tensor = torch.tensor(cropped_image, dtype=torch.float32).permute(2, 0, 1)

        # Convert the image to a PyTorch tensor
        image_tensor = transfroms.functional.resize(image_tensor, (224, 224))
        input = image_tensor.unsqueeze(0)

        vector = net(input)
        vectors.append(vector.squeeze().detach().cpu().numpy())

    for i, box in enumerate(bboxes_dogs):
        cropped_image = image[int(box[0][1]):int(box[0][3]), int(box[0][0]):int(box[0][2]), :]
        # cropped_image_file = os.path.join(result_dir, f'dog_cropped_image_{i}.jpg')
        # cv2.imwrite(cropped_image_file, cropped_image)

        cropped_image = cropped_image / 255
        image_tensor = torch.tensor(cropped_image, dtype=torch.float32).permute(2, 0, 1)

        # Convert the image to a PyTorch tensor
        image_tensor = transfroms.functional.resize(image_tensor, (224, 224))
        input = image_tensor.unsqueeze(0)

        vector = net(input)
        vectors.append(vector.squeeze().detach().cpu().numpy())

    return vectors[0]


def readb64(uri):
   encoded_data = uri.split(',')[1]
   nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
   img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
   return img


def create_embeddings(image_uri):
    image = readb64(image_uri)
    return get_embeddings(image)


def loss(embedding, eval_vector: np.array):
    embedding_vector = np.array(list(map(float, embedding.embedding.split("|"))))
    # TODO: SAMIN WORK
    res = np.linalg.norm(embedding_vector - eval_vector)
    print(res)
    return res


def rank_findings(evaluation_vector, evaluation_embeddings):

    evaluation_embeddings.sort(
        key=lambda x: loss(x, evaluation_vector)
    )
    return evaluation_embeddings
