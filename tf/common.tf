variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "aws_region" {}

provider "aws" {
    access_key = "${var.aws_access_key}"
    secret_key = "${var.aws_secret_key}"
    region ="${var.aws_region}"
}

provider "aws" {
    access_key = "${var.aws_access_key}"
    secret_key = "${var.aws_secret_key}"
    region = "us-east-1"
    alias = "us-west-1"
}

# Data Sources
data "aws_caller_identity" "current" {}
data "aws_canonical_user_id" "current" {}
 
data "aws_iam_role" "iowt_www_role" {
  name = "iowt-www-role"
}

