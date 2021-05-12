# Rainbow
Implementation of an interactive signing/verifying announcements using the Rainbow Signature Scheme.

# rainbow package
Contains the actual implementation of the Rainbow Signature Scheme.

Packages needed:
- pyfinite
- random

# announcements package
Data/Verification base that allows you to write announcements as an user, generating a signature for it. It also allows you to verify if a certain announcement was made by a certain user by using its public key and comparing it to the announcement.
Note: Use only lower case letters and space.