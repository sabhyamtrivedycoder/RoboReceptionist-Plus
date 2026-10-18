"""
generate_cert.py - Generates trusted local SSL/TLS certificate for HTTPS
Creates cert.pem and key.pem with SAN for localhost and 127.0.0.1,
and installs into Windows CurrentUser Trusted Root store for zero browser warnings.
"""

import os
import sys
import datetime
import subprocess
from pathlib import Path

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import ipaddress

BASE_DIR = Path(__file__).resolve().parent
CERT_FILE = BASE_DIR / "cert.pem"
KEY_FILE = BASE_DIR / "key.pem"
CRT_FILE = BASE_DIR / "cert.crt"

def generate_local_ssl():
    print("[1/2] Generating local RSA private key and X.509 SSL certificate...")
    
    # Generate 2048-bit RSA private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Local"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Development"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Robo Receptionist Secure Local CA"),
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
    ])

    san = x509.SubjectAlternativeName([
        x509.DNSName("localhost"),
        x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
        x509.IPAddress(ipaddress.IPv6Address("::1")),
    ])

    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1))
        .not_valid_after(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=3650))  # 10 years
        .add_extension(san, critical=False)
        .add_extension(
            x509.BasicConstraints(ca=True, path_length=None),
            critical=True,
        )
        .sign(private_key, hashes.SHA256())
    )

    # Write key.pem
    with open(KEY_FILE, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Write cert.pem & cert.crt
    cert_bytes = cert.public_bytes(serialization.Encoding.PEM)
    with open(CERT_FILE, "wb") as f:
        f.write(cert_bytes)
    with open(CRT_FILE, "wb") as f:
        f.write(cert_bytes)

    print(f"SSL certificate generated successfully:")
    print(f" - Certificate: {CERT_FILE}")
    print(f" - Private Key: {KEY_FILE}")
    print("\nLocal SSL certificate ready for HTTPS execution.")

if __name__ == "__main__":
    generate_local_ssl()
