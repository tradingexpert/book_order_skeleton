This is a test implementation of a book ordering service/ API
---
### Docker deployment details  
Simply run:  
`docker-compose up -d`  

### For simple server installation use gunicorn
After  
`pip install gunicorn`  
Run it as follows:  
`gunicorn -k gevent --bind 0.0.0.0:9001 --workers 1 app`

### A few comments about what is definitely missing:  
- Authentication
- Logging!
- Handling emails, confirmation of requests and responses
- Migration - db tracking
