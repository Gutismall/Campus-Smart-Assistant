# 1. Create the Cluster
resource "aws_ecs_cluster" "main" {
  name = "campus-cluster"
}

# 2. Define the Backend Task
resource "aws_ecs_task_definition" "backend" {
  family                   = "campus-backend"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "ARM64"
  }

  container_definitions = jsonencode([{
    name         = "backend"
    image        = "${aws_ecr_repository.backend.repository_url}:latest" # Point to your ECR URL
    portMappings = [{ containerPort = 8000, hostPort = 8000 }]
    environment = [
      { name = "DATABASE_URL", value = "postgresql://campus_admin:${var.db_password}@${aws_db_instance.campus_db.endpoint}/campus_data_db" }
    ]
  }])
}

# 3. Launch the Backend Service
resource "aws_ecs_service" "backend" {
  name            = "campus-backend-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.backend.arn
  launch_type     = "FARGATE"
  desired_count   = 1

  network_configuration {
    subnets          = module.vpc.public_subnets
    assign_public_ip = true # So you can reach it via IP for now
    security_groups  = [aws_security_group.app_sg.id]
  }
}
# 1. Define the Frontend Task
resource "aws_ecs_task_definition" "frontend" {
  family                   = "campus-frontend"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "ARM64"
  }

  container_definitions = jsonencode([{
    name  = "frontend"
    image = "${aws_ecr_repository.frontend.repository_url}:latest"
    portMappings = [{
      containerPort = 3000 # Or 80, 5173 - whatever your frontend uses
      hostPort      = 3000
    }]

    # This is how the React/Express app knows where to send API calls
    environment = [
      { name = "BACKEND_API_URL", value = "http://54.90.69.229:8000" }
    ]
  }])
}

# 2. Launch the Frontend Service
resource "aws_ecs_service" "frontend" {
  name            = "campus-frontend-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.frontend.arn
  launch_type     = "FARGATE"
  desired_count   = 1

  network_configuration {
    subnets          = module.vpc.public_subnets
    assign_public_ip = true
    security_groups  = [aws_security_group.app_sg.id]
  }
}
