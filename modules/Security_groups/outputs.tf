output "security_group_ids" {
  description = "Map of security group names to their IDs"
  value = {
    for name, sg in aws_security_group.groups : name => sg.id
  }
}

output "security_groups" {
  description = "Map of security group names to security group objects"
  value       = aws_security_group.groups
}

output "security_group_arns" {
  description = "Map of security group names to their ARNs"
  value = {
    for name, sg in aws_security_group.groups : name => sg.arn
  }
}