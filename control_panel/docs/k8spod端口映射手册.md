```yaml
apiVersion: v1
kind: Service
metadata:
  name: notebook-multi-port-svc
  namespace: notebook-2a6e891b17d2
spec:
  type: NodePort
  selector:
    app: notebook-2a6e891b17d2
  ports:
    - name: port-31555
      protocol: TCP
      port: 31555
      targetPort: 31555
      nodePort: 31555
    - name: port-32703
      protocol: TCP
      port: 32703
      targetPort: 32703
      nodePort: 32703
    - name: port-31758
      protocol: TCP
      port: 31758
      targetPort: 31758
      nodePort: 31758
    - name: port-31944
      protocol: TCP
      port: 31944
      targetPort: 31944
      nodePort: 31944
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: notebook-multi-port-allow
  namespace: notebook-2a6e891b17d2
  ownerReferences:
  - apiVersion: v1
    kind: Pod
    name: notebook-2a6e891b-17d2-4a70-98d7-b92689b38ec7-5c5b64c5c6-kgx5w
    uid: ed6a5aa4-30e8-4f94-a207-b0b7185ef021
spec:
  ingress:
  - from: []
    ports:
    - protocol: TCP
      port: 31555
    - protocol: TCP
      port: 32703
    - protocol: TCP
      port: 31758
    - protocol: TCP
      port: 31944
  podSelector:
    matchLabels:
      project_id: ws-d8t5nq1uma3bg0ocu5cg
      workspace_id: es-d8640touuv8854a539jg
  policyTypes:
  - Ingress

```

创建好yaml之后直接kubectl apply就可以了