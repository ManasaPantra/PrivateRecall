from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
_caption_model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
_caption_model.to(_device)


def get_caption(image: Image.Image) -> str:
    inputs = _processor(image, return_tensors="pt").to(_device)
    out = _caption_model.generate(**inputs)
    caption = _processor.decode(out[0], skip_special_tokens=True)
    return caption