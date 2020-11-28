FROM node as builder-node
COPY app/static/package*.json /tmp/
RUN cd /tmp/ &&  npm install

FROM python:3.7
# Install deployment dependencies
RUN pip3 install --no-cache-dir uwsgi psycopg2

# Install sources
WORKDIR /usr/src/app
COPY . .
COPY --from=builder-node /tmp/node_modules app/static/node_modules

# Install application dependencies from pypi to get latests versions
RUN pip3 install --no-cache-dir .

CMD ["uwsgi", "--ini", "/usr/src/app/uwsgi.conf"]
