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
      { name = "DATABASE_URL", value = "postgresql://${var.db_username}:${var.db_password}@${aws_db_instance.campus_db.endpoint}/${var.db_name}" },
      { name = "ADMIN_EMAIL", value = var.admin_email },
      { name = "ADMIN_PASSWORD", value = var.admin_password },
      { name = "GEMINI_API_KEY", value = var.gemini_api_key },
      { name = "JWT_SECRET", value = var.jwt_secret },
      { name = "TEXT_TO_SQL_SCHEMA_CONTEXT", value = var.text_to_sql_schema_context }
    ],
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = aws_cloudwatch_log_group.ecs_logs.name
        "awslogs-region"        = "us-east-1"
        "awslogs-stream-prefix" = "backend"
      }
    }
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
    assign_public_ip = true
    security_groups  = [aws_security_group.app_sg.id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.backend_tg.arn
    container_name   = "backend"
    container_port   = 8000
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
      { name = "NEXT_PUBLIC_API_URL", value = "http://${aws_lb.campus_alb.dns_name}:8000" }
    ],
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = aws_cloudwatch_log_group.ecs_logs.name
        "awslogs-region"        = "us-east-1"
        "awslogs-stream-prefix" = "frontend"
      }
    }
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

  load_balancer {
    target_group_arn = aws_lb_target_group.frontend_tg.arn
    container_name   = "frontend"
    container_port   = 3000
  }
}
