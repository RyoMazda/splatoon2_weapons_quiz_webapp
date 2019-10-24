FROM python:3.7-alpine as scraper
RUN pip install --upgrade pip && pip install \
  requests \
  BeautifulSoup4 \
  Jinja2
COPY scraping .
RUN python scraper.py


FROM node:12.10.0-alpine

ENV WORKDIR /work
WORKDIR $WORKDIR

COPY package*.json .
RUN yarn install

COPY .browserslistrc .
COPY tsconfig.json .
COPY tslint.json .
COPY *.config.js ./
COPY public public
COPY tests tests
COPY src src
COPY --from=scraper /weapons.ts src/weapons.ts

EXPOSE 8080
CMD yarn run serve
