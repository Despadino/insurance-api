```shell
    #generate private rsa key
    openssl genrsa -out private.pem 2048
```

```shell
    #generate public rsa key
    openssl rsa -in private.pem -outform PEM -pubout -out public.pem
```
