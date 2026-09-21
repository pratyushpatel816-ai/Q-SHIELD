from qshield.protocol.payload import CanonicalPayload
from qshield.protocol.signature import SignatureGenerator
from qshield.protocol.verifier import SignatureVerifier

payload = CanonicalPayload.create(
    expiry_minutes=10
)

generator = SignatureGenerator(shots=256)

signature = generator.generate(
    payload,
    signature_length=8
)

verifier = SignatureVerifier(shots=256)

print("FIRST VERIFICATION:")
first_result = verifier.verify(
    payload,
    signature
)
print(first_result)

print("\nREPLAY VERIFICATION:")
second_result = verifier.verify(
    payload,
    signature
)
print(second_result)