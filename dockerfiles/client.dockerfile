FROM node:18-alpine

WORKDIR /app

COPY ./client/package.json ./

RUN npm install

COPY ./client .

CMD ["npm", "run", "dev"]