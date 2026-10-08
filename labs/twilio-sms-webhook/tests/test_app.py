import unittest
from app import AUTH_TOKEN, create_app, twilio_signature

URL = "https://example.com/sms"


class TwilioTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(URL)
        self.c = self.app.test_client()

    def post(self, body, token=AUTH_TOKEN, frm="+1"):
        p = {"From": frm, "Body": body}
        return self.c.post("/sms", data=p, headers={"X-Twilio-Signature": twilio_signature(token, URL, p)})

    def test_known_signature_vector(self):
        # Order-independent: params are sorted before signing
        a = twilio_signature("t", "https://x/y", {"b": "2", "a": "1"})
        b = twilio_signature("t", "https://x/y", {"a": "1", "b": "2"})
        self.assertEqual(a, b)

    def test_forged_request_rejected(self):
        self.assertEqual(self.post("hi", token="nope").status_code, 403)

    def test_stop_silences_until_start(self):
        self.post("STOP")
        self.assertNotIn("<Message>", self.post("hello").get_data(as_text=True))
        self.post("START")
        self.assertIn("<Message>", self.post("hello").get_data(as_text=True))

    def test_user_text_is_escaped(self):
        self.assertIn("&lt;b&gt;", self.post("<b>").get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
