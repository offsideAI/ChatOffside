# ChatOffside API Documentation

This document provides detailed information about the ChatOffside API endpoints, authentication, and data models.

## Base URL

The API is served at the root path `/` with API version 0.1.0.

## Authentication

The API uses OAuth2 Password Bearer authentication.

### Login
```http
POST /login
```

Authenticate a user and receive an access token.

**Request Body (form-data)**:
- `username`: User's email
- `password`: User's password

**Response**:
- `200`: Successfully authenticated
- `422`: Validation Error

## Posts

### Create Post
```http
POST /posts/
```
Create a new post. Requires authentication.

**Request Body**:
```json
{
  "title": "string",
  "body": "string"
}
```

**Response**:
- `200`: Successfully created post
- `422`: Validation Error

### List Posts
```http
GET /posts
```
Retrieve a list of posts. Requires authentication.

**Query Parameters**:
- `offset` (optional): Number of items to skip (default: 0)
- `limit` (optional): Maximum number of items to return (default: 100, max: 100)

**Response**:
- `200`: Array of posts
- `422`: Validation Error

### Get Post
```http
GET /posts/{post_id}
```
Retrieve a specific post by ID. Requires authentication.

**Parameters**:
- `post_id`: Integer ID of the post

**Response**:
- `200`: Post details with user information
- `422`: Validation Error

### Update Post
```http
PATCH /posts/{post_id}
```
Update an existing post. Requires authentication.

**Parameters**:
- `post_id`: Integer ID of the post

**Request Body**:
```json
{
  "title": "string",
  "body": "string"
}
```

**Response**:
- `200`: Updated post details
- `422`: Validation Error

### Delete Post
```http
DELETE /posts/{post_id}
```
Delete a post. Requires authentication.

**Parameters**:
- `post_id`: Integer ID of the post

**Response**:
- `200`: Success
- `422`: Validation Error

## Prompts

### Create Prompt
```http
POST /prompts/
```
Create a new prompt. Requires authentication.

**Request Body**:
```json
{
  "title": "string",
  "body": "string"
}
```

**Response**:
- `200`: Successfully created prompt
- `422`: Validation Error

### List Prompts
```http
GET /prompts
```
Retrieve a list of prompts. Requires authentication.

**Query Parameters**:
- `offset` (optional): Number of items to skip (default: 0)
- `limit` (optional): Maximum number of items to return (default: 100, max: 100)

**Response**:
- `200`: Array of prompts
- `422`: Validation Error

## Professions

### List Professions
```http
GET /professions
```
Retrieve a list of professions. Requires authentication.

**Query Parameters**:
- `offset` (optional): Number of items to skip (default: 0)
- `limit` (optional): Maximum number of items to return (default: 100, max: 100)

**Response**:
- `200`: Array of professions
- `422`: Validation Error

## Users

### List Users
```http
GET /users/
```
Retrieve a list of users. Requires authentication.

**Query Parameters**:
- `offset` (optional): Number of items to skip (default: 0)
- `limit` (optional): Maximum number of items to return (default: 100, max: 100)

**Response**:
- `200`: Array of users
- `422`: Validation Error

## OffsideAI Integration

### Function Calling
```http
GET /offsideai/functioncalling
```
Endpoint for AI function calling capabilities.

**Response**:
- `200`: Function calling response
- `422`: Validation Error

## Error Responses

All endpoints may return the following error response for validation errors:

```json
{
  "detail": [
    {
      "loc": ["string"],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## Security

All endpoints (except `/login`) require authentication using OAuth2 Password Bearer token:

```http
Authorization: Bearer <access_token>
```

## Rate Limiting

Please be mindful of API usage and implement appropriate rate limiting in your applications. Contact the API administrators for specific rate limit details.

## API Versioning

Current API version: 0.1.0

The API follows semantic versioning. Breaking changes will be communicated through version updates.

## Additional Resources

- Interactive API documentation: `/docs`
- OpenAPI Specification: `/openapi.json`
- ReDoc documentation: `/redoc`
