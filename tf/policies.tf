data "aws_iam_policy_document" "iowt-auth-policy-document" {
  statement {
    sid = "1"
    actions = ["logs:CreateLogGroup",
               "logs:CreateLogStream",
               "logs:PutLogEvents"]
    resources = ["arn:aws:logs:*:*:*"]
    effect = "Allow"
  }

  statement {
    sid = "2"
    actions = ["s3:GetObject",
               "s3:PutObject"]
    resources = ["arn:aws:s3:::iowt/*"]
    effect = "Allow"
  }

  statement {
    sid = "3"
    actions = ["cognito-idp:AdminInitiateAuth",
               "cognito-idp:AdminRespondToAuthChallenge",
               "cognito-idp:AdminListGroupsForUser",
               "cognito-idp:AdminGetUser"]
    resources = ["arn:aws:cognito-idp:*:*:*"]
    effect = "Allow"
  }
}

data "aws_iam_policy_document" "iowt-www-policy-document" {
  statement {
    sid = "1"
    actions = ["logs:CreateLogGroup",
               "logs:CreateLogStream",
               "logs:PutLogEvents"]
    resources = ["arn:aws:logs:*:*:*"]
    effect = "Allow"
  }

  statement {
    sid = "2"
    actions = ["s3:GetObject",
               "s3:PutObject"]
    resources = ["arn:aws:s3:::iowt/*"]
    effect = "Allow"
  }

  statement {
    sid = "3"
    actions = ["s3:GetObject",
               "s3:PutObject"]
    resources = ["arn:aws:s3:::iowt-pub/*"]
    effect = "Allow"
  }

  statement {
    sid = "4"
    actions = ["cognito-idp:AdminListGroupsForUser",
               "cognito-idp:AdminGetUser"]
    resources = ["arn:aws:cognito-idp:*:*:*"]
    effect = "Allow"
  }
}



