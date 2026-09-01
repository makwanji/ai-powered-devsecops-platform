# Install

```bash
helm repo add defectdojo https://raw.githubusercontent.com/DefectDojo/django-DefectDojo/helm-charts
helm repo update

kubectl create namespace defectdojo
helm upgrade --install defectdojo defectdojo/defectdojo --namespace defectdojo -f my-values.yaml
```
