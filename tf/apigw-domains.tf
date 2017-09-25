## ROBOTIKA
data "aws_route53_zone" "robotika" {
  name = "robotika.co.uk"
}

## IOWT.ROBOTIKA
data "aws_acm_certificate" "robotika-iowt" {
  provider = "aws.us-west-1"
  domain   = "iowt.robotika.co.uk"
  statuses = ["ISSUED"]
}


resource "aws_api_gateway_domain_name" "robotika-iowt" {
  domain_name = "iowt.robotika.co.uk"
  certificate_arn = "${data.aws_acm_certificate.robotika-iowt.arn}"
}

resource "aws_route53_record" "robotika-iowt" {
  zone_id = "${data.aws_route53_zone.robotika.zone_id}"
  name = "${aws_api_gateway_domain_name.robotika-iowt.domain_name}"
  type = "A"

  alias {
    name                   = "${aws_api_gateway_domain_name.robotika-iowt.cloudfront_domain_name}"
    zone_id                = "${aws_api_gateway_domain_name.robotika-iowt.cloudfront_zone_id}"
    evaluate_target_health = false
  }
}

resource "aws_api_gateway_base_path_mapping" "robotika-iowt-www" {
  api_id      = "${aws_api_gateway_rest_api.iowt-www.id}"
  stage_name  = "${aws_api_gateway_deployment.iowt-www-dev.stage_name}"
  domain_name = "${aws_api_gateway_domain_name.robotika-iowt.domain_name}"
  base_path   = "www"
}

resource "aws_api_gateway_base_path_mapping" "robotika-iowt-login" {
  api_id      = "${aws_api_gateway_rest_api.iowt-user-auth.id}"
  stage_name  = "${aws_api_gateway_deployment.iowt-user-auth-dev.stage_name}"
  domain_name = "${aws_api_gateway_domain_name.robotika-iowt.domain_name}"
  base_path   = "login"
}



## API.IOWT.ROBOTIKA
data "aws_acm_certificate" "robotika-iowt-api" {
  provider = "aws.us-west-1"
  domain   = "api.iowt.robotika.co.uk"
  statuses = ["ISSUED"]
}

resource "aws_api_gateway_domain_name" "robotika-iowt-api" {
  domain_name = "api.iowt.robotika.co.uk"
  certificate_arn = "${data.aws_acm_certificate.robotika-iowt-api.arn}"
}

resource "aws_route53_record" "robotika-iowt-api" {
  zone_id = "${data.aws_route53_zone.robotika.zone_id}"
  name = "${aws_api_gateway_domain_name.robotika-iowt-api.domain_name}"
  type = "A"

  alias {
    name                   = "${aws_api_gateway_domain_name.robotika-iowt-api.cloudfront_domain_name}"
    zone_id                = "${aws_api_gateway_domain_name.robotika-iowt-api.cloudfront_zone_id}"
    evaluate_target_health = false
  }
}

resource "aws_api_gateway_base_path_mapping" "robotika-iowt-api" {
  api_id      = "${aws_api_gateway_rest_api.iowt-api-auth.id}"
  stage_name  = "${aws_api_gateway_deployment.iowt-api-auth-dev.stage_name}"
  domain_name = "${aws_api_gateway_domain_name.robotika-iowt-api.domain_name}"
  base_path = "token"
}

resource "aws_api_gateway_base_path_mapping" "robotika-iowt-api-event" {
  api_id      = "${aws_api_gateway_rest_api.iowt-www.id}"
  stage_name  = "${aws_api_gateway_deployment.iowt-www-dev.stage_name}"
  domain_name = "${aws_api_gateway_domain_name.robotika-iowt-api.domain_name}"
  base_path = "event"
}



