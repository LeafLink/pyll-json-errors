"""Driver application for examples of Marshmallow integration."""
import json

from marshmallow import Schema, ValidationError, fields, validate, validates, validates_schema

from pyll_json_errors.contrib import marshmallow


# Various example Marshmallow Schema classes.
class EmailAddressSchema(Schema):
    email = fields.Email(required=True)
    name = fields.Str(required=False)

    @validates("email")
    def validates_email_tld(self, data):
        errs = []
        if not data.endswith(".com"):
            errs.append("Email must end in '.com'.")
        if "mark" in data:
            errs.append("Mark is not allowed.")
        if errs:
            raise ValidationError(errs)


class EmailMessageBodySchema(Schema):
    """De/serialize email body information."""

    html = fields.Str(required=False)
    text = fields.Str(required=True)

    def _validate_body_str(self, data):
        """Check if data is empty or only contains whitespace, if so it fails validation."""
        if data.strip() == "":
            raise ValidationError("Body content cannot be an empty or whitespace-only string.")

    @validates("text")
    def validates_text(self, data):
        self._validate_body_str(data)

    @validates("html")
    def validates_html(self, data):
        self._validate_body_str(data)


class EmailMessageSchema(Schema):
    """De/serialize email information."""

    sender = fields.Nested(EmailAddressSchema, data_key="from", required=True)
    to = fields.List(fields.Nested(EmailAddressSchema), required=False, validate=validate.Length(min=1))
    reply_to = fields.List(fields.Nested(EmailAddressSchema), required=False, validate=validate.Length(min=1))
    cc = fields.List(fields.Nested(EmailAddressSchema), required=False, validate=validate.Length(min=1))
    bcc = fields.List(fields.Nested(EmailAddressSchema), required=False, validate=validate.Length(min=1))
    subject = fields.Str(required=True)
    body = fields.Nested(EmailMessageBodySchema, required=True)

    def _validate_minimum_destinations(self, data, **kwargs):
        """to, bcc, and cc are all optional. But at least one must be provided."""
        err_msg = "Missing data for least one required field."
        to = data.get("to", None)
        cc = data.get("cc", None)
        bcc = data.get("bcc", None)

        if not to and not cc and not bcc:
            errs = {"to": err_msg, "bcc": err_msg, "cc": err_msg}
            raise ValidationError(errs)

    def _validate_unique_destinations(self, data, **kwargs):
        """to, bcc, and cc must contain unique addresses between them."""
        err_msg = "Destination email addresses must be unique."
        to = set(dest["email"].lower() for dest in data.get("to", []))
        cc = set(dest["email"].lower() for dest in data.get("cc", []))
        bcc = set(dest["email"].lower() for dest in data.get("bcc", []))

        if len(to.intersection(cc)) > 0 or len(to.intersection(bcc)) > 0 or len(cc.intersection(bcc)) > 0:
            errs = {"to": err_msg, "bcc": err_msg, "cc": err_msg}
            raise ValidationError(errs)

    @validates_schema
    def validates_email(self, data, **kwargs):
        self._validate_minimum_destinations(data, **kwargs)
        self._validate_unique_destinations(data, **kwargs)


def get_email_data(
    *,
    sender={"email": "caroline@leaflink.com", "name": "Caroline"},
    bcc=[
        {"email": "joker@phantomthieves.com", "name": "Protag"},
        {"email": "skull@phantomthieves.com", "name": "Ryuji Sakamoto"},
    ],
    cc=[
        {"email": "panther@phantomthieves.com", "name": "Ann Takamaki"},
    ],
    to=[
        {"email": "queen@phantomthieves.com", "name": "Makoto Niijima"},
    ],
    reply_to=[
        {"email": "morgana@phantomthieves.com", "name": "Morgana"},
    ],
    subject="Subject",
    body={"text": "A Basic Email", "html": "<em>A Fancy Email</em>"},
):
    """Gets example data to validate."""
    return {"from": sender, "bcc": bcc, "cc": cc, "to": to, "reply_to": reply_to, "subject": subject, "body": body}


def run_example(func_name, data):
    """Runs an example with some pretty printing."""
    print(f"|{func_name}() - Start|".center(80, "="))
    print(f"Data:")
    print(f"{json.dumps(data, indent=2)}\n")
    print("Reponse:")

    schema = EmailMessageSchema()
    try:
        schema.load(data)
    # Catch the validation error, transform, and print.
    except ValidationError as err:
        transform = marshmallow.ValidationErrorTransform()
        array = transform.to_array(sources=[err])
        print(json.dumps(array.as_dict(), indent=2))

    print(f"|{func_name}() - End|".center(80, "="))


def example_missing_field():
    """A required field is missing."""
    data = get_email_data()
    del data["from"]
    run_example("example_missing_field", data)


def multiple_errors():
    """Multiple validation errors."""
    data = get_email_data(subject=None)
    del data["from"]
    run_example("multiple_errors", data)


def nested_objects():
    """Nested objects."""
    data = get_email_data(sender={"email": "notvalid@.com]"})
    run_example("nested_objects", data)


def multiple_errors_on_same_field():
    """Multiple errors on a nested objec."""
    data = get_email_data(sender={"email": "mark@leaflink.net"})
    run_example("multiple_errors_on_same_field", data)


def arrays_of_objects():
    """Arrays of objects."""
    data = get_email_data()
    del data["bcc"][0]["email"]
    data["bcc"][1]["email"] = ""
    run_example("arrays_of_objects", data)


if __name__ == "__main__":
    example_missing_field()
    multiple_errors()
    nested_objects()
    multiple_errors_on_same_field()
    arrays_of_objects()
