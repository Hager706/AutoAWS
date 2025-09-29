variable "name" {}

variable "ami" {}

variable "instance_type" {}

variable "instance_profile_name" {}

variable "app_sg_id" {}

variable "subnet_ids" {
     type = list(string)
}

variable "min_size" {
    type = number
    default = 1
}

variable "max_size" {
    type = number
    default = 1
}

variable "user_data" {
    type = string
    default = ""
}

variable "target_group_arn" {
    type = string
    default = ""
}



# feat(autoscaling): add AutoScaling group with Nginx user_data
