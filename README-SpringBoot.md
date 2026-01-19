# Spring Boot Web Application

A simple Spring Boot web application with Maven that connects to backend REST APIs.

## Features

- **Web Interface**: Responsive web UI built with Bootstrap and Thymeleaf templates
- **REST API Integration**: Connects to external REST APIs (uses JSONPlaceholder as example)
- **Dual Interface**: Both web pages and REST endpoints available
- **Error Handling**: Graceful fallback to mock data when external APIs are unavailable
- **Modern Stack**: Spring Boot 3.2, Java 17, Maven, WebClient for async HTTP calls

## Project Structure

```
├── pom.xml                                 # Maven configuration
├── src/main/java/com/example/webapp/
│   ├── WebAppApplication.java              # Main Spring Boot application
│   ├── controller/
│   │   ├── WebController.java              # Web page controllers
│   │   └── ApiController.java              # REST API controllers
│   ├── service/
│   │   └── BackendService.java             # Service for external API calls
│   ├── model/
│   │   └── DataModel.java                  # Data model classes
│   └── config/
│       └── WebConfig.java                  # Web configuration
├── src/main/resources/
│   ├── application.properties              # Application configuration
│   ├── templates/
│   │   ├── index.html                      # Main page template
│   │   └── dashboard.html                  # Dashboard page template
│   └── static/
│       ├── css/style.css                   # Custom CSS styles
│       └── js/
│           ├── app.js                      # Main JavaScript
│           └── dashboard.js                # Dashboard JavaScript
```

## Prerequisites

- Java 17 or higher
- Maven 3.6 or higher

## Running the Application

1. **Clone or download the project**

2. **Build the application:**
   ```bash
   mvn clean compile
   ```

3. **Run the application:**
   ```bash
   mvn spring-boot:run
   ```

4. **Access the application:**
   - Web Interface: http://localhost:8080
   - Dashboard: http://localhost:8080/dashboard
   - REST API: http://localhost:8080/api/data

## API Endpoints

- `GET /api/data` - Fetch all data items
- `GET /api/data/{id}` - Fetch single data item by ID

## Configuration

The application can be configured via `src/main/resources/application.properties`:

- `backend.api.base-url`: External API base URL (default: https://jsonplaceholder.typicode.com)
- `server.port`: Application port (default: 8080)

## External API Integration

The application demonstrates connecting to external REST APIs using Spring WebClient. It uses JSONPlaceholder (a fake REST API) as an example backend. If the external API is unavailable, the application gracefully falls back to mock data.

## Technology Stack

- **Spring Boot 3.2**: Main framework
- **Spring Web**: Web MVC framework
- **Spring WebFlux**: Reactive HTTP client (WebClient)
- **Thymeleaf**: Server-side templating engine
- **Bootstrap 5**: Frontend CSS framework
- **Maven**: Build and dependency management
