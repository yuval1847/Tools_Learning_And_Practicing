FROM busybox:latest
WORKDIR /app
CMD sh -c "mkdir -p /app/data && echo 'hello' > /app/data/hello.txt"
