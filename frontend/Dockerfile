# Build stage only - output used by nginx gateway
FROM docker.io/library/node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN VITE_API_URL=/api npm run build

# Minimal image to hold the built files
FROM docker.io/library/alpine:latest
COPY --from=build /app/dist /dist
CMD ["sleep", "infinity"]
