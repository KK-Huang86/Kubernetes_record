terraform {
  required_providers {
    linode = {
      source  = "linode/linode"
      version = "~> 2.0"
    }
  }
}

provider "linode" {
  token = var.linode_token
}

resource "linode_lke_cluster" "k8s" {
  label       = var.cluster_name
  k8s_version = var.k8s_version
  region      = var.region

  pool {
    type  = var.node_type
    count = var.node_count
  }
}
