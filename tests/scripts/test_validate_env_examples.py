from scripts.validate_env_examples import compose_vars, parse_env_example


def test_compose_vars_parses_default_and_plain_interpolation():
    text = """
    environment:
      JWT_SECRET: ${JWT_SECRET}
      REDIS_URL: ${REDIS_URL:-redis://redis:6379/0}
    """
    assert compose_vars(text) == {"JWT_SECRET", "REDIS_URL"}


def test_parse_env_example_detects_duplicates_and_malformed_lines():
    text = """
    # comment
    JWT_SECRET=value
    REDIS_URL=redis://redis:6379/0
    JWT_SECRET=duplicate
    INVALID-KEY=value
    MISSING_EQUALS
    """
    keys, duplicates, malformed = parse_env_example(text)
    assert "JWT_SECRET" in keys
    assert "REDIS_URL" in keys
    assert duplicates == ["JWT_SECRET"]
    assert any("invalid key" in item for item in malformed)
    assert any("missing '='" in item for item in malformed)
