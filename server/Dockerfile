FROM node:14

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

COPY .dockerignore .

# Create a volume for server data
VOLUME /serverdata

EXPOSE 3000

CMD [ "npm", "start" ]
