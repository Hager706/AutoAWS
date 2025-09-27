output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "vpc_cidr_block" {
  description = "CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}

output "internet_gateway_id" {
  description = "ID of the Internet Gateway"
  value       = length(aws_internet_gateway.main) > 0 ? aws_internet_gateway.main[0].id : null
}

output "public_subnet_ids" {
  description = "List of IDs of public subnets"
  value       = values(aws_subnet.public)[*].id
}

output "private_subnet_ids" {
  description = "List of IDs of private subnets"
  value       = values(aws_subnet.private)[*].id
}

output "public_subnets" {
  description = "Map of public subnet names to subnet objects"
  value       = aws_subnet.public
}

output "private_subnets" {
  description = "Map of private subnet names to subnet objects"
  value       = aws_subnet.private
}