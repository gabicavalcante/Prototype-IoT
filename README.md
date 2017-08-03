# Prototype-IoT


web:
  restart: always
  build: ./web
  container_name: prototype-iot
  ports:
    - 5000:5000
  env_file: .env
  volumes:
    - .:/code

mongodb:
  image: mongo:latest
  container_name: mongodb
  environment:
    - MONGO_DATA_DIR=/data/db
    - MONGO_LOG_DIR=/dev/null
  volumes:
    - ./data/db:/data/db
  ports:
    - 27017:27017
  command: mongod --smallfiles --logpath=/dev/null # --quiet