import os

from modules import logger, add_url_with_error, delay

import openai
openai.api_key = os.getenv('OPENAI_TOKEN')


def get_gpt_response(task_for_gpt, str_prompt, url=None):
    """Get response from GPT-3.5 turbo API.
    :param task_for_gpt: Task for GPT-3.5 turbo API. What to do with the prompt.
    :param str str_prompt: Prompt to send to the API
    :return: str Response from the API"""

    if not str_prompt or not isinstance(str_prompt, str):
        raise ValueError("'str_prompt' is missing or not of 'str' type")

    messages = [
        {"role": "system", "content": task_for_gpt},
        {"role": "user", "content": str_prompt},
    ]

    retries = 5
    for i in range(retries):
        logger.info(f"Try to get response from GPT-3.5 turbo API:  {i + 1}/{retries}")
        duration = 3 ** (i + 1)
        try:

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                **{
                    "temperature": 1,
                    "max_tokens": 2000,
                    "top_p": 1,
                    "frequency_penalty": 0,
                    "presence_penalty": 0
                }
            )

            for choice in response.choices:
                content = choice.message['content'].strip()
                if "Error: Exceeded maximum token length" in content:
                    if url:
                        add_url_with_error(url)
                    break

            return content

        except openai.error.AuthenticationError as err:
            logger.error(f'Authentication failed: {err}')
            add_url_with_error(url)
            raise err from None
        except openai.error.PermissionError as err:
            logger.error(f'Permission denied: {err}')
            add_url_with_error(url)
            raise err from None
        except openai.error.InvalidRequestError as err:
            logger.warning(f'The request was too long: {err}. Skipping this iteration...')
            add_url_with_error(url)
            continue
        except openai.error.RateLimitError as err:
            logger.warning(f'Rate limit exceeded: {err}. Retrying after delay...')
            delay(duration)  # delay increases with each retry
            continue
        except openai.error.ServiceUnavailableError as err:
            logger.warning(f'Server is overloaded or not ready yet: {err}. Retrying after delay...')
            delay(duration)  # delay increases with each retry
            continue
        except openai.error.APIError as err:
            if err.status_code == 502:
                logger.warning(f'API Error: HTTP code 502. Retrying after delay...')
            else:
                logger.error(f'An OpenAI API error occurred: {err}')
            add_url_with_error(url)
            delay(duration)  # delay increases with each retry
            raise err from None
        except openai.error.OpenAIError as err:
            logger.error(f'An OpenAI error occurred: {err}')
            add_url_with_error(url)
            delay(duration)  # delay increases with each retry
            raise err from None
        except Exception as e:
            logger.error(f'An unexpected error occurred: {e}')
            add_url_with_error(url)
            delay(duration)  # delay increases with each retry
            raise e from None
