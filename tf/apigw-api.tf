resource "aws_api_gateway_rest_api" "iowt-api-auth" {
  name = "iowt-api-auth"
}


## VALIDATETOKEN
resource "aws_api_gateway_resource" "iowt-api-auth-validatetoken" {
  rest_api_id = "${aws_api_gateway_rest_api.iowt-api-auth.id}"
  parent_id   = "${aws_api_gateway_rest_api.iowt-api-auth.root_resource_id}"
  path_part   = "validatetoken"
}

resource "aws_api_gateway_method" "iowt-api-auth-validatetoken-post" {
  rest_api_id   = "${aws_api_gateway_rest_api.iowt-api-auth.id}"
  resource_id   = "${aws_api_gateway_resource.iowt-api-auth-validatetoken.id}"
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "iowt-api-auth-validatetoken-post" {
  rest_api_id             = "${aws_api_gateway_rest_api.iowt-api-auth.id}"
  resource_id             = "${aws_api_gateway_resource.iowt-api-auth-validatetoken.id}"
  http_method             = "${aws_api_gateway_method.iowt-api-auth-validatetoken-post.http_method}"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/2015-03-31/functions/${aws_lambda_function.iowt-api-auth.arn}/invocations"
}

resource "aws_lambda_permission" "iowt-api-auth-validatetoken-post" {
  statement_id  = "AllowExecutionFromAPIGateway-iowt-api-auth-validatetoken-post"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.iowt-api-auth.arn}"
  principal     = "apigateway.amazonaws.com"
  source_arn = "arn:aws:execute-api:${var.aws_region}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.iowt-api-auth.id}/*/${aws_api_gateway_method.iowt-api-auth-validatetoken-post.http_method}/*"
}

resource "aws_api_gateway_method_response" "iowt-api-auth-validatetoken-post-200" {
  rest_api_id   = "${aws_api_gateway_rest_api.iowt-api-auth.id}"
  resource_id   = "${aws_api_gateway_resource.iowt-api-auth-validatetoken.id}"
  http_method   = "${aws_api_gateway_method.iowt-api-auth-validatetoken-post.http_method}"
  status_code = "200"
  response_models = {
    "text/html" = "Empty"
  }
}


## USERACTION
resource "aws_api_gateway_resource" "iowt-api-auth-useraction" {
  rest_api_id = "${aws_api_gateway_rest_api.iowt-api-auth.id}"
  parent_id   = "${aws_api_gateway_rest_api.iowt-api-auth.root_resource_id}"
  path_part   = "useraction"
}

resource "aws_api_gateway_method" "iowt-api-auth-useraction-post" {
  rest_api_id   = "${aws_api_gateway_rest_api.iowt-api-auth.id}"
  resource_id   = "${aws_api_gateway_resource.iowt-api-auth-useraction.id}"
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "iowt-api-auth-useraction-post" {
  rest_api_id             = "${aws_api_gateway_rest_api.iowt-api-auth.id}"
  resource_id             = "${aws_api_gateway_resource.iowt-api-auth-useraction.id}"
  http_method             = "${aws_api_gateway_method.iowt-api-auth-useraction-post.http_method}"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/2015-03-31/functions/${aws_lambda_function.iowt-api-auth.arn}/invocations"
}

resource "aws_lambda_permission" "iowt-api-auth-useraction-post" {
  statement_id  = "AllowExecutionFromAPIGateway-iowt-api-auth-useraction-post"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.iowt-api-auth.arn}"
  principal     = "apigateway.amazonaws.com"
  source_arn = "arn:aws:execute-api:${var.aws_region}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.iowt-api-auth.id}/*/${aws_api_gateway_method.iowt-api-auth-useraction-post.http_method}/*"
}

resource "aws_api_gateway_method_response" "iowt-api-auth-useraction-post-200" {
  rest_api_id   = "${aws_api_gateway_rest_api.iowt-api-auth.id}"
  resource_id   = "${aws_api_gateway_resource.iowt-api-auth-useraction.id}"
  http_method   = "${aws_api_gateway_method.iowt-api-auth-useraction-post.http_method}"
  status_code = "200"
  response_models = {
    "text/html" = "Empty"
  }
}


# Deployment
resource "aws_api_gateway_deployment" "iowt-api-auth-dev" {
  depends_on = ["aws_api_gateway_method.iowt-api-auth-validatetoken-post", "aws_api_gateway_method.iowt-api-auth-useraction-post"]
  rest_api_id = "${aws_api_gateway_rest_api.iowt-api-auth.id}"
  stage_name  = "dev"
}


