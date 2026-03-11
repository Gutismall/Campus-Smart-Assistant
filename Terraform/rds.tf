# This groups our private subnets together for the DB to use
resource "aws_db_subnet_group" "campus_db_subnets" {
  name       = "campus-db-subnets"
  subnet_ids = module.vpc.private_subnets

  tags = {
    Name = "Campus DB Subnet Group"
  }
}

resource "aws_db_instance" "campus_db" {
  identifier        = "campus-data-db"
  engine            = "postgres"
  engine_version    = "17"          # Matches your local Docker version
  instance_class    = "db.t3.micro" # AWS Free Tier eligible
  allocated_storage = 20
  storage_type      = "gp2"

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password # We will move this to a secret later

  db_subnet_group_name   = aws_db_subnet_group.campus_db_subnets.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]

  skip_final_snapshot = true  # Set to true for dev/test to avoid extra costs
  publicly_accessible = false # Crucial: Keeps the DB hidden in the private subnet
}
