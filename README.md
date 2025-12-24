# Image Hub

Image Hub is a web application that allows users to create an account, log in, and upload images to their profile. Each uploaded image is provided in various formats for easy sharing, including a direct link and HTML embed code. The application uses Flask and SQLite for a lightweight and efficient backend.

## How It Works

- **User Authentication**: Users can register for a new account or log in to an existing one. The application uses Flask-Login for session management and secure password hashing to protect user credentials.
- **Image Uploads**: Once logged in, users can upload images to their profile. The images are saved to the server, and a reference is stored in the database, linked to the user's account.
- **Image Management**: Users can view all their uploaded images on their profile page and delete any images they no longer want.
- **Image Sharing**: Each image has a dedicated page with a direct link and an HTML embed code, making it easy to share on other websites or applications.

## How to Use

To run the application locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/image-hub.git
   cd image-hub
   ```

2. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

The application will be available at `http://127.0.0.1:5000`.

## Version History

- **v1.0.0** (Current)
  - Initial release.
  - Features: User registration, login, and logout. Image uploading, viewing, and deletion. Direct link and HTML embed code for each image.
