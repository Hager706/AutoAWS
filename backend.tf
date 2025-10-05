terraform {
  backend "s3" {
    bucket         = "autoaws-terraform-state"
    key            = "autoaws/terraform.tfstate"
    region         = "eu-central-1"
    dynamodb_table = "tf-locks"
    encrypt        = true
  }
}