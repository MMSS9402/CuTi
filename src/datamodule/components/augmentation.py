import torchvision.transforms as transforms
import numpy as np
import numpy.linalg as LA


class RGBDAugmentor:
    """perform augmentation on RGB-D video"""

    def __init__(self, reshape_size: (int, int)):
        self.reshape_size = reshape_size
        p_gray = 0.1
        self.augcolor = transforms.Compose(
            [
                transforms.ToPILImage(),
                transforms.ColorJitter(
                    brightness=0.25, contrast=0.25, saturation=0.25, hue=0.4 / 3.14
                ),
                transforms.RandomGrayscale(p=p_gray),
                transforms.ToTensor(),
            ]
        )

    def color_transform(self, images):
        """color jittering"""
        num, ch, h, w = images.shape
        images = images.permute(1, 2, 3, 0).reshape(ch, ht, wd * num)
        images = self.augcolor(images[[2, 1, 0]] / 255.0)
        
        return (
            images.reshape(ch, ht, wd, num).permute(3, 0, 1, 2).contiguous()
        )

    def __call__(self, images):
        images = self.color_transform(images)
        return images
