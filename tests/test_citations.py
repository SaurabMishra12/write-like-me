import pytest


@pytest.mark.parametrize("before,after", [
    (r"See \cite{shannon1948}.", r"See \cite{other1948}."),
    (r"See \citep[p. 3]{alpha,beta}.", r"See \citep[p. 3]{alpha}."),
    ("See [paper](https://example.org/a).", "See [paper](https://example.org/b)."),
    ("See [paper][ref].\n\n[ref]: https://example.org/a", "See [paper][ref]."),
    (r"\bibitem{key} Author. Title.", r"\bibitem{key} Author. Another Title."),
    ("# References\n\nAuthor. Title. 1948.", "# References\n\nAuthor. Different title. 1948."),
    ("See https://example.org/a.", "See https://example.org/b."),
])
def test_reference_mutations_veto(tool, before, after):
    assert tool("preservation_checker").check(before, after)["decision"] == "veto"


def test_prose_edit_preserves_nested_markdown_destination(tool):
    a = "Read [this paper](https://example.org/paper_(final)) carefully."
    b = "Read [this paper](https://example.org/paper_(final)) now."
    r = tool("preservation_checker").check(a, b)
    assert r["decision"] == "review_required"
