# Django Contact Manager with Custom User Management

## Custom User

A full-featured Django web application featuring a custom user model and a modern Tailwind CSS UI. It includes user registration, login, logout, profile viewing and updating, and secure profile deletion with password confirmation.

---

### 🚀 Features

- Custom user model (`CustomUser`)
- Tailwind CSS–styled forms and templates
- Register new users with profile images and bios
- Login/logout with session management
- Profile page with image display and fallback initials
- Profile update functionality
- Password-confirmed profile deletion
- Server-side image resizing and optimization (400x400, JPEG)
- Reusable Django messages with fading alerts
- Fully responsive, modern UI

---

## Django Contacts Application

A comprehensive Django-based contacts management system that allows authenticated users to efficiently manage their personal and professional contacts. The application supports creating, reading, updating, and deleting (CRUD) contacts, as well as searching and filtering contacts by various attributes.

---

### 🚀 Features

- **User Authentication:** All features require users to be logged in, ensuring the privacy and security of contacts.
- **Add Contacts:** Users can add new contacts, including uploading files (e.g., profile pictures).
- **View Contacts:** Paginated listing of contacts (50 contacts per page), sorted by creation date.
- **Contact Details:** View full details of any contact.
- **Update Contacts:** Edit existing contact information.
- **Delete Contacts:** Remove contacts permanently.
- **Search:** Quickly find contacts by first name, last name, email, or phone number with case-insensitive partial matching.
- **Filter Contacts:** Filter contacts by city, state, country, contact type, and preferred communication method, with each filter view paginated.
- **Flash Messages:** User-friendly success messages appear after adding, updating, or deleting contacts.
- **Pagination:** Large contact lists are handled efficiently with Django’s paginator, ensuring smooth performance.

---

## 🛠️ Tech Stack

- **Backend:** Django, Python
- **Frontend:** Tailwind CSS
- **Image Processing:** Pillow (PIL)
- **Database:** SQLite (default, easily configurable)
- **Version Control:** Git and GitHub

---

## 📦 Installation & Setup (Optional)

```bash
# Clone the repository
git clone https://github.com/shinde-abhijit/django-contacts.git
cd yourrepo

# Create virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create a superuser (optional)
python manage.py createsuperuser

# Run the development server
python manage.py runserver
