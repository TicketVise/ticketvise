import secrets

print("LTI_KEY:")
print(secrets.token_hex(16))
print()
print("LTI_SECRET:")
print(secrets.token_hex(32))
