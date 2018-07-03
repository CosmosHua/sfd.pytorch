import torch
import cv2
from dataset import create_datasets
from model import Net
from trainer import Trainer

torch.set_default_tensor_type('torch.DoubleTensor')

if __name__ == "__main__":

    train_dataset, val_dataset = create_datasets('/home/louis/datasets/wider_face')

    train_dataloader = torch.utils.data.DataLoader(
        train_dataset,
        batch_size=1,
        num_workers=1,
        shuffle=True
    )

    model = Net()

    trainables_wo_bn = [param for name, param in model.named_parameters() if
                        param.requires_grad and 'bn' not in name]
    trainables_only_bn = [param for name, param in model.named_parameters() if
                          param.requires_grad and 'bn' in name]

    optimizer = torch.optim.SGD([
        {'params': trainables_wo_bn, 'weight_decay': 0.0001},
        {'params': trainables_only_bn}
    ], lr=0.01, momentum=0.9)

    trainer = Trainer(
        optimizer,
        model,
        train_dataloader,
        None,
        max_epoch=100,
        resume=None,
        log_dir='./logs'
    )
    trainer.train()