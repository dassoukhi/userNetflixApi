FROM node:17

WORKDIR /app

COPY . .

RUN npm install
RUN npm install db-migrate-pg

CMD ["npm", "start"]