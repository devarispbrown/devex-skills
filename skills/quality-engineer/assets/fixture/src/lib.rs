// Fixture rust library surface.
pub fn parse(input: &str) -> u64 {
    input.parse().unwrap_or(0)
}

#[test]
fn parses_digits() {
    assert_eq!(parse("42"), 42);
}

fuzz_target!(|data: &[u8]| {
    let _ = parse(std::str::from_utf8(data).unwrap_or(""));
});
