resource "aws_dynamodb_table" "iowt-events" {
  name           = "iowt-events"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "id"

  attribute {
    name = "id"
    type = "S"
  }

}





