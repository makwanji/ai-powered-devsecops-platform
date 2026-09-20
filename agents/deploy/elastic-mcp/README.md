#

## Get Password

```bash
kubectl -n elastic get secret quickstart-es-elastic-user -o go-template='{{.data.elastic | base64decode}}'
```

## Get Token

```bash
curl -k -u elastic:'xRMl5UjYANuTFVe7LhNAGVcX' \
  -X POST "https://127.0.0.1:9200/_security/api_key" \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "elastic-mcp-full-access",
    "role_descriptors": {}
  }'


<<K9s-Shell>> Pod: elastic/quickstart-es-default-0 | Container: elasticsearch
elasticsearch@quickstart-es-default-0:~$ curl -k -u elastic:'xRMl5UjYANuTFVe7LhNAGVcX' \
>   -X POST "https://127.0.0.1:9200/_security/api_key" \
>   -H 'Content-Type: application/json' \
>   -d '{
>     "name": "elastic-mcp-full-access",
>     "role_descriptors": {}
>   }'
{"id":"o-ravaABmocbrbjB_mt4","name":"elastic-mcp-full-access","api_key":"8PsGENd8RfayZUKxb9mdkg","encoded":"by1yYXZhQUJtb2NicmJqQl9tdDQ6OFBzR0VOZDhSZmF5WlVLeGI5bWRrZw=="}elasticsearch@quickstart-es-default-0:~$

```

## Test connection

```bash
echo -n 'elastic:xRMl5UjYANuTFVe7LhNAGVcX' | base64

kubectl run elastic-test -n ai-platform --rm -it --image=curlimages/curl --restart=Never -- sh

curl -k \
    -u 'elastic:xRMl5UjYANuTFVe7LhNAGVcX' \
    https://quickstart-es-http.elastic.svc:9200/_cluster/health

curl -k \
  -H "Authorization: ApiKey Mi1yb3ZhQUJtb2NicmJqQlNJYjM6SlZzQmlxMFpSTktfazZaTlFWR01WQQ==" \
  https://quickstart-es-http.elastic.svc:9200/_cat/indices?v
```

## Rollout restart

```bash
kubectl rollout restart deployment elastic-mcp -n ai-platform
```

<http://kubernetes-mcp.ai-platform.svc.cluster.local:8080/mcp>
