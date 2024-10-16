FROM node:21-alpine3.20
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY package.json tsconfig.json webpack.config.js .env ./
#RUN touch .env
RUN yarn
COPY . ./
RUN yarn build
EXPOSE 443 4010
CMD ["yarn", "start"]
