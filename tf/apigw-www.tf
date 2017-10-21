resource "aws_api_gateway_rest_api" "iowt-www" {
  name = "iowt-www"
}

## ROOT_GET
resource "aws_api_gateway_method" "iowt-www-root-get" {
  rest_api_id   = "${aws_api_gateway_rest_api.iowt-www.id}"
  resource_id   = "${aws_api_gateway_rest_api.iowt-www.root_resource_id}"
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "iowt-www-root-get" {
  rest_api_id             = "${aws_api_gateway_rest_api.iowt-www.id}"
  resource_id             = "${aws_api_gateway_rest_api.iowt-www.root_resource_id}"
  http_method             = "${aws_api_gateway_method.iowt-www-root-get.http_method}"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/2015-03-31/functions/${aws_lambda_function.iowt-www.arn}/invocations"
}

resource "aws_lambda_permission" "apigw-lambda-iowt-www-get" {
  statement_id  = "AllowExecutionFromAPIGateway-iowt-www-get"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.iowt-www.arn}"
  principal     = "apigateway.amazonaws.com"
  source_arn = "arn:aws:execute-api:${var.aws_region}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.iowt-www.id}/*/${aws_api_gateway_method.iowt-www-root-get.http_method}/*"
}

resource "aws_api_gateway_method_response" "iowt-www-get-200" {
  rest_api_id = "${aws_api_gateway_rest_api.iowt-www.id}"
  resource_id = "${aws_api_gateway_rest_api.iowt-www.root_resource_id}"
  http_method = "${aws_api_gateway_method.iowt-www-root-get.http_method}"
  status_code = "200"
  response_models = {
    "text/html" = "Empty"
  }
}


## NEWEVENT
resource "aws_api_gateway_resource" "iowt-www-newevent" {
  rest_api_id = "${aws_api_gateway_rest_api.iowt-www.id}"
  parent_id   = "${aws_api_gateway_rest_api.iowt-www.root_resource_id}"
  path_part   = "newevent"
}

resource "aws_api_gateway_method" "iowt-www-newevent-post" {
  rest_api_id   = "${aws_api_gateway_rest_api.iowt-www.id}"
  resource_id   = "${aws_api_gateway_resource.iowt-www-newevent.id}"
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "iowt-www-newevent-post" {
  rest_api_id             = "${aws_api_gateway_rest_api.iowt-www.id}"
  resource_id             = "${aws_api_gateway_resource.iowt-www-newevent.id}"
  http_method             = "${aws_api_gateway_method.iowt-www-newevent-post.http_method}"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/2015-03-31/functions/${aws_lambda_function.iowt-www.arn}/invocations"
}

resource "aws_lambda_permission" "iowt-www-newevent-post" {
  statement_id  = "AllowExecutionFromAPIGateway-iowt-www-newevent-post"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.iowt-www.arn}"
  principal     = "apigateway.amazonaws.com"
  source_arn = "arn:aws:execute-api:${var.aws_region}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.iowt-www.id}/*/${aws_api_gateway_method.iowt-www-newevent-post.http_method}/*"
}

resource "aws_api_gateway_method_response" "iowt-www-newevent-post-200" {
  rest_api_id   = "${aws_api_gateway_rest_api.iowt-www.id}"
  resource_id   = "${aws_api_gateway_resource.iowt-www-newevent.id}"
  http_method   = "${aws_api_gateway_method.iowt-www-newevent-post.http_method}"
  status_code = "200"
  response_models = {
    "text/html" = "Empty"
  }
}


## PAGES
resource "aws_api_gateway_resource" "iowt-www-pages" {
  rest_api_id = "${aws_api_gateway_rest_api.iowt-www.id}"
  parent_id   = "${aws_api_gateway_rest_api.iowt-www.root_resource_id}"
  path_part   = "{pages}"
}

resource "aws_api_gateway_method" "iowt-www-pages-get" {
  rest_api_id   = "${aws_api_gateway_rest_api.iowt-www.id}"
  resource_id   = "${aws_api_gateway_resource.iowt-www-pages.id}"
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "iowt-www-pages-post" {
  rest_api_id   = "${aws_api_gateway_rest_api.iowt-www.id}"
  resource_id   = "${aws_api_gateway_resource.iowt-www-pages.id}"
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "iowt-www-pages-get" {
  rest_api_id             = "${aws_api_gateway_rest_api.iowt-www.id}"
  resource_id             = "${aws_api_gateway_resource.iowt-www-pages.id}"
  http_method             = "${aws_api_gateway_method.iowt-www-pages-get.http_method}"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/2015-03-31/functions/${aws_lambda_function.iowt-www.arn}/invocations"
}

resource "aws_api_gateway_integration" "iowt-www-pages-post" {
  rest_api_id             = "${aws_api_gateway_rest_api.iowt-www.id}"
  resource_id             = "${aws_api_gateway_resource.iowt-www-pages.id}"
  http_method             = "${aws_api_gateway_method.iowt-www-pages-post.http_method}"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/2015-03-31/functions/${aws_lambda_function.iowt-www.arn}/invocations"
}

resource "aws_lambda_permission" "iowt-www-pages-get" {
  statement_id  = "AllowExecutionFromAPIGateway-iowt-www-pages-get"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.iowt-www.arn}"
  principal     = "apigateway.amazonaws.com"
  source_arn = "arn:aws:execute-api:${var.aws_region}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.iowt-www.id}/*/${aws_api_gateway_method.iowt-www-pages-get.http_method}/*"
}

resource "aws_lambda_permission" "iowt-www-pages-post" {
  statement_id  = "AllowExecutionFromAPIGateway-iowt-www-pages-post"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.iowt-www.arn}"
  principal     = "apigateway.amazonaws.com"
  source_arn = "arn:aws:execute-api:${var.aws_region}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.iowt-www.id}/*/${aws_api_gateway_method.iowt-www-pages-post.http_method}/*"
}

resource "aws_api_gateway_method_response" "iowt-www-pages-get-200" {
  rest_api_id   = "${aws_api_gateway_rest_api.iowt-www.id}"
  resource_id   = "${aws_api_gateway_resource.iowt-www-pages.id}"
  http_method   = "${aws_api_gateway_method.iowt-www-pages-post.http_method}"
  status_code = "200"
  response_models = {
    "text/html" = "Empty"
  }
}

# Deployment
resource "aws_api_gateway_deployment" "iowt-www-dev" {
  depends_on = ["aws_api_gateway_method.iowt-www-newevent-post", "aws_api_gateway_method.iowt-www-pages-get", "aws_api_gateway_method.iowt-www-pages-post"]

#"aws_api_gateway_method.iowt-www-root-get",
  rest_api_id = "${aws_api_gateway_rest_api.iowt-www.id}"
  stage_name  = "dev"
}

