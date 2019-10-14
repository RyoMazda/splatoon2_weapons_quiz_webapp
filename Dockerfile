FROM node:12.10.0-alpine

ENV WORKDIR /work
WORKDIR $WORKDIR

COPY package*.json $WORKDIR
RUN yarn install

COPY .browserslistrc $WORKDIR
COPY tsconfig.json $WORKDIR
COPY tslint.json $WORKDIR
COPY *.config.js $WORKDIR/
COPY public $WORKDIR/public
COPY tests $WORKDIR/tests
COPY src $WORKDIR/src

EXPOSE 8080
CMD yarn run serve
