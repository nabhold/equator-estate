# Use the official Nginx image as the base
FROM nginx:alpine

# Install necessary tools (e.g., OpenSSL for TLS, Bash for scripting)
RUN apk update && apk add --no-cache openssl bash

# Set the working directory for Nginx
WORKDIR /etc/nginx

# Remove the default Nginx configuration to prevent conflicts
RUN rm /etc/nginx/conf.d/default.conf

# Copy over the main nginx.conf and custom site configuration
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./custom-site.conf /etc/nginx/conf.d/custom-site.conf

# Copy SSL certificates (uncomment if using SSL)
# Ensure you securely manage your certificates
# COPY ./certs/fullchain.pem /etc/nginx/ssl/fullchain.pem
# COPY ./certs/privkey.pem /etc/nginx/ssl/privkey.pem

# Optionally, copy static and media files if needed
# COPY ./static /app/static
# COPY ./media /app/media

# Expose ports for HTTP and HTTPS
EXPOSE 80 443

# Health check (uncomment if you want to use it)
# Useful in orchestration tools like Docker Compose
# HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl --fail http://localhost:80 || exit 1

# Run Nginx in the foreground to keep the container running
CMD ["nginx", "-g", "daemon off;"]
