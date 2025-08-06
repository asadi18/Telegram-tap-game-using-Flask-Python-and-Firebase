# 🌐 Telegram Tap Game

This project is a full-stack Telegram Web App game where users tap to collect coins.  
Built with Python (Flask), Firestore (Firebase), and Telegram Bot API.

---

## Features

- Telegram Web App: Play directly inside Telegram, no installation required.
- Real-time coin tracking: Shows both session and total coins.
- Persistent storage: All user data saved in Google Firestore.
- Batch saving: Fast, efficient updates of coins during play.
- Responsive: Works on both mobile and desktop devices.
- Cloudflare Tunnel: Easy public access for Telegram Web Apps, even from localhost.

---

## Prerequisites

- Python 3.8 or newer
- pip (Python package manager)
- A Telegram account with a registered Telegram Bot
- Firebase project with Firestore enabled
- cloudflared (for exposing localhost, download from Cloudflare)
- Optionally, you can use ngrok as an alternative to cloudflared

---

## Setup Instructions

1. **Clone the Repository**

   Download or clone the repository to your machine.

2. **Install Python Dependencies**

   Run the following command to install required packages:


3. **Set Up Firebase**

- Go to [Firebase Console](https://console.firebase.google.com/)
- Create a new project and enable Firestore.
- Download the service account credentials JSON file and save it as `firebase.json` in your project directory.

4. **Create Your Telegram Bot**

- Open Telegram and search for `@BotFather`.
- Use the `/newbot` command and follow instructions to get your bot token.
- Edit `main.py` and replace the `BOT_TOKEN` variable with your own bot token.

5. **Run Cloudflare Tunnel**

- Download [cloudflared](https://github.com/cloudflare/cloudflared/releases) for your system.
- Start the tunnel using:

  ```
  cloudflared tunnel --url http://localhost:5000
  ```

- Copy the public URL provided by cloudflared and update it in `main.py` where the `webapp_url` is set.

6. **Run the App**

- Start your application by running:

  ```
  python main.py
  ```

- The Flask server runs at `localhost:5000`, and the Telegram bot will start polling for messages.

---

## How to Use

- Open Telegram, start your bot, and send the `/start` command.
- Tap the "Play Tap Game" button to open the game as a web app inside Telegram.
- Tap the hamster to collect coins.
- Your total coins are saved to Firestore. The app auto-saves session coins every few seconds and on close.

---

## File Descriptions

- `main.py`: The Python backend (Flask app, Telegram bot, Firestore API)
- `firebase.json`: Firebase admin credentials (**never share or commit this file publicly**)
- `templates/tap.html`: The web app UI for the game (HTML & JavaScript)
- `static/style.css`: CSS styles for the tap game
- `cloudflared-windows-amd64.exe`: Cloudflare tunnel binary for Windows
- `details.txt`: Any project notes or details you want to keep
- `Backups/`: Folder for your own backup files (optional)

---

## Security Notes

- Never commit your `firebase.json` or Telegram bot token to a public repository.  
Always add them to `.gitignore` before pushing to GitHub.
- Update your public tunnel URL (from cloudflared/ngrok) in your code any time it changes.

---

## Troubleshooting

- **Bot not responding:**  
Double-check your `BOT_TOKEN` and make sure your bot is started in Telegram.  
Ensure cloudflared or ngrok is running and the webhook URL in your code matches the current tunnel address.

- **Firestore errors:**  
Check your Firebase service account JSON and make sure Firestore is enabled.

- **Web app not loading:**  
Confirm your public URL is accessible in the browser and points to your running Flask server.

---

## Customization

- Edit `static/style.css` to change the look and feel.
- Update `templates/tap.html` to add new UI or game logic.
- Expand `main.py` for extra features or new Telegram commands.

---

## Credits

- Built with Flask, PyTelegramBotAPI, Firebase Admin SDK, and Cloudflare Tunnel.
- Inspired by Telegram’s [Web Apps documentation](https://core.telegram.org/bots/webapps).

---

## License

MIT License

---

*Questions or issues? Open an issue on GitHub or contact me.*
