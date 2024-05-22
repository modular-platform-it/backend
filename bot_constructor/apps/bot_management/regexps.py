from ..bot_management import constants

VARIABLE_REGEXP = r"^[a-zA-Z0-9_]{1," + rf"{constants.VARIABLE_LENGTH}" + r"}"
COMMAND_KEYWORD_REGEXP = (
    r"^/[a-zA-Z0-9_]{1," + rf"{constants.COMMAND_KEYWORD_LENGTH}" + r"}$"
)
TELEGRAM_TOKEN_REGEXP = (
    r"^[0-9]{"
    + rf"{constants.MIN_TELEGRAM_ID_LENGTH},{constants.MAX_TELEGRAM_ID_LENGTH}"
    + r"}:[a-zA-Z0-9_-]"
    + rf"{{{constants.TELEGRAM_TOKEN_KEY_LENGTH}}}$"
)
HEADER_REGEXP = r"[a-zA-Z0-9-]{1," + rf"{constants.HEADER_LENGTH}" + r"}"
