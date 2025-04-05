# Clarification of `return_codes` Naming Convention

## Current Status

In the WDL specification version 1.2:

- The primary attribute name is `return_codes` (snake_case)
- `returnCodes` (camelCase) is listed as an alias
- All examples in the specification use the snake_case form: `return_codes`

## Recommended Usage

To maintain consistency and ensure compliance with the specification:

1. WDL authors should use `return_codes` (snake_case) in task requirements sections
2. Implementation engines should accept both `return_codes` and `returnCodes` for backward compatibility
3. All documentation and examples should consistently use `return_codes` (snake_case)

## Future Plans

- In WDL 1.3: Both forms will remain supported, but `returnCodes` (camelCase) will be formally deprecated
- In WDL 2.0: Only `return_codes` (snake_case) will be supported

This clarification aims to resolve the discrepancy between naming conventions in the specification and examples. 