terraform {
  required_version = ">= 1.6"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
  # Remote state per environment. Commented so 'terraform validate' runs without credentials.
  # backend "azurerm" {
  #   resource_group_name  = "rg-tfstate"
  #   storage_account_name = "sttfstatehybrid"
  #   container_name       = "tfstate"
  #   key                  = "dev.tfstate"
  # }
}

provider "aws" {
  region = "us-east-2"
}

provider "azurerm" {
  features {}
}

locals {
  env  = "dev"
  name = "racehub-${local.env}"
  tags = {
    environment = local.env
    owner       = "platform"
    managed_by  = "terraform"
  }
}

# Data plane on AWS: private network for ingestion workers
module "network" {
  source = "../../modules/aws-network"
  name   = local.name
  cidr   = "10.20.0.0/16"
  azs    = ["us-east-2a"]
  tags   = local.tags
}

# Customer-facing app on Azure
module "app" {
  source = "../../modules/azure-app"
  name   = local.name
  sku    = "B1"
  tags   = local.tags
  app_settings = {
    ENVIRONMENT = local.env
    AWS_VPC_ID  = module.network.vpc_id
  }
}

output "app_url" {
  value = "https://${module.app.app_hostname}"
}
