FROM node:22-alpine

WORKDIR /app

# Copiamos archivos de dependencias
COPY package*.json ./

# Usamos install para desarrollo y aseguramos que se generen los tipos de svelte-kit
RUN npm install

COPY . .

# Generar archivos de autocompletado e imports de SvelteKit
RUN npm run prepare

EXPOSE 5173

ENV HOST=0.0.0.0
ENV PORT=5173

# No hace falta pasarle los flags aquí si ya los tienes en el package.json, 
# pero dejarlo así no hace daño.
CMD ["npm", "run", "dev"]