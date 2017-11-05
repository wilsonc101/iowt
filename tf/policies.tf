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
               "cognito-idp:ListUsers",
               "cognito-idp:AdminResetUserPassword",
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
    actions = ["s3:GetObject",
               "s3:DeleteObject",
               "s3:PutObject"]
    resources = ["arn:aws:s3:::iowt-events/*"]
    effect = "Allow"
  }

  statement {
    sid = "5"
    actions = ["s3:ListBucket",
               "s3:ListObjects"]
    resources = ["arn:aws:s3:::iowt-events"]
    effect = "Allow"
  }


  statement {
    sid = "6"
    actions = ["cognito-idp:AdminListGroupsForUser",
               "cognito-idp:AdminGetUser"]
    resources = ["arn:aws:cognito-idp:*:*:*"]
    effect = "Allow"
  }

  statement {
    sid = "7"
    actions = ["dynamodb:DeleteItem",
               "dynamodb:PutItem",
               "dynamodb:UpdateItem",
               "dynamodb:Scan"]
    resources = ["arn:aws:dynamodb:eu-west-1:*:table/iowt-events"]
    effect = "Allow"
  }

  statement {
    sid = "8"
    actions = ["dynamodb:DeleteItem",
               "dynamodb:PutItem",
               "dynamodb:UpdateItem",
               "dynamodb:Scan"]
    resources = ["arn:aws:dynamodb:eu-west-1:*:table/iowt-devices"]
    effect = "Allow"
  }
}



