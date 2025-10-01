variable "name" {}
variable "engine" {}
variable "engine_version" { default = null }
variable "instance_class" {}
variable "db_name" { default = null }
variable "username" { default = null }
variable "password" { default = null }
variable "db_sg_id" {}

variable "allocated_storage" {
    type = number
    default = 20 
}

variable "subnet_ids" {
    type = list(string) 
}

variable "create" {
    type = bool
    default = false
}
