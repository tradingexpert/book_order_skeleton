This is a test implementation of a book requesting service/ API
---
Docker deployment details:  
simply run:  
docker-compose up -d  

### For simple server installation use gunicorn
pip install gunicorn  
And run it:  
gunicorn -k gevent --bind 0.0.0.0:9001 --workers 1 app  
