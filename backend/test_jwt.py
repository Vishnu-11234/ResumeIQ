
from app.core.security import (
    create_access_token,
    verify_access_token
)


# Generate a token for user ID 1
token = create_access_token(1)

print("Generated token:", token[:30] + "...")

# Test valid token
valid_payload = verify_access_token(token)

print("Valid token result:", valid_payload)

# Test invalid token
invalid_payload = verify_access_token("invalid.token.value")

print("Invalid token result:", invalid_payload)

# Tamper with the original token's signature
parts = token.split(".")
parts[2] = ("A" if parts[2][0] != "A" else "B") + parts[2][1:]
tampered_token = ".".join(parts)

tampered_payload = verify_access_token(tampered_token)

print("Tampered token result:", tampered_payload)
