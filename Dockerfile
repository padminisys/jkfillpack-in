# Use the official PHP image as a base, with Nginx
FROM php:7.4-fpm

# Install Nginx and required PHP extensions and dependencies
RUN apt-get update && apt-get install -y \
    nginx \
    libssl-dev \
    git \
    unzip \
    libzip-dev \
    && docker-php-ext-configure zip \
    && docker-php-ext-install sockets zip

# Install Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Set the working directory
WORKDIR /var/www/html

# Copy the composer.json and composer.lock files
COPY composer.json ./

# Install dependencies
RUN composer install

# Copy the rest of the project files into the working directory
COPY . .

# Copy custom Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Fix permissions
RUN chown -R www-data:www-data /var/www/html

# Expose port 80
EXPOSE 80

# Start Nginx and PHP-FPM
CMD ["sh", "-c", "php-fpm -D && nginx -g 'daemon off;'"]
