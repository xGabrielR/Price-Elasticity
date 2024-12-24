

```sh
docker build . -t airflow-with-aws-and-trino:2.10.2 --platform linux/amd64
docker tag airflow-with-aws-and-trino:2.10.2 gabrielrichter/airflow-with-aws-and-trino:2.10.2
docker push gabrielrichter/airflow-with-aws-and-trino:2.10.2
```

