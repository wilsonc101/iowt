resource "aws_api_gateway_rest_api" "iowt-www" {
  name = "iowt-www"
}

resource "aws_api_gateway_method" "iowt-www-method-root-get" {
  rest_api_id   = "${aws_api_gateway_rest_api.iowt-www.id}"
  resource_id   = "${aws_api_gateway_rest_api.iowt-www.root_resource_id}"
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "iowt-www-method-root-post" {
  rest_api_id   = "${aws_api_gateway_rest_api.iowt-www.id}"
  resource_id   = "${aws_api_gateway_rest_api.iowt-www.root_resource_id}"
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "iowt-www-integration-get" {
  rest_api_id             = "${aws_api_gateway_rest_api.iowt-www.id}"
  resource_id             = "${aws_api_gateway_rest_api.iowt-www.root_resource_id}"
  http_method             = "${aws_api_gateway_method.iowt-www-method-root-get.http_method}"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/2015-03-31/functions/${aws_lambda_function.iowt-www.arn}/invocations"
}

resource "aws_api_gateway_integration" "iowt-www-integration-post" {
  rest_api_id             = "${aws_api_gateway_rest_api.iowt-www.id}"
  resource_id             = "${aws_api_gateway_rest_api.iowt-www.root_resource_id}"
  http_method             = "${aws_api_gateway_method.iowt-www-method-root-post.http_method}"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/2015-03-31/functions/${aws_lambda_function.iowt-www.arn}/invocations"
}

resource "aws_lambda_permission" "apigw-lambda-iowt-www-get" {
  statement_id  = "AllowExecutionFromAPIGateway-iowt-www-get"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.iowt-www.arn}"
  principal     = "apigateway.amazonaws.com"
  source_arn = "arn:aws:execute-api:${var.aws_region}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.iowt-www.id}/*/${aws_api_gateway_method.iowt-www-method-root-get.http_method}/*"
}

resource "aws_lambda_permission" "apigw-lambda-iowt-www-post" {
  statement_id  = "AllowExecutionFromAPIGateway-iowt-www-post"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.iowt-www.arn}"
  principal     = "apigateway.amazonaws.com"
  source_arn = "arn:aws:execute-api:${var.aws_region}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.iowt-www.id}/*/${aws_api_gateway_method.iowt-www-method-root-post.http_method}/*"
}

resource "aws_api_gateway_method_response" "iowt-www-get-200" {
  rest_api_id = "${aws_api_gateway_rest_api.iowt-www.id}"
  resource_id = "${aws_api_gateway_rest_api.iowt-www.root_resource_id}"
  http_method = "${aws_api_gateway_method.iowt-www-method-root-get.http_method}"
  status_code = "200"
  response_models = {
    "text/html" = "Empty"
  }
}

resource "aws_api_gateway_method_response" "iowt-www-post-200" {
  rest_api_id = "${aws_api_gateway_rest_api.iowt-www.id}"
  resource_id = "${aws_api_gateway_rest_api.iowt-www.root_resource_id}"
  http_method = "${aws_api_gateway_method.iowt-www-method-root-post.http_method}"
  status_code = "200"
  response_models = {
    "text/html" = "Empty"
  }
}

resource "aws_api_gateway_deployment" "iowt-www-dev" {
  depends_on = ["aws_api_gateway_method.iowt-www-method-root-get",
                "aws_api_gateway_method.iowt-www-method-root-post"]
  rest_api_id = "${aws_api_gateway_rest_api.iowt-www.id}"
  stage_name  = "dev"
}

