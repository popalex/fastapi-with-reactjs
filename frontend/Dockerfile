# Declare the build argument in the global scope
ARG REACT_APP_BACKEND_API_ARG=TEST

# Use an official Node runtime as a parent image
FROM node:20-alpine

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Consume the build argument in the build stage
ARG REACT_APP_BACKEND_API_ARG
ENV REACT_APP_BACKEND_API=${REACT_APP_BACKEND_API_ARG}

RUN echo $REACT_APP_BACKEND_API
# Build the React app
# WE need the env variable to be available at BUILD TIME
RUN npm run build

# Serve the app using serve
RUN npm install -g serve

# Expose the port the app runs on
EXPOSE 3000

# Command to run the app
CMD ["serve", "-s", "build", "-l", "3000"]
