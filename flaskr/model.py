import torch
from torch import nn
import torchvision
from pathlib import Path
from typing import List, Union
import json


def model_and_transforms(model_type: str):
    device = torch.device("cpu")

    efficient_net_weights = torchvision.models.EfficientNet_V2_S_Weights.DEFAULT
    efficient_net = torchvision.models.efficientnet_v2_s(weights=efficient_net_weights)
    transforms = efficient_net_weights.transforms()

    for param in efficient_net.features.parameters():
        param.requires_grad = False

    if model_type == "flower":
        efficient_net.classifier[1] = nn.Linear(in_features=1280, out_features=14, bias=True)
        efficient_net.load_state_dict(torch.load(r"flaskr\models\flower\flower_model.pt", map_location=device, weights_only=True))
    

    elif model_type == "mushroom":
        efficient_net.classifier[1] = nn.Linear(in_features=1280, out_features=9, bias=True)
        efficient_net.load_state_dict(torch.load(r"flaskr\models\mushroom\mushroom_model.pt", map_location=device, weights_only=True))
    
    
    efficient_net.eval()

    return efficient_net, transforms


def get_idx_to_class(model_type: str):
    CLASS_TO_IDX = {}
    

    if model_type == "flower":
        path = r"flaskr\models\flower\flower_classes_to_index.json"
    elif model_type == "mushroom":
        path = r"flaskr\models\mushroom\mushroom_class_to_index.json"

    with open(path, "r") as f:
        CLASS_TO_IDX = json.load(f)

    IDX_TO_CLASS = dict((v, k) for (k, v) in CLASS_TO_IDX.items())
    return IDX_TO_CLASS
    


def get_prediction(model_type: str, image_path: Union[str, Path]):
    eff_net, transforms = model_and_transforms(model_type=model_type)
    IDX_TO_CLASS = get_idx_to_class(model_type=model_type)

    image = torchvision.io.read_image(image_path)
    image = transforms(image).unsqueeze(0)

    logits = eff_net(image)[0]
    idx = logits.argmax().item()

    return IDX_TO_CLASS[idx]