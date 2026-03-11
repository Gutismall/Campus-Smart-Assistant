# The Application Load Balancer
resource "aws_lb" "campus_alb" {
  name               = "campus-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.app_sg.id]
  subnets            = module.vpc.public_subnets
}

# Target Group for Backend
resource "aws_lb_target_group" "backend_tg" {
  name        = "campus-backend-tg"
  port        = 8000
  protocol    = "HTTP"
  vpc_id      = module.vpc.vpc_id
  target_type = "ip"

  health_check {
    path                = "/docs" # FastAPI default health/swagger docs path
    matcher             = "200-299"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

# Listener for Backend (Port 8000)
resource "aws_lb_listener" "backend_listener" {
  load_balancer_arn = aws_lb.campus_alb.arn
  port              = "8000"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.backend_tg.arn
  }
}

# Target Group for Frontend
resource "aws_lb_target_group" "frontend_tg" {
  name        = "campus-frontend-tg"
  port        = 3000
  protocol    = "HTTP"
  vpc_id      = module.vpc.vpc_id
  target_type = "ip"

  health_check {
    path                = "/"
    matcher             = "200-299"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }
}

# Listener for Frontend (Port 3000)
resource "aws_lb_listener" "frontend_listener" {
  load_balancer_arn = aws_lb.campus_alb.arn
  port              = "3000"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.frontend_tg.arn
  }
}

output "api_url" {
  value       = "http://${aws_lb.campus_alb.dns_name}:8000"
  description = "The Base URL for your Backend API"
}

output "website_url" {
  value       = "http://${aws_lb.campus_alb.dns_name}:3000"
  description = "The URL to view your Frontend React/Next.js App"
}
