from utils.enviroment import parse_coma_separated_str_to_list, get_env_variable


CORS_ALLOWED_ORIGINS: list[str] = parse_coma_separated_str_to_list(
    get_env_variable('CORS_ALLOWED_ORIGINS'))  # noqa E501
