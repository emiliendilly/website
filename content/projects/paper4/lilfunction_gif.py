import cv2
import os
import glob
import imageio

def videos_to_gifs(input_folder, fps=10, scale=0.5):
    """
    Convert all videos in the given folder to GIFs.

    Args:
        input_folder (str): Path to folder containing video files.
        fps (int): Frames per second for output GIF.
        scale (float): Resize scale factor (e.g., 0.5 = half size).
    """
    output_folder = os.path.join(input_folder, "gifs")
    os.makedirs(output_folder, exist_ok=True)

    video_files = glob.glob(os.path.join(input_folder, "*.mov"))
    i = 0
    for video_path in video_files:
        filename, ext = os.path.splitext(os.path.basename(video_path))
        gif_path = os.path.join(output_folder, f"{filename}.gif")

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"⚠️ Cannot open {video_path}")
            continue

        frames = []
        while True:
            ret, frame = cap.read()
            if not ret :
                break
            # Resize if needed
            if scale != 1.0:
                frame = cv2.resize(frame, None, fx=scale, fy=scale)
            # Convert BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if i % 10 == 0:
                frames.append(frame)
                framesave = frame
            i += 1
        for k in range(10):
            frames.append(framesave)

        cap.release()

        if frames:
            imageio.mimsave(gif_path, frames, fps=fps)
            print(f"✅ Saved {gif_path}")
        else:
            print(f"⚠️ No frames extracted from {video_path}")


def main():
    current_folder = os.getcwd()   # current working directory
    videos_to_gifs(current_folder, fps=5, scale=0.4)

if __name__ == "__main__":
    main()
