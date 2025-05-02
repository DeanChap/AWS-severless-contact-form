output "api_endpoint" {
  value = "${aws_apigatewayv2_api.contact_form_api.api_endpoint}/contact"
}
