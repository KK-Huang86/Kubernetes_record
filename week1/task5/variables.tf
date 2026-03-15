variable "linode_token" {
  description = "Linode API token"
  type        = string
  sensitive   = true
}

variable "cluster_name" {
  description = "LKE cluster name"
  type        = string
  default     = "k8s-practice"
}

variable "k8s_version" {
  description = "Kubernetes version"
  type        = string
  default     = "1.31"
}

variable "region" {
  description = "Linode region"
  type        = string
  default     = "ap-southeast" # Singapore
}

variable "node_type" {
  description = "Linode instance type for worker nodes"
  type        = string
  default     = "g6-standard-2" # 2 vCPU, 4GB RAM
}

variable "node_count" {
  description = "Number of worker nodes"
  type        = number
  default     = 2
}
