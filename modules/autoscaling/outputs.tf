output "asg_name" {
  value = aws_autoscaling_group.this.name
}

variable "target_group_arn" {
  description = "ARN of the ALB target group to attach (optional)"
  type        = string
  default     = ""
}
