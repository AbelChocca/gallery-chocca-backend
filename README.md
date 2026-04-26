# Project Description
Chocca Catalogue is a web catalog platform developed for a clothing store, where customers can explore products visually and filter them by category, title, color, and size.

This application solves a daily problem for the store: many customers cannot easily view all available clothing items. The platform allows them to find the right products more quickly and place an order through the system or via WhatsApp.

# Demo
[Chocca Catalogue](https://www.chocca.com.pe/)

## Stack

### Frontend 
![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white) ![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB) ![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white) ![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white) ![TanStack Query](https://img.shields.io/badge/TanStack_Query-FF4154?style=for-the-badge&logo=reactquery&logoColor=white) ![Axios](https://img.shields.io/badge/Axios-5A29E4?style=for-the-badge&logo=axios&logoColor=white) ![Framer Motion](https://img.shields.io/badge/Framer_Motion-0055FF?style=for-the-badge&logo=framer&logoColor=white) ![Zustand](https://img.shields.io/badge/Zustand-443E38?style=for-the-badge&logo=react&logoColor=white)

### Backend 
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white) ![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white) ![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white) ![Redis](https://img.shields.io/badge/Redis-DD0031?style=for-the-badge&logo=redis&logoColor=white)

### Database 
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

### Infrastructure 
![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white) ![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=black) ![Upstash](https://img.shields.io/badge/Upstash-00E9A3?style=for-the-badge&logo=upstash&logoColor=black)
 ### External Services 
 ![Cloudinary](https://img.shields.io/badge/Cloudinary-3448C5?style=for-the-badge&logo=cloudinary&logoColor=white) ![Google reCAPTCHA](https://img.shields.io/badge/Google_reCAPTCHA-4285F4?style=for-the-badge&logo=google&logoColor=white)
## Features
-   User authentication with JWT and secure HTTP-only cookies
-   Role-based access control for admin and regular users
-   Product catalog with filters by category, title, color, and size
-   Dynamic slides and promotional banners management
-   Product image upload and storage with Cloudinary
-   Protected admin dashboard for viewing overview data and managing products, slides and users.
-   Pagination for large product, favorite and users collections
-   Redis caching for better performance
-   Rate limiting on authentication endpoints
-   Google reCAPTCHA integration for bot protection
-   Responsive design for desktop and mobile devices
-   Dark mode support in dashboard sections
-   Search and filtering system for products
-   Favorite's page to view own favorite products
-   Deployment-ready architecture with Vercel, Render, and Upstash

## Architecture

The application follows a decoupled fullstack architecture where the frontend and backend are deployed independently. The frontend is hosted on Vercel and communicates with a FastAPI backend deployed on Render. Product images are stored in Cloudinary, while Redis is used for caching and rate limiting through Upstash.

### System Flow
<img width="4855" height="4865" alt="diagram_242" src="https://github.com/user-attachments/assets/86b8a423-e759-4163-9e08-98458b6532f3" />

## 📸 Screenshots
The following screenshots showcase the main features of the platform and its user experience.

### 🧑‍💼 Admin Dashboard
<img width="1569" height="800" alt="Captura de pantalla 2026-04-24 a la(s) 7 53 52 p  m" src="https://github.com/user-attachments/assets/0bbb3a48-019b-4433-81de-00d6e308620a" />
Admin panel where products, slides, and system data are managed.

### 🛍️ Product Catalog
<img width="1558" height="806" alt="Captura de pantalla 2026-04-24 a la(s) 7 54 24 p  m" src="https://github.com/user-attachments/assets/aa30083a-0089-40d7-a092-97b310fcaa43" />
Public view where users can browse and filter products by category, color, size, and title.

### 🏠 Home Page
<img width="1579" height="803" alt="Captura de pantalla 2026-04-24 a la(s) 7 53 40 p  m" src="https://github.com/user-attachments/assets/ea1c5dac-76c9-4e74-991b-d0e5e3830ec7" />

## Coming updates

- Expand the dashboard with more options to manage user sessions, roles, and permissions.
- Integrate a payment system and shopping cart to allow direct product orders.
- Implement a full order management system to track and handle customer purchases efficiently.
- Improve frontend architecture and optimize performance for faster load times and smoother interactions.
