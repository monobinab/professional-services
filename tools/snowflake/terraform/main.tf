// Configure the Google Cloud provider
provider "google" {
 credentials = "${file("cardinal-data-piper-sbx.json")}"
 project     = "cardinal-data-piper-sbx"
 region      = "us-west1"
}

//resource "google_sourcerepo_repository" "Billing" {
//  name = "Billing/snowflake"
//}

module "consul" {
 source = "git@github.com:monobinab/professional-services.git?ref=snowflake"
}

// Terraform plugin for creating random ids
resource "random_id" "instance_id" {
 byte_length = 8
}

/*resource "github_user_ssh_key" "snowflake_rsa" {
  title = "snowflake_rsa"
  key   = "${file("~/.ssh/terraform_key.pub")}"
}*/

provider "docker" {}

# declare any input variables

# create docker volume resource

# create docker network resource

# create db container

# create wordpress container
resource "docker_container" "snowflakebigqueryextract" {
  name  = "snowflakebigqueryextract"
  image = "snowflake-test:latest"
  restart = "always"
  ports = {
    internal = "80"
    external = "8080"
  }
}

// A single Google Cloud Engine instance
resource "google_compute_instance" "snowflake" {
   name         = "snowflake"
   machine_type = "f1-micro"
   zone         = "us-west1-a"

   tags = ["dataextract"]

   boot_disk {
     initialize_params {
       image = "cos-cloud/cos-stable"
     }
   }

   network_interface {
     network = "default"

     access_config {
       // Ephermal ip
     }
   }

   metadata = {
     sshKeys = "monobina:${file(var.ssh_public_key_filepath)}"
   }

   // Once VM is started, run these commands
   //metadata_startup_script = "${file("install_vm.sh")}"
   metadata_startup_script = "docker build --tag=snowflake-test . "


/*  service_account {
    "cardinal-data-piper-sbx@cardinal-data-piper-sbx.iam.gserviceaccount.com"
    scopes = ["cloud-platform", "compute-ro"]
  }*/
}

//resource "google_service_account" "object_viewer" {
  //account_id   = "cardinal-data-piper-sbx"
  //email = "cardinal-data-piper-sbx@cardinal-data-piper-sbx.iam.gserviceaccount.com"
  //name = "cardinal-data-piper-sbx"
//}

