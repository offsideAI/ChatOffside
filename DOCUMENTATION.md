# ChatOffside Developer Documentation

## Overview
ChatOffside is a FastAPI-based web application that provides AI-powered chat and vision capabilities, along with user management and content organization features. The application uses SQLModel for database operations and integrates with OpenAI's GPT models for AI functionality.

## Architecture

### Core Components

1. **FastAPI Application (`main.py`)**
   - Main application entry point
   - CORS middleware configuration
   - Admin interface setup
   - Router integration
   - Database initialization

2. **Data Models (`models.py`)**
   - SQLModel-based data models
   - Key entities:
     - User
     - Post
     - Prompt
     - Project
     - Profession
     - UserProfessionLink (many-to-many relationship)

3. **API Routers**
   - `authentication.py`: User authentication endpoints
   - `offsideai.py`: AI-powered features using OpenAI
   - `post.py`: Blog post management
   - `prompt.py`: AI prompt management
   - `project.py`: Project management
   - `profession.py`: Profession management
   - `user.py`: User management
   - `currency.py`: Currency-related functionality

## Database Schema

### Core Tables
- **users**: User information and authentication
- **posts**: Blog posts with author relationships
- **prompts**: AI prompts with author relationships
- **projects**: Project information with author relationships
- **professions**: Professional categories
- **user_profession_link**: Many-to-many relationship between users and professions

## API Endpoints

### Authentication
- Login and token generation
- User registration
- Protected route authentication using JWT

### AI Features (`/offsideai`)
- `/jsonfunctioncalling`: Generate JSON responses using GPT-4
- `/functioncalling`: Generate regular text responses
- `/vision`: Process and analyze images
- `/urlvision`: Analyze images from URLs
- `/docvision`: Document analysis and interpretation
- `/visioncounter`: Vision-based counting functionality

### Content Management
- CRUD operations for posts, prompts, and projects
- User profile management
- Profession management

## Security

1. **Authentication**
   - JWT-based authentication
   - Password hashing
   - Admin role support

2. **Admin Interface**
   - Protected admin routes
   - Role-based access control
   - Model management interface

## Development Setup

### Environment Variables
- `SECRET_KEY`: JWT secret key
- `ALGORITHM`: JWT algorithm
- OpenAI API configuration
- Database connection settings

### Database
- SQLite database for development
- Automatic table creation in development mode
- Migration support using Alembic

## Best Practices

1. **Code Organization**
   - Modular router structure
   - Clear separation of concerns
   - Type hints and Pydantic models

2. **API Design**
   - RESTful endpoints
   - Consistent error handling
   - Input validation

3. **Security**
   - Protected routes
   - Proper error handling
   - Environment variable management

## Dependencies

- FastAPI
- SQLModel
- OpenAI
- Python-Jose (JWT)
- SQLAdmin
- Other requirements in `requirements.txt`

## Error Handling

The application uses FastAPI's built-in exception handling:
- HTTPException for API errors
- Database exceptions handling
- Custom error responses

## Testing

- Database connection testing available
- API endpoint testing recommended
- Authentication flow testing

## Deployment

1. **Environment Setup**
   - Set production environment variables
   - Configure database connections
   - Set up CORS policies

2. **Database Migration**
   - Use Alembic for schema migrations
   - Follow migration scripts in `/app/alembic`

3. **Security Considerations**
   - Secure all environment variables
   - Configure proper CORS settings
   - Set up proper SSL/TLS

## Maintenance

1. **Monitoring**
   - Log error handling
   - API endpoint monitoring
   - Database performance

2. **Updates**
   - Regular dependency updates
   - Security patch management
   - API version management

## Contributing

1. **Code Style**
   - Follow PEP 8 guidelines
   - Use type hints
   - Document new features

2. **Pull Requests**
   - Include tests
   - Update documentation
   - Follow existing patterns

## Support

Refer to:
- `README.md` for basic setup
- `SETUP.md` for detailed installation
- `MIGRATIONS.md` for database changes
- `CONTRIBUTOR.md` for contribution guidelines