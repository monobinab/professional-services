provider "google" {
  project = "${var.project_id}"
  region = "${var.region}"
  credentials="${file(var.credentials_path)}"
}

data "google_compute_image" "ubuntu" {
  family = "ubuntu-1804-lts"
  project = "gce-uefi-images"
}

resource "google_compute_instance_template" "exporter_vm_template" {
    name_prefix = "billing-exporter-instance-template-"
    description = "This VM is being used to dump the billing data from Big Query to a designated GCS bucket."
    instance_description = "Billing Exporter Job Server"
    machine_type         = "n1-standard-1"
    can_ip_forward       = false

    scheduling {
        preemptible = true
        automatic_restart   = false
        on_host_maintenance = "TERMINATE"
    }

  // Create a new boot disk from an image
    disk {
        source_image = "${data.google_compute_image.ubuntu.self_link}"
        auto_delete  = true
        boot         = true
    }
    network_interface {
        network = "default"
    }
    service_account {
        email = "${var.service_account}"
        scopes = ["cloud-platform"]
    }
    metadata_startup_script = <<SCRIPT
    sudo apt-get update
    sudo apt-get install -yq python3  python-pip3 build-essential libssl-dev libffi-dev python-dev
    pip install google-cloud-storage
    gcloud init
    mkdir /opt/billing_exporter
    cd /opt/billing-exporter
    touch placeholder.txt
    SCRIPT
    lifecycle {
        create_before_destroy = true
    }
}

resource "google_compute_instance_from_template" "test_vm" {
  name = "billing-export-test-vm"
  zone = "${var.zone}"
  source_instance_template = "${google_compute_instance_template.exporter_vm_template.self_link}"
  scheduling {
    preemptible = true
    automatic_restart   = false
    on_host_maintenance = "TERMINATE"
    }
}

