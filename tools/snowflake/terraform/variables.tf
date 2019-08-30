variable project_id {
    description="GCP Project ID to host the GCS billing export resources"
}

variable "service_account" {
    description="Service account to be used for deployment and operation"
}

variable "credentials_path" {
    description = "Path to the service account credentials JSON file. Download from your GCP Service Accounts Console."
  
}


variable "region" {
    description="GCP region where the solution would be deployed."
    default="us-central1"
}

variable "zone" {
  description="GCP zone where the solution would be deployed."
  default="us-central1-f"
}



