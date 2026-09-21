from qshield.protocol.payload import CanonicalPayload
from qshield.protocol.signature import SignatureGenerator
from qshield.protocol.verifier import SignatureVerifier

payload = CanonicalPayload.create(
    expiry_minutes=10
)

generator = SignatureGenerator(
    shots=256
)

signature = generator.generate(
    payload,
    signature_length=8
)

# Tamper with the first quantum position
original_bit = signature["positions"][0]["expected_bit"]

signature["positions"][0]["expected_bit"] = (
    1 - original_bit
)

verifier = SignatureVerifier(
    shots=256
)

result = verifier.verify(
    payload,
    signature
)

print(result)