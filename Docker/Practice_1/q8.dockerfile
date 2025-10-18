FROM alpine:latest
ENV MYFLAG="CTF"
CMD ["sh", "-c", "echo MYFLAG: $MYFLAG"]