from app import AUTH_TOKEN, create_app, twilio_signature

URL = "https://example.com/sms"
app = create_app(URL)
c = app.test_client()


def send(body, frm="+13175550100", token=AUTH_TOKEN):
    params = {"From": frm, "Body": body, "To": "+13175550199", "MessageSid": "SM123"}
    r = c.post("/sms", data=params, headers={"X-Twilio-Signature": twilio_signature(token, URL, params)})
    return r.status_code, r.get_data(as_text=True)


for body in ("tickets?", "<script>hi</script>", "STOP", "tickets?", "START"):
    print(f"{body!r:22} ->", *send(body))
print(f"{'forged request':22} ->", send("hi", token="wrong")[0])
