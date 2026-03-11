FROM node:20-alpine
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Set the API URL for the production build
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

# Build the Next.js/React application for production
RUN npm run build

EXPOSE 3000

# Run in production mode
CMD ["npm", "run", "start"]
