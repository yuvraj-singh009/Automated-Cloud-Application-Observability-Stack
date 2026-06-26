resource "aws_instance" "soc_server" {

  ami           = "ami-01a00762f46d584a1"
  instance_type = "t3.micro"

  subnet_id = aws_subnet.public.id

  vpc_security_group_ids = [
    aws_security_group.soc_sg.id
  ]

  key_name = "soc-key"

  user_data = file("userdata.sh")

  tags = {
    Name = "soc-dashboard-server"
  }
}