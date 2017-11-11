resource "aws_iam_role_policy" "iowt-auth-policy" {
  name = "iowt-auth-policy"
  role = "${aws_iam_role.iowt-auth-role.id}"
  policy = "${data.aws_iam_policy_document.iowt-auth-policy-document.json}"
}


resource "aws_iam_role" "iowt-auth-role" {
  name = "iowt-auth-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "iowt-www-policy" {
  name = "iowt-www-policy"
  role = "${aws_iam_role.iowt-www-role.id}"
  policy = "${data.aws_iam_policy_document.iowt-www-policy-document.json}"
}


resource "aws_iam_role" "iowt-www-role" {
  name = "iowt-www-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "iowt-device-auth-policy" {
  name = "iowt-device-auth-policy"
  role = "${aws_iam_role.iowt-device-auth-role.id}"
  policy = "${data.aws_iam_policy_document.iowt-device-auth-policy-document.json}"
}

resource "aws_iam_role" "iowt-device-auth-role" {
  name = "iowt-device-auth-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}
