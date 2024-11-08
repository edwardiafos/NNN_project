import torch
from torch import nn
import torchvision
from pathlib import Path
from typing import List, Union
import json

THIS_FOLDER = Path(__file__).parent.resolve() # path/to/root/folder/NNN_Project/flaskr


def model_and_transforms(model_type: str):
    device = torch.device("cpu")

    efficient_net_weights = torchvision.models.EfficientNet_V2_S_Weights.DEFAULT
    efficient_net = torchvision.models.efficientnet_v2_s(weights=efficient_net_weights)
    transforms = efficient_net_weights.transforms()

    for param in efficient_net.features.parameters():
        param.requires_grad = False
    
    if model_type == "flower":
        efficient_net.classifier[1] = nn.Linear(in_features=1280, out_features=14, bias=True)
        efficient_net.load_state_dict(torch.load(f"{THIS_FOLDER}/models/flower/flower_model.pt", map_location=device, weights_only=True))
    

    elif model_type == "mushroom":
        efficient_net.classifier[1] = nn.Linear(in_features=1280, out_features=9, bias=True)
        efficient_net.load_state_dict(torch.load(f"{THIS_FOLDER}/models/mushroom/mushroom_model.pt", map_location=device, weights_only=True))
    
    elif model_type == "animal-90":
        efficient_net.classifier[1] = nn.Linear(in_features=1280, out_features=90, bias=True)
        efficient_net.load_state_dict(torch.load(f"{THIS_FOLDER}/models/animal-90/animal_90_model.pt", map_location=device, weights_only=True))

    elif model_type == "butterfly-moth":
        efficient_net.classifier[1] = nn.Linear(in_features=1280, out_features=100, bias=True)
        efficient_net.load_state_dict(torch.load(f"{THIS_FOLDER}/models/butterfly-moth/butterfly_moth_model.pt", map_location=device, weights_only=True))

    elif model_type == "gemstone":
        efficient_net.classifier[1] = nn.Linear(in_features=1280, out_features=40, bias=True)
        efficient_net.load_state_dict(torch.load(f"{THIS_FOLDER}/models/gemstone/gemstone_model.pt", map_location=device, weights_only=True))

    elif model_type == "indian-bird":
        efficient_net.classifier[1] = nn.Linear(in_features=1280, out_features=25, bias=True)
        efficient_net.load_state_dict(torch.load(f"{THIS_FOLDER}/models/indian-bird/indian_bird_model.pt", map_location=device, weights_only=True))

    elif model_type == "sea-animal":
        efficient_net.classifier[1] = nn.Linear(in_features=1280, out_features=23, bias=True)
        efficient_net.load_state_dict(torch.load(f"{THIS_FOLDER}/models/sea-animal/sea_animal_model.pt", map_location=device, weights_only=True))

    elif model_type == "snake":
        efficient_net.classifier[1] = nn.Linear(in_features=1280, out_features=40, bias=True)
        efficient_net.load_state_dict(torch.load(f"{THIS_FOLDER}/models/snake/snake_model.pt", map_location=device, weights_only=True))

    efficient_net.eval()

    return efficient_net, transforms


def get_idx_to_class(model_type: str):
    CLASS_TO_IDX = {}
    

    if model_type == "flower":
        path = f"{THIS_FOLDER}/models/flower/flower_classes_to_index.json"
    elif model_type == "mushroom":
        path = f"{THIS_FOLDER}/models/mushroom/mushroom_class_to_index.json"
    elif model_type == "animal-90":
        path = f"{THIS_FOLDER}/models/animal-90/animal_90_class_to_index.json"
    elif model_type == "butterfly-moth":
        path = f"{THIS_FOLDER}/models/butterfly-moth/butterfly_moth_class_to_index.json"
    elif model_type == "gemstone":
        path = f"{THIS_FOLDER}/models/gemstone/gemstone_class_to_index.json"
    elif model_type == "indian-bird":
        path = f"{THIS_FOLDER}/models/indian-bird/indian_bird_class_to_index.json"
    elif model_type == "sea-animal":
        path = f"{THIS_FOLDER}/models/sea-animal/sea_animal_class_to_index.json"
    elif model_type == "snake":
        path = f"{THIS_FOLDER}/models/snake/snake_class_to_index.json"

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
