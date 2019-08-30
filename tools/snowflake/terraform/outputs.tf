output "external_ip" {
    value = "${google_compute_instance.snowflake.network_interface.0.access_config.0.assigned_nat_ip}"
}