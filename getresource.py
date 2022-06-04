from kubernetes import client, config
from kubernetes.client import configuration
from pick import pick  # install pick using `pip install pick`
from pprint import pprint

def main():
    contexts, active_context = config.list_kube_config_contexts()
    if not contexts:
        print("Cannot find any context in kube-config file.")
        return
    contexts = [context['name'] for context in contexts]
    active_index = contexts.index(active_context['name'])
    cluster1, first_index = pick(contexts, title="Pick the first context",
                                 default_index=active_index)

    client1 = client.CoreV1Api(
        api_client=config.new_client_from_config(context=cluster1))
    
    # print("\nList of pods on %s:" % cluster1)
    # for i in client1.list_pod_for_all_namespaces().items:
    #     print("%s\t%s\t%s" %
    #           (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
    
    result = client1.list_namespace()
    # for i in result.items:
    #     print("%s" %
    #           (i.metadata.name)) 
    
    client2 = client.AppsV1Api( 
        api_client=config.new_client_from_config(context=cluster1))
    result = client2.list_namespaced_deployment(namespace="lineman-beta")
    
    # pprint(result)
    for i in result.items:
        print("%s\t|\t%s\t|\t%s\t|\t%s" %
              (i.metadata.name,i.metadata.namespace,i.spec.replicas,i.spec.template.spec.containers[0].resources))
        # if i.spec.template.spec.containers.resources == 0 :
        #     print("None")
        # else:
        #     print("%s\n" %
        #         (i.spec.template.spec.containers.resources)) 


if __name__ == '__main__':
    main()