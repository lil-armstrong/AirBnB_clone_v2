#!/usr/bin/python3
import os


def getEnv(key: str) -> str:
    """
    Get the value of an environment variable

    Parameters:
        key(str): Target of environment variable key

    Returns:
        str: value of the environment variable key

    Example:
        >>> getEnv('IS_DEV')
    """
    return os.environ.get(key)


def setEnv(key: str, value: int) -> None:
    """ Set the value of an environment variable key

    Parameters:
        key(str): Environment variable key
        value(int): Value of the key
    """
    os.environ[key] = value
