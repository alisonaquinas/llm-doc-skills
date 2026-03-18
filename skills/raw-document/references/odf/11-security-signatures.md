# ODF Security, Encryption, and Digital Signatures

> **Cross-references:** [Package Structure](./03-package-structure.md) | [Specification](./02-specification.md) | [Best Practices](./12-best-practices.md)

---

## 1. Overview

ODF provides three security mechanisms:

1. **Document encryption** — encrypt entire document (password or OpenPGP)
2. **Protection locks** — restrict editing of specific elements
3. **Digital signatures** — verify document authenticity and integrity

These are specified in ODF 1.2 Part 3 (Packages) and significantly enhanced in ODF 1.3.

---

## 2. Document Encryption

### Password-Based Encryption (ODF 1.2+)

ODF encrypts individual files within the ZIP package. The `META-INF/manifest.xml` stores encryption parameters for each encrypted file. **`META-INF/manifest.xml` itself MUST NOT be encrypted.**

#### Encryption Algorithm Chain

```text
Password
   ↓ PBKDF2 (key derivation)
  Key (32 bytes for AES-256)
   ↓ AES-256-CBC (encryption)
  Encrypted content bytes
```

#### Manifest Entry for Encrypted File

```xml
<manifest:file-entry
    manifest:full-path="content.xml"
    manifest:media-type="text/xml"
    manifest:size="15248">            <!-- uncompressed size -->

  <manifest:encryption-data
      manifest:checksum-type="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0#sha256-1k"
      manifest:checksum="BASE64_ENCODED_SHA256_OF_FIRST_1024_BYTES">

    <manifest:algorithm
        manifest:algorithm-name="http://www.w3.org/2001/04/xmlenc#aes256-cbc"
        manifest:initialisation-vector="BASE64_IV_16_BYTES"/>

    <manifest:key-derivation
        manifest:key-derivation-name="PBKDF2"
        manifest:key-size="32"
        manifest:iteration-count="100000"
        manifest:salt="BASE64_SALT_16_BYTES"/>

    <manifest:start-key-generation
        manifest:start-key-generation-name="http://www.w3.org/2000/09/xmldsig#sha256"
        manifest:key-size="32"/>

  </manifest:encryption-data>
</manifest:file-entry>
```

#### Supported Algorithms

| Component | Recommended | Legacy |
| --- | --- | --- |
| Key derivation | PBKDF2 | Blowfish + SHA-1 |
| Key size | 32 bytes (AES-256) | 16 bytes (AES-128) |
| Encryption | AES-256-CBC | Blowfish-CFB, AES-128-CBC |
| Checksum | SHA-256 | SHA-1 |
| Iterations | 100,000+ | 1,024 |

### OpenPGP Encryption (ODF 1.3)

ODF 1.3 adds support for OpenPGP (RFC 4880) encryption as an alternative to password-based encryption. This allows encryption to a specific recipient's public key without requiring a shared password.

```xml
<manifest:file-entry manifest:full-path="content.xml"
                     manifest:media-type="text/xml">
  <manifest:encryption-data>

    <!-- Session key encrypted to each recipient -->
    <manifest:keyinfo>
      <manifest:pgp-key-id>0xABCDEF0123456789</manifest:pgp-key-id>
    </manifest:keyinfo>

    <manifest:encrypted-key>
      <!-- Base64-encoded OpenPGP encrypted session key -->
      <manifest:pgp-encrypted-key-packet>
        BASE64_ENCODED_PGP_PACKET
      </manifest:pgp-encrypted-key-packet>
    </manifest:encrypted-key>

    <manifest:algorithm
        manifest:algorithm-name="http://www.w3.org/2001/04/xmlenc#aes256-cbc"
        manifest:initialisation-vector="BASE64_IV"/>

  </manifest:encryption-data>
</manifest:file-entry>
```

---

## 3. Protection Locks

Protection locks prevent editing specific document elements without requiring encryption. Protected elements can still be read but not modified.

### Sheet Protection (Spreadsheets)

```xml
<table:table table:name="Sheet1" table:protected="true">
  <!-- Sheet content — locked for editing -->
</table:table>
```

With password protection:

```xml
<table:table table:name="Sheet1"
             table:protected="true"
             table:protection-key="BASE64_HASH"
             table:protection-key-digest-algorithm="http://www.w3.org/2000/09/xmldsig#sha256">
```

### Section Protection (Text Documents)

```xml
<style:section-properties style:editable="false"/>

<text:section text:name="ProtectedSection"
              text:protected="true"
              text:protection-key="BASE64_HASH">
  <!-- Protected section content -->
</text:section>
```

### Cell Protection (Spreadsheets)

```xml
<style:table-cell-properties style:cell-protect="protected"/>
```

Values for `style:cell-protect`:

- `none` — cell is not protected
- `protected` — cell content protected when sheet is protected
- `formula-hidden` — formula hidden when sheet is protected
- `protected formula-hidden` — both

---

## 4. Digital Signatures

ODF 1.2+ supports digital signatures using W3C XML Signature Syntax and Processing (xmldsig). ODF 1.3 additionally supports **XAdES** (XML Advanced Electronic Signatures) extensions.

### Signature File Location

```text
META-INF/
├── manifest.xml
├── documentsignatures.xml   ← Signatures on document content
└── macrosignatures.xml      ← Signatures on macros/scripts
```

These files MUST be listed in `manifest.xml`:

```xml
<manifest:file-entry
    manifest:full-path="META-INF/documentsignatures.xml"
    manifest:media-type="application/vnd.oasis.opendocument.dsig+xml"/>
```

### Basic XML Signature Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<document-signatures
    xmlns="urn:oasis:names:tc:opendocument:xmlns:digitalsignature:1.0"
    xmlns:ds="http://www.w3.org/2000/09/xmldsig#"
    xmlns:xades="http://uri.etsi.org/01903/v1.3.2#">

  <ds:Signature Id="Signature1">

    <ds:SignedInfo>
      <ds:CanonicalizationMethod
          Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
      <ds:SignatureMethod
          Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"/>

      <!-- Reference to document content -->
      <ds:Reference URI="content.xml">
        <ds:DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"/>
        <ds:DigestValue>BASE64_SHA256_OF_CONTENT_XML</ds:DigestValue>
      </ds:Reference>

      <!-- Reference to styles -->
      <ds:Reference URI="styles.xml">
        <ds:DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"/>
        <ds:DigestValue>BASE64_SHA256_OF_STYLES_XML</ds:DigestValue>
      </ds:Reference>

    </ds:SignedInfo>

    <ds:SignatureValue>BASE64_SIGNATURE_VALUE</ds:SignatureValue>

    <ds:KeyInfo>
      <ds:X509Data>
        <ds:X509Certificate>BASE64_DER_CERTIFICATE</ds:X509Certificate>
      </ds:X509Data>
    </ds:KeyInfo>

    <!-- XAdES properties (ODF 1.3 — recommended) -->
    <ds:Object>
      <xades:QualifyingProperties Target="#Signature1">
        <xades:SignedProperties>
          <xades:SignedSignatureProperties>
            <xades:SigningTime>2024-03-15T14:30:00Z</xades:SigningTime>
            <xades:SigningCertificate>
              <xades:Cert>
                <xades:CertDigest>
                  <ds:DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"/>
                  <ds:DigestValue>BASE64_CERT_HASH</ds:DigestValue>
                </xades:CertDigest>
                <xades:IssuerSerial>
                  <ds:X509IssuerName>CN=My CA, O=Example</ds:X509IssuerName>
                  <ds:X509SerialNumber>12345</ds:X509SerialNumber>
                </xades:IssuerSerial>
              </xades:Cert>
            </xades:SigningCertificate>
          </xades:SignedSignatureProperties>
        </xades:SignedProperties>
      </xades:QualifyingProperties>
    </ds:Object>

  </ds:Signature>

</document-signatures>
```

---

## 5. XAdES Extensions (ODF 1.3)

XAdES (ETSI EN 319 132) provides extended digital signature metadata:

| XAdES Level | Description | ODF Support |
| --- | --- | --- |
| XAdES-B-B | Basic: timestamp and signing certificate | Recommended in ODF 1.3 |
| XAdES-B-T | With trusted timestamp | Supported |
| XAdES-B-LT | With full certificate chain | Supported |
| XAdES-B-LTA | Long-term archival signatures | Supported |

XAdES adds:

- Signing time (non-repudiation)
- Signer role (claimed roles and certified roles)
- Signer location
- Commitment type indication (what the signer attests to)
- Certificate validation data

---

## 6. Signature Verification Guidance

When verifying ODF digital signatures:

1. Confirm `META-INF/documentsignatures.xml` is present and listed in manifest
2. Verify the certificate chain against trusted CAs
3. Check that all referenced package parts have matching digest values
4. Verify the `ds:SignatureValue` against the signing certificate
5. If XAdES: check the XAdES qualified properties for signing time, commitment type
6. If timestamps present: verify the timestamp against TSA certificate

**Important**: Modifying any file listed as a `ds:Reference` invalidates the signature, even if the modification is minor (e.g., re-saving with different compression).

---

## 7. Security Best Practices

| Practice | Recommendation |
| --- | --- |
| Password strength | Minimum 16 characters, mixed character sets |
| Key derivation iterations | 100,000+ PBKDF2 iterations |
| Encryption algorithm | AES-256-CBC (avoid legacy AES-128 or Blowfish) |
| Signature algorithm | RSA-SHA256 or ECDSA-SHA256 (avoid SHA-1) |
| Certificate management | Use certificates from trusted CAs with 2+ year validity |
| XAdES | Use XAdES-B-T or higher for long-term signatures |
| Transport | Always use TLS when transmitting encrypted ODF over network |
| Backup | Maintain password-protected backup of signing keys |

---

*Previous: [Metadata ←](./10-metadata.md) | Next: [Best Practices →](./12-best-practices.md)*
