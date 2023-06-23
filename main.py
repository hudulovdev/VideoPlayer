import tkinter as tk
import cv2

class VideoPlayer:
    def __init__(self, video_path):
        self.video_path = video_path
        self.root = tk.Tk()
        self.root.title("Video Player")

        # Create a canvas to display the video frames
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack()

        # Create playback controls
        self.play_button = tk.Button(self.root, text="Play", command=self.play_video)
        self.play_button.pack(side=tk.LEFT)

        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_video)
        self.pause_button.pack(side=tk.LEFT)

        # Open the video file
        self.video = cv2.VideoCapture(self.video_path)

        self.play_video()

        self.root.mainloop()

    def play_video(self):
        # Read the next frame from the video
        ret, frame = self.video.read()

        if ret:
            # Convert the frame from BGR to RGB format
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Resize the frame to fit the canvas
            height, width, _ = frame_rgb.shape
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            aspect_ratio = canvas_width / canvas_height
            if width / height > aspect_ratio:
                new_width = int(canvas_height * (width / height))
                new_height = canvas_height
            else:
                new_width = canvas_width
                new_height = int(canvas_width / (width / height))
            frame_rgb = cv2.resize(frame_rgb, (new_width, new_height))

            # Convert the frame to ImageTk format
            image = Image.fromarray(frame_rgb)
            image_tk = ImageTk.PhotoImage(image)

            # Update the canvas with the new frame
            self.canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)
            self.canvas.image = image_tk

            # Schedule the next frame update
            self.root.after(10, self.play_video)
        else:
            # End of video
            self.video.release()

    def pause_video(self):
        # Stop playing the video
        self.video.release()


# Example usage
video_path = input("Enter video location: ")
player = VideoPlayer(video_path)
