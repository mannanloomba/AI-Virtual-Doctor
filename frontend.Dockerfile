FROM node:18-alpine

WORKDIR /app

# Copy package.json and package-lock.json
COPY ai-virtual-doctor-ui/package*.json ./

# Install dependencies
RUN npm install

# Copy frontend source code
COPY ai-virtual-doctor-ui/ .

# Build the app (if we wanted to serve static files, but for simple deployment we can just use the dev server or serve build)
# RUN npm run build
# RUN npm install -g serve
# CMD ["serve", "-s", "dist", "-p", "5173"]

# For simplicity, we'll run the dev server exposing all hosts
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]
