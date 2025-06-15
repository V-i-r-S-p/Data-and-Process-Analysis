def data_parser(filePath: str) -> list[str] | None:
  data = []

  try:
    with open(filePath) as file:
      for line in file:
        data_ = line.strip()
        if len(data_) != 0 and data_[0] != '%':
          data.append(data_)
  except (FileNotFoundError or FileExistsError) as e:
    print(e)
    data = None

  return data
