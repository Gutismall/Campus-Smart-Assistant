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

variable "admin_email" {
  type      = string
  sensitive = true
}

variable "admin_password" {
  type      = string
  sensitive = true
}

variable "gemini_api_key" {
  type      = string
  sensitive = true
}

variable "jwt_secret" {
  type      = string
  sensitive = true
}

variable "text_to_sql_schema_context" {
  type      = string
}
