FROM node:20-alpine
WORKDIR /app
COPY package.json .
RUN npm install
COPY src/ ./src/
COPY public/ ./public/
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD wget -q -O- http://localhost:3000
CMD ["npm", "run", "dev"]
