import os
import cv2
import numpy as np
import tempfile
import torch
from PIL import Image
from tqdm import tqdm
import moviepy.editor as mp
import noisereduce as nr
import scipy.io.wavfile as wav
from realesrgan import RealESRGANer
from basicsr.archs.srvgg_arch import SRVGGNetCompact

def enhance_video(input_path, output_path, model_path='weights/realesr-general-x4v3.pth', scale=4, progress_callback=None):
    # Load the RealESRGAN model structure
    model = SRVGGNetCompact(
        num_in_ch=3, num_out_ch=3, num_feat=64,
        num_conv=32, upscale=scale, act_type='prelu'
    )

    # Initialize RealESRGAN upsampler
    upsampler = RealESRGANer(
        scale=scale,
        model_path=model_path,
        model=model,
        dni_weight=None,
        tile=0,
        tile_pad=10,
        pre_pad=0,
        half=False,
        gpu_id=None  # Change to 0 if using GPU
    )

    # Open video
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise RuntimeError(f"❌ Failed to open video file: {input_path}")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    new_width, new_height = width * scale, height * scale

    temp_video_path = os.path.join(tempfile.gettempdir(), 'temp_enhanced_video.mp4')
    out = cv2.VideoWriter(temp_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (new_width, new_height))

    print(f"🔧 Enhancing video: {width}x{height} → {new_width}x{new_height}")

    for i in tqdm(range(total_frames), desc="Enhancing Frames"):
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)

        try:
            enhanced, _ = upsampler.enhance(np.array(img))
            enhanced_bgr = cv2.cvtColor(enhanced, cv2.COLOR_RGB2BGR)
            out.write(enhanced_bgr)
        except Exception as e:
            print(f"⚠️ Frame {i+1} enhancement failed: {e}")
            out.write(frame)

        if progress_callback:
            progress = int(((i + 1) / total_frames) * 100)
            progress_callback(progress)

    cap.release()
    out.release()

    print("🎧 Extracting and denoising audio...")

    # === Extract and denoise audio ===
    clip = mp.VideoFileClip(input_path)
    audio = clip.audio

    temp_wav = os.path.join(tempfile.gettempdir(), "temp_audio.wav")
    temp_cleaned_wav = os.path.join(tempfile.gettempdir(), "cleaned_audio.wav")
    audio.write_audiofile(temp_wav, verbose=False, logger=None)

    rate, data = wav.read(temp_wav)
    if len(data.shape) == 2:  # Stereo to mono
        data = np.mean(data, axis=1).astype(np.int16)
    cleaned = nr.reduce_noise(y=data, sr=rate)
    wav.write(temp_cleaned_wav, rate, cleaned)

    # === Attach denoised audio ===
    print("🔗 Merging enhanced video with cleaned audio...")

    final_video = mp.VideoFileClip(temp_video_path)
    final_video = final_video.set_audio(mp.AudioFileClip(temp_cleaned_wav))
    final_video.write_videofile(output_path, codec='libx264', audio_codec='aac', verbose=False, logger=None)

    print(f"✅ Enhanced video saved at: {output_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python video_editor.py input_video.mp4 output_video.mp4")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    enhance_video(input_path, output_path)
