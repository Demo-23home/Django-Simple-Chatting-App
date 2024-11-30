# Chat Application

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Architecture](#architecture)
- [Installation](#installation)
- [Project Setup](#project-setup)
- [Routing and WebSockets](#routing-and-websockets)

## Overview

The **Chat Application** is a real-time messaging platform built using Django. It allows users to sign up, log in, create chat groups, join existing groups, and send messages. The app features WebSocket integration for live chat and group management functionalities. Users can manage their profiles and engage in chat conversations via WebSockets.

## Features

- **Real-Time Messaging:** Users can send and receive messages instantly using WebSockets.
- **Group Chat:** Create, join, and leave chat groups.
- **User Authentication:** Secure login, signup, and profile management.
- **Group Management:** Manage membership and delete groups.

## Technologies Used

### Backend

- **Django:** Web framework for building the backend application.
- **WebSockets:** Real-time messaging powered by WebSockets.
- **Channels:** Django Channels for handling WebSocket connections.
- **SQLite:** Relational database for storing user and group data.

### Frontend

- **HTML/CSS/JavaScript:** For creating the user interface of the web application.
- **WebSockets:** Used in the frontend for real-time messaging.

## Architecture

The application follows a **client-server architecture**, with Django handling the backend and WebSockets integration through Django Channels. Users interact with the frontend (HTML/CSS/JS), and messages are transmitted in real-time using WebSockets. The backend routes requests via Django views, and Channels handles WebSocket connections to ensure seamless chat communication.

## Installation

### Project Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Demo-23home/Django-Simple-Chatting-App.git
   cd chat-app
   ```
1. **Build the Docker Conatainer:**

```bash
docker-compose up --build
```

2. **Create a Superuser**:
```bash
docker-compose exec backend python manage.py createsuperuser
```

The application will be accessible at http://localhost:8000.

Routing and WebSockets
WebSocket Routing
This application uses Django Channels to handle WebSocket connections. The WebSocket URL pattern is set as follows:

```python
websocket_urlpatterns = [
    path(r"ws/open_chat/<uuid>/", consumers.ChatConsumer.as_asgi()),
]
```
This enables real-time communication for each chat group. When users connect to a chat, they can exchange messages using WebSockets.

Chat URLs
The URLs for group management and chat-related actions are:

```python
from django.urls import path
from . import views

urlpatterns = [
    path("new_group", views.create_group, name="new_group"),
    path("join_group/<uuid:uuid>", views.join_group, name="join_group"),
    path("leave_group/<uuid:uuid>", views.leave_group, name="leave_group"),
    path("remove_group/<uuid:uuid>", views.delete_group, name="remove_group"),
    path("open_chat/<uuid:uuid>", views.open_chat, name="open_chat"),
]
```

Members URLs
User authentication and management are handled through the following routes:

```python
from django.urls import path
from . import views

urlpatterns = [
    path("signup", views.user_signup, name="signup"),
    path("login", views.user_login, name="login"),
    path("logout", views.logout, name="logout"),
    path("", views.home, name="home"),
]

```
Main URLs
The main URL configuration includes the routing for both chat and user-related features:

```python
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include("members.urls")),
    path('chat/', include("chat.urls")),
]
```
