variable "cognito_app_id" {}
variable "cognito_pool_id" {}


resource "aws_lambda_function" "iowt-user-auth" {
  filename         = "build_files/iowt-auth.zip"
  function_name    = "iowt-user-auth"
  role             = "${aws_iam_role.iowt-auth-role.arn}"
  handler          = "app.app"
  runtime          = "python2.7"
  source_code_hash = "${base64sha256(file("build_files/iowt-auth.zip"))}"

  environment {
    variables = {
      cogadmgrp = "admin"
      pubbucketurl = "https://s3-eu-west-1.amazonaws.com/iowt-pub/"
      s3bucket = "iowt"
      domain = "iowt.robotika.co.uk"
      cogpoolid = "${var.cognito_pool_id}"
      cogappid = "${var.cognito_app_id}"
      cogattrib = "attrib1"
      logopath = "Things"      
    }
  }

}

resource "aws_lambda_function" "iowt-api-auth" {
  filename         = "build_files/iowt-auth.zip"
  function_name    = "iowt-api-auth"
  role             = "${aws_iam_role.iowt-auth-role.arn}"
  handler          = "app.app"
  runtime          = "python2.7"
  source_code_hash = "${base64sha256(file("build_files/iowt-auth.zip"))}"

  environment {
    variables = {
      cogadmgrp = "admin"
      pubbucketurl = "https://s3-eu-west-1.amazonaws.com/iowt-pub/"
      s3bucket = "iowt"
      domain = "iowt.robotika.co.uk"
      cogpoolid = "${var.cognito_pool_id}"
      cogappid = "${var.cognito_app_id}"
      cogattrib = "attrib1"
      logopath = "Things"      
    }
  }

}


resource "aws_lambda_function" "iowt-www" {
  filename         = "build_files/iowt-www.zip"
  function_name    = "iowt-www"
  role             = "${aws_iam_role.iowt-www-role.arn}"
  handler          = "app.app"
  runtime          = "python3.6"
  source_code_hash = "${base64sha256(file("build_files/iowt-www.zip"))}"
  timeout          = "20"
  environment {
    variables = {
      bucket = "iowt",
      pubbucketurl = "https://s3-eu-west-1.amazonaws.com/iowt-pub/",
      loginurl = "https://api.iowt.robotika.co.uk/token/validatetoken",
      useractionurl = "https://api.iowt.robotika.co.uk/token/useraction",
      adminactionurl = "https://api.iowt.robotika.co.uk/token/useradmin",
      event_bucket = "iowt-events",
      iowt_events_table = "iowt-events"
      iowt_device_table = "iowt-devices"
      logopath = "Things"      
      iowt_api = "https://iowt.robotika.co.uk/www"
      sightings_image_url = "https://iowt.robotika.co.uk/www/image"
    }
  }

}


