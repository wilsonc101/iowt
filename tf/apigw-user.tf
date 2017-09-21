resource "aws_api_gateway_rest_api" "iowt-user-auth" {
  name = "iowt-user-auth"
}


## AUTHFORM
resource "aws_api_gateway_resource" "iowt-user-auth-authform" {
  rest_api_id = "${aws_api_gateway_rest_api.iowt-user-auth.id}"
  parent_id   = "${aws_api_gateway_rest_api.iowt-user-auth.root_resource_id}"
  path_part   = "authform"
}

resource "aws_api_gateway_method" "iowt-user-auth-authform-get" {
  rest_api_id   = "${aws_api_gateway_rest_api.iowt-user-auth.id}"
  resource_id   = "${aws_api_gateway_resource.iowt-user-auth-authform.id}"
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "iowt-user-auth-authform-get" {
  rest_api_id             = "${aws_api_gateway_rest_api.iowt-user-auth.id}"
  resource_id             = "${aws_api_gateway_resource.iowt-user-auth-authform.id}"
  http_method             = "${aws_api_gateway_method.iowt-user-auth-authform-get.http_method}"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/2015-03-31/functions/${aws_lambda_function.iowt-user-auth.arn}/invocations"
}

resource "aws_lambda_permission" "iowt-user-auth-authform-get" {
  statement_id  = "AllowExecutionFromAPIGateway-iowt-user-auth-authform-get"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.iowt-user-auth.arn}"
  principal     = "apigateway.amazonaws.com"
  source_arn = "arn:aws:execute-api:${var.aws_region}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.iowt-user-auth.id}/*/${aws_api_gateway_method.iowt-user-auth-authform-get.http_method}/*"
}

resource "aws_api_gateway_method_response" "iowt-user-auth-authform-get-200" {
  rest_api_id = "${aws_api_gateway_rest_api.iowt-user-auth.id}"
  resource_id = "${aws_api_gateway_resource.iowt-user-auth-authform.id}"
  http_method = "${aws_api_gateway_method.iowt-user-auth-authform-get.http_method}"
  status_code = "200"
  response_models = {
    "text/html" = "Empty"
  }
}


## AUTHIN
resource "aws_api_gateway_resource" "iowt-user-auth-authin" {
  rest_api_id = "${aws_api_gateway_rest_api.iowt-user-auth.id}"
  parent_id   = "${aws_api_gateway_rest_api.iowt-user-auth.root_resource_id}"
  path_part   = "authin"
}

resource "aws_api_gateway_method" "iowt-user-auth-authin-post" {
  rest_api_id   = "${aws_api_gateway_rest_api.iowt-user-auth.id}"
  resource_id   = "${aws_api_gateway_resource.iowt-user-auth-authin.id}"
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "iowt-user-auth-authin-post" {
  rest_api_id             = "${aws_api_gateway_rest_api.iowt-user-auth.id}"
  resource_id             = "${aws_api_gateway_resource.iowt-user-auth-authin.id}"
  http_method             = "${aws_api_gateway_method.iowt-user-auth-authin-post.http_method}"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/2015-03-31/functions/${aws_lambda_function.iowt-user-auth.arn}/invocations"
}

resource "aws_lambda_permission" "iowt-user-auth-authin-post" {
  statement_id  = "AllowExecutionFromAPIGateway-iowt-user-auth-authin-post"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.iowt-user-auth.arn}"
  principal     = "apigateway.amazonaws.com"
  source_arn = "arn:aws:execute-api:${var.aws_region}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.iowt-user-auth.id}/*/${aws_api_gateway_method.iowt-user-auth-authin-post.http_method}/*"
}

resource "aws_api_gateway_method_response" "iowt-user-auth-authin-post-200" {
  rest_api_id = "${aws_api_gateway_rest_api.iowt-user-auth.id}"
  resource_id = "${aws_api_gateway_resource.iowt-user-auth-authin.id}"
  http_method = "${aws_api_gateway_method.iowt-user-auth-authin-post.http_method}"
  status_code = "200"
  response_models = {
    "text/html" = "Empty"
  }
}


## NEWPASS
resource "aws_api_gateway_resource" "iowt-user-auth-newpass" {
  rest_api_id = "${aws_api_gateway_rest_api.iowt-user-auth.id}"
  parent_id   = "${aws_api_gateway_rest_api.iowt-user-auth.root_resource_id}"
  path_part   = "newpass"
}

resource "aws_api_gateway_method" "iowt-user-auth-newpass-post" {
  rest_api_id   = "${aws_api_gateway_rest_api.iowt-user-auth.id}"
  resource_id   = "${aws_api_gateway_resource.iowt-user-auth-newpass.id}"
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "iowt-user-auth-newpass-post" {
  rest_api_id             = "${aws_api_gateway_rest_api.iowt-user-auth.id}"
  resource_id             = "${aws_api_gateway_resource.iowt-user-auth-newpass.id}"
  http_method             = "${aws_api_gateway_method.iowt-user-auth-newpass-post.http_method}"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/2015-03-31/functions/${aws_lambda_function.iowt-user-auth.arn}/invocations"
}

resource "aws_lambda_permission" "iowt-user-auth-newpass-post" {
  statement_id  = "AllowExecutionFromAPIGateway-iowt-user-auth-newpass-post"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.iowt-user-auth.arn}"
  principal     = "apigateway.amazonaws.com"
  source_arn = "arn:aws:execute-api:${var.aws_region}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.iowt-user-auth.id}/*/${aws_api_gateway_method.iowt-user-auth-newpass-post.http_method}/*"
}

resource "aws_api_gateway_method_response" "iowt-user-auth-newpass-post-200" {
  rest_api_id = "${aws_api_gateway_rest_api.iowt-user-auth.id}"
  resource_id = "${aws_api_gateway_resource.iowt-user-auth-newpass.id}"
  http_method = "${aws_api_gateway_method.iowt-user-auth-newpass-post.http_method}"
  status_code = "200"
  response_models = {
    "text/html" = "Empty"
  }
}


## READ
resource "aws_api_gateway_resource" "iowt-user-auth-read" {
  rest_api_id = "${aws_api_gateway_rest_api.iowt-user-auth.id}"
  parent_id   = "${aws_api_gateway_rest_api.iowt-user-auth.root_resource_id}"
  path_part   = "read"
}

resource "aws_api_gateway_method" "iowt-user-auth-read-get" {
  rest_api_id   = "${aws_api_gateway_rest_api.iowt-user-auth.id}"
  resource_id   = "${aws_api_gateway_resource.iowt-user-auth-read.id}"
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "iowt-user-auth-read-get-integration" {
  rest_api_id             = "${aws_api_gateway_rest_api.iowt-user-auth.id}"
  resource_id             = "${aws_api_gateway_resource.iowt-user-auth-read.id}"
  http_method             = "${aws_api_gateway_method.iowt-user-auth-read-get.http_method}"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/2015-03-31/functions/${aws_lambda_function.iowt-user-auth.arn}/invocations"
}

resource "aws_lambda_permission" "iowt-user-auth-read-get" {
  statement_id  = "AllowExecutionFromAPIGateway-iowt-user-auth-read-get"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.iowt-user-auth.arn}"
  principal     = "apigateway.amazonaws.com"
  source_arn = "arn:aws:execute-api:${var.aws_region}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.iowt-user-auth.id}/*/${aws_api_gateway_method.iowt-user-auth-read-get.http_method}/*"
}

resource "aws_api_gateway_method_response" "iowt-user-auth-read-get-200" {
  rest_api_id = "${aws_api_gateway_rest_api.iowt-user-auth.id}"
  resource_id = "${aws_api_gateway_resource.iowt-user-auth-read.id}"
  http_method = "${aws_api_gateway_method.iowt-user-auth-read-get.http_method}"
  status_code = "200"
  response_models = {
    "text/html" = "Empty"
  }
}


## RESETPASS
resource "aws_api_gateway_resource" "iowt-user-auth-resetpass" {
  rest_api_id = "${aws_api_gateway_rest_api.iowt-user-auth.id}"
  parent_id   = "${aws_api_gateway_rest_api.iowt-user-auth.root_resource_id}"
  path_part   = "resetpass"
}

resource "aws_api_gateway_method" "iowt-user-auth-resetpass-post" {
  rest_api_id   = "${aws_api_gateway_rest_api.iowt-user-auth.id}"
  resource_id   = "${aws_api_gateway_resource.iowt-user-auth-resetpass.id}"
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "iowt-user-auth-resetpass-post" {
  rest_api_id             = "${aws_api_gateway_rest_api.iowt-user-auth.id}"
  resource_id             = "${aws_api_gateway_resource.iowt-user-auth-resetpass.id}"
  http_method             = "${aws_api_gateway_method.iowt-user-auth-resetpass-post.http_method}"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/2015-03-31/functions/${aws_lambda_function.iowt-user-auth.arn}/invocations"
}

resource "aws_lambda_permission" "iowt-user-auth-resetpass-post" {
  statement_id  = "AllowExecutionFromAPIGateway-iowt-user-auth-resetpass-post"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.iowt-user-auth.arn}"
  principal     = "apigateway.amazonaws.com"
  source_arn = "arn:aws:execute-api:${var.aws_region}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.iowt-user-auth.id}/*/${aws_api_gateway_method.iowt-user-auth-resetpass-post.http_method}/*"
}

resource "aws_api_gateway_method_response" "iowt-user-auth-resetpass-post-200" {
  rest_api_id = "${aws_api_gateway_rest_api.iowt-user-auth.id}"
  resource_id = "${aws_api_gateway_resource.iowt-user-auth-resetpass.id}"
  http_method = "${aws_api_gateway_method.iowt-user-auth-resetpass-post.http_method}"
  status_code = "200"
  response_models = {
    "text/html" = "Empty"
  }
}


# Deployment
resource "aws_api_gateway_deployment" "iowt-user-auth-dev" {
  depends_on = ["aws_api_gateway_method.iowt-user-auth-authform-get",
                "aws_api_gateway_method.iowt-user-auth-authin-post",
                "aws_api_gateway_method.iowt-user-auth-newpass-post",
                "aws_api_gateway_method.iowt-user-auth-read-get",
                "aws_api_gateway_method.iowt-user-auth-resetpass-post"]
  rest_api_id = "${aws_api_gateway_rest_api.iowt-user-auth.id}"
  stage_name  = "dev"
}
