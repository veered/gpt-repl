import os, openai, re, sys, tiktoken

class GPT3:

  def __init__(self, model='text-davinci-003', temperature=0.7):
    if not os.environ.get('OPENAI_API_KEY'):
      print("Please set the OPENAI_API_KEY environment variable. If you don't have one you can generate one here https://beta.openai.com/account/api-keys")
      sys.exit(0)

    self.model = model
    self.temperature = temperature
    self.tokenizer = tiktoken.get_encoding("gpt2")

  def count_tokens(self, text):
    return len(self.tokenizer.encode(text))

  def complete(self, *args, **kwargs):
    if kwargs.get('stream', False):
      return self.__complete_async(*args, **kwargs)
    else:
      return self.__complete_sync(*args, **kwargs)

  def __complete_sync(self, *args, **kwargs):
    kwargs['stream'] = False
    response = self.get_response(*args, **kwargs)
    return response.choices[0].text

  def __complete_async(self, *args, **kwargs):
    kwargs['stream'] = True
    response = self.get_response(*args, **kwargs)
    for data in response:
      yield data.choices[0].text

  def get_response(self, prompt, max_length=1000, stop=None, stream=False):
    # max_length = 2000
    return openai.Completion.create(
      engine=self.model,
      prompt=prompt,
      max_tokens=max_length,
      temperature=self.temperature,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      stop=stop,
      stream=stream,
      # logit_bias={
      #   '2949': 1, # Make "No" a more common token
      #   '44651': 1, # Make "Invalid" a more common token
      # },
    )
