import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="torchvision.transforms.functional_tensor")
import os
from PIL import Image
import numpy as np
from realesrgan import RealESRGANer
from basicsr.archs.srvgg_arch import SRVGGNetCompact

def enhance_photo(input_path, output_path, model_path='weights/realesr-general-x4v3.pth', scale=4):
    try:
        print(f"[INFO] Loading image from: {input_path}")
        img = Image.open(input_path).convert('RGB')

        print("[INFO] Initializing RealESRGAN model...")
        model = SRVGGNetCompact(
            num_in_ch=3, num_out_ch=3, num_feat=64,
            num_conv=32, upscale=scale, act_type='prelu'
        )

        upsampler = RealESRGANer(
            scale=scale,
            model_path=model_path,
            model=model,
            dni_weight=None,
            tile=0,
            tile_pad=10,
            pre_pad=0,
            half=False,
            gpu_id=None  # change to 0 if GPU available
        )

        print("[INFO] Enhancing image...")
        img_np = np.array(img)
        enhanced_img, _ = upsampler.enhance(img_np)

        enhanced_pil = Image.fromarray(enhanced_img)

        # Resize enhanced image back to original input size to preserve resolution
        print("[INFO] Resizing enhanced image back to original size")
        enhanced_pil = enhanced_pil.resize(img.size, Image.LANCZOS)

        print(f"[INFO] Saving enhanced image to: {output_path}")
        enhanced_pil.save(output_path)
        print("[SUCCESS] Enhanced photo saved!")

    except Exception as e:
        print(f"[ERROR] Exception during enhancement: {e}")
        raise


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python photo_editor.py input_photo.jpg output_photo.png")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    enhance_photo(input_path, output_path)
