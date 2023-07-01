# Goal
This a'la Enterprise Service Bus (ESB) service is a part of a project that required Service Oriented Architecture (SOA) implementation. We worked on a project in a group of four for a Master's class at the University of Aveiro. It demanded effective teamwork and communication skills.
# Noteworthy Aspects of the Project
 - OAuth e.g. Login via Google / Github / Facebook are feasible to implement
 - Contracts... In SOA, a contract defines the agreed-upon rules and expectations for service communication between providers and consumers.
 - Cookie-Based Auth is vulnerable to CSRD attacks, next time use more modern approach featuring Edge Auth
 - Consider using REST API instead of Queues when there is a need to reply-back
 - Repository pattern: isolates persistence layer from the app very well
 - Factory Pattern: When there is many of new Factories appearing, consider Abstract Factory for objects inheriting from the same parent class
 - Parametrizing environment variables is a must approach when the app meets deployment. Never push hardcoded secrets.
 - Authenticate, document and version REST API

# REST API
 - **REST:`GET`/`POST`/`PUT`/`DELETE`**
 - *"APIs are like resources"*
 - "*The issue with REST is that the server always must reply back… Synchronous nature…"*
## REST API Best practices

1. Never use verbs, use nouns
    1. DO NOT: `/getAllProducts`
    2. DO: `/products`
2. Use plurals
    1. DO NOT: `/product/all`
    2. DO:`/products`
3. Use parameters
    1. DO NOT: `/getProductsByName`
    2. DO: `/products?name=’ABC'`
4. Use proper HTTP codes - there is more than `200`, `403`, `500`, especially errors
5. Always version your APIs
    1. DO NOT: `/products`
    2. DO: `/v1/products`, later `/v2/products`
6. Use pagination (when you expose data to public and load balancing is done wrong)
    1. DO NOT: `/products?limit=99999999`
    2. DO: `/products?limit=25&offset=50`
7. Supported formats (mostly `JSON` or legacy `XML`)
8. Use OpenAPI specifications // documentation

# Message Oriented Middlewares
 - *"No need to reply back"*
## Queues advantages
1. Asynchronous
2. Reliable queuing
3. 1-to-1 interaction with failure resillience
4. 1-to-many interaction - improve performance, “*the message reaches everyone”*
5. many-to-many - as in replicated services for large amount of clients
6. Allow to implement complex interaction patterns
7. Flexibility at the cost of performance
8. Queues promote clustering


## Techstack
 - Backend: FastAPI
 - Auth: Auth0
 - Middlewares: ActiveMQ, Kubernetes Traefik (Ingress)
 - Persistence: MySQL
