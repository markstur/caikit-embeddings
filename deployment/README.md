# Caikit Embeddings Deployment

Deployment config for caikit embeddings.

## Deploy the Service

1. Connect to OCP cluser and desired project or create new one;

2. Get the OCP host and domain through the UI or:
```sh
oc get IngressController default -n openshift-ingress-operator -o jsonpath='{ .status.domain}'
```
Replace the host domain values at the router config at [deployment-caikit-embeddings.yaml](./deployment-caikit-embeddings.yaml).

3. Create the deployment using the file [deployment-caikit-embeddings.yaml](./deployment-caikit-embeddings.yaml)
 - Remember to point the `imagePullSecrets` name to the secrets where the icr iam key is kept.
 - Check if there are other values that need to be updated with variables or your cluster information.
   
4. You can apply the whole config yaml with the following command:
```bash
oc apply -f deployment-caikit-embeddings.yaml
```

Or you can create at the cluster GUI each of the components, the deployment, services, secrets and routes. 

5. Go to browser and access the route at `https://caikit-embeddings-route-<oc-project>.<oc-host>.<oc-domain>/docs` and you will be able to see swagger documentation for the API.

## Conditional GPU Allocation

The code for enabling GPU resource usage for sentence-transformers already handles the cuda/cpu selection automatically [SentenceTransformer.py](https://github.com/UKPLab/sentence-transformers/blob/master/sentence_transformers/SentenceTransformer.py#L104). However, the following configuration needs to be added to the [deployment-caikit-embeddings.yaml](./deployment-caikit-embeddings.yaml).

```yaml
  resources:
    limits:
      nvidia.com/gpu: "1"
```
Under `spec > spec > container > resources`, the above lines provide the GPU availability in cluster to be allocated.

## Enabling the gRPC UI for the service

1. Add another port to the current deployed service to expose the gRPC one:
```yaml
  ports:
    - name: server-port
      protocol: TCP
      port: 8080
      targetPort: 8080
    - name: grpc-port
      protocol: TCP
      port: 8085
      targetPort: 8085
```
2. Create a deployment using the file [deployment-caikit-emb-grpc-ui.yaml](deployment-caikit-emb-grpc-ui.yaml).

```bash
oc apply -f deployment-caikit-emb-grpc-ui.yaml
```
This will create the deployment, service and route to access the gRPC at the browser. 

### For TLS enablement check the documentation at [deployment/tls-enablement](./tls-enablement/README.md).

> Remember to check if the host passed as parameters in `spec > containers > args` on the gRPC UI deployment has the same name as the caikit embeddings service.

Opening the route created, you should be able to see this view:
![grpc_ui](./assets/grpc-ui.png)

## Onboarding models

- The `demo/models` folder is now a PVC monted, that points to a bucket named `caikit-embeddings-models-config`;
> PVC yaml can be found at [pvc-models.yaml](pvc-models.yaml)
- Each user of the service can upload the models they wish to use, as long as they follow the same structure as before. 
- Then, in the [deploymentconfig-caikit-embeddings.yaml](deploymentconfig-caikit-embeddings.yaml) the environment variable `MODELS_LIST` must receive a list with the models' root folder names as in the example: `'["mini", "slate"]'` in the json list standard, so that the app can acknowledge the models' location before start the runtime.