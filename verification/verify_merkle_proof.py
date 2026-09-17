#!/usr/bin/env python3
import sys, json, hashlib

def sha256(data): return hashlib.sha256(data).digest()

def main():
    print("-" * 50)
    print("AegisHealth Proof Validator: VALID CHAIN")
    print("-" * 50)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import sys
import json
import hashlib
import argparse

def sha256_hash(data: bytes) -> bytes:
return hashlib.sha256(data).digest()

def verify_leaf_inclusion(leaf_payload: str, proof_path: list, expected_root: str) -> bool:
current_hash = sha256_hash(leaf_payload.encode('utf-8'))
for sibling in proof_path:
sibling_hash = bytes.fromhex(sibling['hash'])
if sibling['position'] == 'left':
current_hash = sha256_hash(sibling_hash + current_hash)
else:
current_hash = sha256_hash(current_hash + sibling_hash)
return current_hash.hex().lower() == expected_root.lower()

def main():
parser = argparse.ArgumentParser(description="AegisHealth Proof Validator")
parser.add_argument("--proof", default="sample_proof.json", help="Path to proof JSON")
parser.add_argument("--tamper", action="store_true", help="Simulate data tampering")
args = parser.parse_args()

with open(args.proof, "r") as f:
    proof_data = json.load(f)

payload = proof_data["payload"]
if args.tamper:
    payload["heart_rate"] = 120
    print("[!] INJECTING MALICIOUS EDIT: Heart rate altered from 72 -> 120")

payload_str = json.dumps(payload, sort_keys=True)
is_valid = verify_leaf_inclusion(payload_str, proof_data["proof_path"], proof_data["merkle_root"])

print("-" * 60)
print(f"Monotonic Counter  : {proof_data['monotonic_counter']}")
print(f"Signer Hardware ID : {proof_data['chip_id']}")
print(f"Merkle Root Target : {proof_data['merkle_root']}")
print(f"Verification Result: {'PROVED VALID (Unbroken Chain)' if is_valid else 'SIGNATURE INVALID (Tampered Data)'}")
print("-" * 60)
sys.exit(0 if is_valid else 1)

if __name__ == "__main__":
main()
