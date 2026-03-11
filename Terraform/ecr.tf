# The Backend Warehouse
resource "aws_ecr_repository" "backend" {
  name                 = "campus-backend"
  image_tag_mutability = "MUTABLE"
  force_delete         = true # Helpful for student projects
}

# The Frontend Warehouse
resource "aws_ecr_repository" "frontend" {
  name                 = "campus-frontend"
  image_tag_mutability = "MUTABLE"
  force_delete         = true
}

# Outputs so you can copy the URLs for your terminal
output "backend_url" {
  value = aws_ecr_repository.backend.repository_url
}

output "frontend_url" {
  value = aws_ecr_repository.frontend.repository_url
}
