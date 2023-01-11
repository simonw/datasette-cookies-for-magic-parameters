from datasette.app import Datasette
import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "path,expect_javascript,expected_status",
    (
        ("/", False, 200),
        ("/_memory", False, 200),
        # 400 because "You did not supply a value for binding parameter"
        ("/_memory/name", True, 400),
        ("/_memory/other", False, 200),
    ),
)
async def test_javascript_present(path, expect_javascript, expected_status):
    datasette = Datasette(
        memory=True,
        metadata={
            "databases": {
                "_memory": {
                    "queries": {"name": "select :_cookie_name", "other": "select 1 + 2"}
                }
            }
        },
    )
    response = await datasette.client.get(path)
    assert response.status_code == expected_status
    if expect_javascript:
        assert "enhanceMagicParameterForm()" in response.text
    else:
        assert "enhanceMagicParameterForm()" not in response.text
