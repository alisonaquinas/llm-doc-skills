# AsciiDoc Attributes and Includes

Authoritative source:
- AsciiDoc language documentation: <https://docs.asciidoctor.org/asciidoc/latest/>

## High-value constructs

- document attributes for metadata and behavior switches
- includes for shared partials and reused content
- conditionals around attributes
- admonitions and callouts for procedural content

```adoc
= Guide Title
:toc:
:sectnums:

include::partials/intro.adoc[]
```

## Guidance

Keep includes explicit and predictable.
Use attributes for document configuration, not for obscuring the source model.
