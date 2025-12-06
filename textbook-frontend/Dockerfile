# Stage 1: Build the Docusaurus app
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json yarn.lock ./

# Install dependencies
RUN yarn install --frozen-lockfile

# Copy the rest of the files
COPY . .

# Build the Docusaurus app
RUN yarn build

# Stage 2: Serve the app with nginx
FROM nginx:alpine AS production

# Copy the build output to replace the default nginx page
COPY --from=builder /app/build /usr/share/nginx/html

# Copy custom nginx configuration (optional)
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]