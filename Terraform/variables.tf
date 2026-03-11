variable "db_password" {
  type      = string
  sensitive = true # This stops the password from printing in your terminal logs
}

variable "db_name" {
  type        = string
  description = "The name of the database"
}

variable "db_username" {
  type        = string
  description = "The username for the database administrator"
}
