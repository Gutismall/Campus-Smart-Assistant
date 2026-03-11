# 1. The Security Group for our App (Frontend & Backend)
resource "aws_security_group" "app_sg" {
  name        = "campus-app-sg"
  description = "Security group for ECS backend that needs to access RDS"
  vpc_id      = module.vpc.vpc_id

  # Door for Backend (FastAPI)
  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Door for Frontend (React/Express/Vite)
  ingress {
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow containers to reach the internet (to pull updates or talk to ECR)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 2. The Security Group for RDS (Database)
resource "aws_security_group" "rds_sg" {
  name        = "campus-db-sg"
  description = "Allow inbound traffic to PostgreSQL"
  vpc_id      = module.vpc.vpc_id

  # Inbound: Allow PostgreSQL traffic from the App Security Group
  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app_sg.id] # Only the app can talk to the DB
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
