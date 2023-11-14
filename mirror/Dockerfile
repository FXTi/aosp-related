FROM alpine:latest

RUN apk add git-daemon

CMD ["/usr/libexec/git-core/git-daemon", "--export-all", "--base-path=/srv/git", "--verbose", "--informative-errors", "--enable=receive-pack", "--listen=0.0.0.0", "--port=9418", "/srv/git"]
