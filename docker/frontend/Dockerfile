FROM node:alpine3.11

RUN apk add --update python3 make g++\
   && rm -rf /var/cache/apk/*

RUN mkdir -p /app
WORKDIR /app

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ .

RUN npm run build

EXPOSE $PORT
ENV NUXT_HOST=0.0.0.0

ENV NUXT_PORT=$PORT
ENV REACT_APP_API_URL=$REACT_APP_API_URL

# Start the app
CMD [ "npm", "start" ]