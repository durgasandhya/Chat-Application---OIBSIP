import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext

class ChatClient:
    def __init__(self, username):
        self.username = username
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('localhost', 12345))

        # GUI Setup
        self.window = tk.Tk()
        self.window.title(f"{username}'s Chat")
        
        self.chat_window = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, state=tk.DISABLED, height=20, width=60)
        self.chat_window.pack(pady=10, padx=10)

        self.message_entry = tk.Entry(self.window, width=50)
        self.message_entry.pack(pady=5, padx=10)
        self.message_entry.bind("<Return>", self.send_message)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.start_client()

    def start_client(self):
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    self.display_message(message, received=True)
            except:
                break

    def send_message(self, event=None):
        message = self.message_entry.get()
        if message:
            self.client_socket.send(f"{self.username}: {message}".encode('utf-8'))
            self.display_message(f"{self.username}: {message}", received=False)
            self.message_entry.delete(0, tk.END)

    def display_message(self, message, received):
        self.chat_window.config(state=tk.NORMAL)
        if received:
            self.chat_window.insert(tk.END, message + '\n', 'received')
        else:
            self.chat_window.insert(tk.END, message + '\n', 'sent')
        self.chat_window.yview(tk.END)
        self.chat_window.tag_config('sent', background='blue', foreground='white')
        self.chat_window.tag_config('received', background='green', foreground='black')
        self.chat_window.config(state=tk.DISABLED)

    def on_closing(self):
        self.client_socket.close()
        self.window.destroy()

if __name__ == "__main__":
    username = simpledialog.askstring("Login", "Enter your username:")
    if username:
        ChatClient(username)
        tk.mainloop()
