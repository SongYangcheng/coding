import torch
import torch.nn as nn
import torchvision.models as models
from torchinfo import summary
from data_processing import create_data_loaders

device = 'cuda' if torch.cuda.is_available() else 'cpu'

#采用迁移学习，使用ResNet18预训练模型
class RestNet18Net(nn.Module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        