module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "campus-llm-vpc"
  cidr = "10.0.0.0/16"

  # We use two Availability Zones for "High Availability"
  # This is a requirement for professional RDS setups
  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  # Allows private resources (like your DB) to reach out 
  # for updates without being reached from the outside
  enable_nat_gateway = true
  single_nat_gateway = true

  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Environment = "staging"
    Project     = "Campus-LLM"
  }
}
