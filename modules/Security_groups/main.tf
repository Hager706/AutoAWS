resource "aws_security_group" "groups" {
  for_each = {
    for sg in var.security_groups : sg.name => sg
  }

  name        = "${var.project_name}-${var.environment}-${each.value.name}"
  description = each.value.description
  vpc_id      = var.vpc_id

  tags = merge(var.tags, {
    Name = "${var.project_name}-${var.environment}-${each.value.name}"
  })
}

# Create Ingress Rules
resource "aws_vpc_security_group_ingress_rule" "ingress" {
  for_each = {
    for rule in flatten([
      for sg_key, sg in var.security_groups : [
        for idx, rule in sg.ingress_rules : {
          sg_key      = sg.name
          rule_key    = "${sg.name}-ingress-${idx}"
          from_port   = rule.from_port
          to_port     = rule.to_port
          ip_protocol = rule.protocol
          cidr_ipv4   = length(rule.cidr_blocks) > 0 ? rule.cidr_blocks[0] : null
          description = rule.description
        }
      ]
    ]) : rule.rule_key => rule
  }

  security_group_id = aws_security_group.groups[each.value.sg_key].id
  from_port         = each.value.from_port
  to_port           = each.value.to_port
  ip_protocol       = each.value.ip_protocol
  cidr_ipv4         = each.value.cidr_ipv4
  description       = each.value.description
}

# Create Egress Rules (default allow all if not specified)
resource "aws_vpc_security_group_egress_rule" "egress" {
  for_each = {
    for rule in flatten([
      for sg_key, sg in var.security_groups : 
      length(sg.egress_rules) > 0 ? [
        for idx, rule in sg.egress_rules : {
          sg_key      = sg.name
          rule_key    = "${sg.name}-egress-${idx}"
          from_port   = rule.from_port
          to_port     = rule.to_port
          ip_protocol = rule.protocol
          cidr_ipv4   = length(rule.cidr_blocks) > 0 ? rule.cidr_blocks[0] : null
          description = rule.description
        }
      ] : [
        # Default allow all outbound if no egress rules specified
        {
          sg_key      = sg.name
          rule_key    = "${sg.name}-egress-default"
          from_port   = -1
          to_port     = -1
          ip_protocol = "-1"
          cidr_ipv4   = "0.0.0.0/0"
          description = "Default allow all outbound"
        }
      ]
    ]) : rule.rule_key => rule
  }

  security_group_id = aws_security_group.groups[each.value.sg_key].id
  from_port         = each.value.from_port
  to_port           = each.value.to_port
  ip_protocol       = each.value.ip_protocol
  cidr_ipv4         = each.value.cidr_ipv4
  description       = each.value.description
}
