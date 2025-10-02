variable "create" {
    type = bool 
    default = false 
}

variable "name" {

}

variable "secret_data" {
    type = map(string)
    default = {} 
}
