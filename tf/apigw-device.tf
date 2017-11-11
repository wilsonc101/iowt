resource "aws_api_gateway_rest_api" "iowt-device-auth" {
  name = "iowt-device-auth"
}


## DEVICEAUTH
resource "aws_api_gateway_resource" "iowt-device-auth-deviceauth" {
  rest_api_id = "${aws_api_gateway_rest_api.iowt-device-auth.id}"
  parent_id   = "${aws_api_gateway_rest_api.iowt-device-auth.root_resource_id}"
  path_part   = "deviceauth"
}

resource "aws_api_gateway_method" "iowt-device-auth-deviceauth-post" {
  rest_api_id   = "${aws_api_gateway_rest_api.iowt-device-auth.id}"
  resource_id   = "${aws_api_gateway_resource.iowt-device-auth-deviceauth.id}"
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "iowt-device-auth-deviceauth-post" {
  rest_api_id             = "${aws_api_gateway_rest_api.iowt-device-auth.id}"
  resource_id             = "${aws_api_gateway_resource.iowt-device-auth-deviceauth.id}"
  http_method             = "${aws_api_gateway_method.iowt-device-auth-deviceauth-post.http_method}"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/2015-03-31/functions/${aws_lambda_function.iowt-device-auth.arn}/invocations"
}

resource "aws_lambda_permission" "iowt-device-auth-deviceauth-post" {
  statement_id  = "AllowExecutionFromAPIGateway-iowt-device-auth-deviceauth-post"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.iowt-device-auth.arn}"
  principal     = "apigateway.amazonaws.com"
  source_arn = "arn:aws:execute-api:${var.aws_region}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.iowt-device-auth.id}/*/${aws_api_gateway_method.iowt-device-auth-deviceauth-post.http_method}/*"
}

resource "aws_api_gateway_method_response" "iowt-device-auth-deviceauth-post-200" {
  rest_api_id = "${aws_api_gateway_rest_api.iowt-device-auth.id}"
  resource_id = "${aws_api_gateway_resource.iowt-device-auth-deviceauth.id}"
  http_method = "${aws_api_gateway_method.iowt-device-auth-deviceauth-post.http_method}"
  status_code = "200"
  response_models = {
    "text/html" = "Empty"
  }
}

# Deployment
resource "aws_api_gateway_deployment" "iowt-device-auth-dev" {
  depends_on = ["aws_api_gateway_method.iowt-device-auth-deviceauth-post"]
  rest_api_id = "${aws_api_gateway_rest_api.iowt-device-auth.id}"
  stage_name  = "dev"
}


