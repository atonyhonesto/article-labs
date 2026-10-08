<sub>[← all labs](../../README.md)</sub>

# A small Spring Boot REST API

> Controller, service, validation and error handling: the shape most Spring Boot APIs share.

`Java 21` · `Spring Boot 3` · `Maven` · `JUnit 5`

**Companion to:**
- [Spring Boot](https://www.linkedin.com/pulse/spring-boot-tony-honesto-ijwqc/)

## What it shows

- Records for request and response DTOs, with Bean Validation on the request.
- Constructor injection and a service layer that owns the business rules (no duplicate car numbers).
- One `@RestControllerAdvice` that turns exceptions into RFC 9457 problem details (400, 404, 409).
- MockMvc tests, Actuator health, and CI that starts the jar and calls it with curl.

## Run it

```bash
bash labs/spring-boot-api/ci.sh
# or:
mvn spring-boot:run
curl localhost:8080/api/entries
```

Real output (from this lab's CI run):

```text
$ curl -X POST localhost:8080/api/entries -H Content-Type: application/json -d {"number":24,"driver":"A. Driver","team":"Team Green"}
{"id":1,"number":24,"driver":"A. Driver","team":"Team Green"}  <- HTTP 201
$ curl -X POST localhost:8080/api/entries -H Content-Type: application/json -d {"number":150,"driver":"","team":"X"}
{"type":"about:blank","title":"Bad Request","status":400,"detail":"Validation failed","instance":"/api/entries","errors":{"driver":"driver is required","number":"car number must be 1-99"}}  <- HTTP 400
$ curl localhost:8080/api/entries
[{"id":1,"number":24,"driver":"A. Driver","team":"Team Green"}]  <- HTTP 200
$ curl localhost:8080/api/entries/7
{"type":"about:blank","title":"Not Found","status":404,"detail":"No entry with id 7","instance":"/api/entries/7"}  <- HTTP 404
```

## What's in here

| File | Purpose |
|---|---|
| `pom.xml` | Spring Boot 3 parent, web, validation, actuator |
| `src/main/java/` | Application, controller, service, DTOs, error handling |
| `src/test/java/` | MockMvc tests |
| `ci.sh` | Build, test, run and call the API |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| ConcurrentHashMap | Spring Data JPA with PostgreSQL and Flyway migrations |
| No security | Spring Security with OAuth2 resource server (JWT) |
| Actuator health only | Metrics to Prometheus, tracing with Micrometer |
