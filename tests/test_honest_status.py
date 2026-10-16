"""API failures must come back as errors, never as a job to wait for."""

UNAUTHORIZED = {
    "status": "error",
    "errorCode": 401,
    "error": True,
    "message": "Unauthorized. Authentication is required and has failed or has not yet been provided.",
}


async def test_api_error_is_reported_as_error(api, call):
    api.respond(401, UNAUTHORIZED)

    result = await call("pdf_to_text", url="https://example.com/in.pdf", api_key="bad")

    assert result.status == "error"
    assert result.content == UNAUTHORIZED
    assert "API key" in result.tips
    assert "wait_job_completion" not in result.tips


async def test_error_body_with_http_200_is_still_an_error(api, call):
    api.respond(200, {"error": True, "status": 402, "message": "Not enough credits."})

    result = await call("pdf_to_text", url="https://example.com/in.pdf", api_key="k")

    assert result.status == "error"
    assert "credits" in result.tips


async def test_synchronous_success_without_job_id(api, call):
    api.respond(
        200,
        {
            "status": "success",
            "url": "https://x/out.txt",
            "credits": 1,
            "remainingCredits": 9,
        },
    )

    result = await call("pdf_to_text", url="https://example.com/in.pdf", api_key="k")

    assert result.status == "success"
    assert result.credits_used == 1


async def test_non_json_body_is_an_error(api, call):
    api.respond(502, text="<html>Bad Gateway</html>")

    result = await call("pdf_to_text", url="https://example.com/in.pdf", api_key="k")

    assert result.status == "error"
    assert result.content.startswith("HTTP 502")


async def test_wait_job_completion_stops_on_api_error(api, call):
    api.respond(401, UNAUTHORIZED)

    result = await call(
        "wait_job_completion", job_id="JOB123", interval=0, timeout=5, api_key="bad"
    )

    assert result.status == "error"
    assert len(api.requests) == 1


async def test_wait_job_completion_treats_aborted_as_terminal(api, call):
    api.respond(200, {"status": "aborted", "message": "aborted"})

    result = await call(
        "wait_job_completion", job_id="JOB123", interval=0, timeout=5, api_key="k"
    )

    assert result.status == "error"
    assert len(api.requests) == 1


async def test_request_payload_is_not_logged(api, call, capsys):
    await call(
        "pdf_to_text",
        url="https://example.com/in.pdf",
        password="s3cret-pw",
        api_key="k",
    )

    err = capsys.readouterr().err
    assert "s3cret-pw" not in err
    assert "POST /v1/pdf/convert/to/text -> 200 jobId=JOB123" in err
