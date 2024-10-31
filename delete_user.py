import database as db
import argparse
import bcrypt

parser = argparse.ArgumentParser(description='Add a user to the database')
parser.add_argument('--username', type=str, help='The username of the user to delete')

def obtain_session():
  try:
    session = db.get_session()
  except Exception as e:
    raise
  return next(session)

session = obtain_session()

def main(args):
  db.delete_user(session, args.username)
  print(f"User {args.username} deleted successfully")

if __name__ == '__main__':
  args = parser.parse_args()
  main(args)