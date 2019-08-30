variable "ssh_public_key_filepath" {
    description = "File path for ssh key"
    type = "string"

    default = "~/.ssh/terraform_key.pub"
}