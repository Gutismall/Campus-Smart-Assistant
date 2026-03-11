FROM node:20-alpine
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Build the Next.js/React application for production
RUN npm run build

EXPOSE 3000

# Run in production mode
CMD ["npm", "run", "start"]
