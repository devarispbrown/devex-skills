# Fixture terraform surface.
resource "aws_s3_bucket" "fixture" {
  bucket = "quality-engineer-fixture"
}
