import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from pytube import YouTube, Playlist
import os

class youtubedownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("500x550")
        self.root.config(bg="lightblue")

        self.url_label = tk.Label(root, text="YouTube URL:", bg="lightblue")
        self.url_label.pack(pady=5)

        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack(pady=5)

        self.resolution_label = tk.Label(root, text="Select Resolution:", bg="lightblue")
        self.resolution_label.pack(pady=5)

        self.resolution_var = tk.StringVar(root)
        self.resolution_options = ["360p", "720p", "1080p", "Audio Only"]
        self.resolution_var.set(self.resolution_options[0])
        self.resolution_menu = ttk.Combobox(root, textvariable=self.resolution_var, values=self.resolution_options)
        self.resolution_menu.pack(pady=5)
        self.resolution_menu.bind("<<ComboboxSelected>>", self.update_format_options)

        self.format_label = tk.Label(root, text="Select Format:", bg="lightblue")
        self.format_label.pack(pady=5)

        self.format_var = tk.StringVar(root)
        self.format_options_video = ["mp4", "webm"]
        self.format_options_audio = ["mp3"]
        self.format_var.set(self.format_options_video[0])
        self.format_menu = ttk.Combobox(root, textvariable=self.format_var, values=self.format_options_video)
        self.format_menu.pack(pady=5)

        self.download_button = tk.Button(root, text="Download Video/Audio", command=self.download_video)
        self.download_button.pack(pady=5)

        self.download_playlist_button = tk.Button(root, text="Download Playlist", command=self.download_playlist)
        self.download_playlist_button.pack(pady=5)

        self.output_label = tk.Label(root, text="Output Directory:", bg="lightblue")
        self.output_label.pack(pady=5)

        self.output_button = tk.Button(root, text="Select Directory", command=self.select_directory)
        self.output_button.pack(pady=5)

        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=20)

        self.output_dir = ""

    def select_directory(self):
        self.output_dir = filedialog.askdirectory()
        if self.output_dir:
            self.output_label.config(text=f"Output Directory: {self.output_dir}")

    def update_format_options(self, event):
        selected_resolution = self.resolution_var.get()
        if selected_resolution == "audio only":
            self.format_menu.config(values=self.format_options_audio)
            self.format_var.set(self.format_options_audio[0])
        else:
            self.format_menu.config(values=self.format_options_video)
            self.format_var.set(self.format_options_video[0])

    def get_stream(self, yt, resolution, file_format):
        if resolution == "audio only":
            return yt.streams.filter(only_audio=True).first()
        else:
            return yt.streams.filter(res=resolution, file_extension=file_format).first()

    def download_video(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL.")
            return
        
        if not self.output_dir:
            messagebox.showerror("Error", "Please select an output directory.")
            return

        resolution = self.resolution_var.get()
        file_format = self.format_var.get()

        try:
            yt = YouTube(url, on_progress_callback=self.show_progress)
            stream = self.get_stream(yt, resolution, file_format)
            self.progress['maximum'] = 100
            if resolution == "audio only":
                output_file = stream.download(self.output_dir)
                base, ext = os.path.splitext(output_file)
                new_file = base + '.mp3'
                os.rename(output_file, new_file)
            else:
                stream.download(self.output_dir)
            messagebox.showinfo("Success", f"Downloaded: {yt.title}")
            self.progress['value'] = 0
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def download_playlist(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL.")
            return
        
        if not self.output_dir:
            messagebox.showerror("Error", "Please select an output directory.")
            return

        resolution = self.resolution_var.get()
        file_format = self.format_var.get()

        try:
            playlist = Playlist(url)
            total_videos = len(playlist.video_urls)
            for video_url in playlist.video_urls:
                yt = YouTube(video_url, on_progress_callback=self.show_progress)
                stream = self.get_stream(yt, resolution, file_format)
                self.progress['maximum'] = 100
                if resolution == "audio only":
                    output_file = stream.download(self.output_dir)
                    base, ext = os.path.splitext(output_file)
                    new_file = base + '.mp3'
                    os.rename(output_file, new_file)
                else:
                    stream.download(self.output_dir)
                self.progress['value'] = 0
            messagebox.showinfo("Success", "Playlist downloaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = bytes_downloaded / total_size * 100
        self.progress['value'] = percentage
        self.root.update_idletasks()


root = tk.Tk()
youtubedownloader(root)
root.mainloop()