FROM node:18

# Create app directory and set permissions
WORKDIR /app
RUN mkdir -p /app/node_modules && chown -R node:node /app

# Switch to non-root user
USER node

# Copy package.json and package-lock.json
COPY --chown=node:node package*.json ./

# Install dependencies
RUN npm install

# Install Angular CLI locally (not globally)
RUN npm install @angular/cli

# Copy the rest of the application code
COPY --chown=node:node . .

# Expose the port the app runs on
EXPOSE 4200

# Command to run the application
CMD ["npm", "start"]