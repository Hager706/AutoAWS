variable "bucket_name" {}

variable "env" {}

variable "versioning" {
    type = bool
    default = false
}

variable "tags" {
    type = map(string)
    default = {}
}

