resource "aws_cloudwatch_log_group" "ecs_logs" {
  name              = "/ecs/campus-app"
  retention_in_days = 7 # Keep logs for 7 days to save costs
}
