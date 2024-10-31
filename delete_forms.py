import database as db

def obtain_session():
  try:
    session = db.get_session()
  except Exception as e:
    raise
  return next(session)

session = obtain_session()

def main():
  db.delete_all_forms(session)
  print(f"All forms deleted successfully!")

if __name__ == '__main__':
  main()