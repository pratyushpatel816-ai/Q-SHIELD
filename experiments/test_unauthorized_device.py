from qshield.protocol.payload import CanonicalPayload
from qshield.protocol.signature import SignatureGenerator
from qshield.protocol.verifier import SignatureVerifier

payload = CanonicalPayload.create(
    expiry_minutes=10
)

payload["device_id"] = "ATTACKER_DEVICE"

generator = SignatureGenerator(shots=256)

signature = generator.generate(
    payload,
    signature_length=8
)

verifier = SignatureVerifier(shots=256)

result = verifier.verify(
    payload,
    signature
)

print(result)