output "cluster_id" {
  description = "LKE cluster ID"
  value       = linode_lke_cluster.k8s.id
}

output "kubeconfig" {
  description = "Kubeconfig for the cluster (base64 decoded)"
  value       = base64decode(linode_lke_cluster.k8s.kubeconfig)
  sensitive   = true
}
