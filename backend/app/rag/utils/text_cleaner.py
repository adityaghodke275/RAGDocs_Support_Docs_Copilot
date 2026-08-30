import re


class TextCleaner:

    @staticmethod
    def clean(text: str):

        if not text:
            return ""

        # Remove references
        text = re.split(
            r"\nREFERENCES",
            text,
            flags=re.IGNORECASE,
        )[0]

        # Remove acknowledgement
        text = re.split(
            r"\nACKNOWLEDG",
            text,
            flags=re.IGNORECASE,
        )[0]

        # Collapse blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()