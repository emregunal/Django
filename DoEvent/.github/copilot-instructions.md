# AI Agent Instructions for DoEvent Project

## Project Overview
DoEvent is a Django-based event management system with two main domains:
- **Academic** (`Akademik/`): Handles academic calendars, attendance tracking, and appointment systems
- **Social** (`Sosyal/`): Manages events, clubs, and social activities

## Project Structure
```
DoEvent/
├── Akademik/           # Academic domain
│   ├── AkademikTakvim/     # Academic calendar
│   ├── DevamsizlikTakvimi/ # Attendance tracking
│   └── RandevuSistemi/     # Appointment system
├── Core/               # Core application functionality
└── Sosyal/            # Social domain
    ├── Etkinlik/           # Events management
    ├── EtkinlikOner/       # Event suggestions
    ├── Kulup/             # Clubs management
    └── KulupOner/         # Club suggestions
```

## Key Development Patterns

### Application Organization
- Each major feature is organized as a separate Django app within its domain directory
- Templates are stored in `templates/` directories within each app
- URLs are configured hierarchically from the project root through domain and feature levels

### URL Patterns
- Main project URLs are in `DoEvent/urls.py`
- Each domain (`Akademik/`, `Sosyal/`) has its own `urls.py`
- Feature-specific URLs are in their respective app directories (e.g., `Akademik/RandevuSistemi/urls.py`)

### Development Environment
- Uses SQLite database (`db.sqlite3`)
- Debug mode is enabled in development
- Static files are served from `static/` directory

## Common Development Tasks

### Running the Development Server
```bash
python manage.py runserver
```

### Database Migrations
When modifying models:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Adding New Features
1. Create a new app in the appropriate domain directory
2. Add the app to `INSTALLED_APPS` in `settings.py`
3. Create necessary models, views, and templates
4. Include app URLs in the domain's `urls.py`

## Areas Requiring Special Attention
- Django debug mode is enabled - should be disabled in production
- Template configurations might need adjustment for more complex views
- Database is SQLite - may need migration to production database
- Static file handling needs configuration for production deployment

## Key Files for Reference
- `DoEvent/settings.py` - Main project configuration
- `DoEvent/urls.py` - Root URL configuration
- Domain-level `urls.py` files for routing structure examples
- Feature-level templates for UI patterns