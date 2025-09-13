# syntax=docker/dockerfile:1
FROM node:20-alpine AS deps
WORKDIR /app
# Install fonts and fontconfig
RUN apk add --no-cache fontconfig ttf-dejavu ttf-liberation
COPY package.json package-lock.json* ./
RUN npm ci --no-audit --no-fund

FROM node:20-alpine AS builder
WORKDIR /app
# Install fonts and fontconfig
RUN apk add --no-cache fontconfig ttf-dejavu ttf-liberation
COPY --from=deps /app/node_modules ./node_modules
COPY . .
# Ensure NEXT_PUBLIC_* envs are set from compose
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
# Install fonts and fontconfig
RUN apk add --no-cache fontconfig ttf-dejavu ttf-liberation
ENV NODE_ENV=production \
    PORT=3000
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY package.json ./
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "node_modules/next/dist/bin/next", "start", "-p", "3000"]
