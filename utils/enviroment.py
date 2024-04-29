import os


def get_env_variable(variable_name, default_name=''):
    return os.environ.get(variable_name, default_name)


def parse_coma_separated_str_to_list(comma_separated_str):
    if not comma_separated_str or not isinstance(comma_separated_str, str):
        return []
    return [string.strip() for string in comma_separated_str.split(',')]


if __name__ == "__main__":
    print(parse_coma_separated_str_to_list('a, b, c, b, g'))
