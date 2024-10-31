import database as db
import argparse
import bcrypt

parser = argparse.ArgumentParser(description='Add a user to the database')
parser.add_argument('--username', type=str, help='The username of the user')
parser.add_argument('--password', type=str, help='The password of the user')
parser.add_argument('--admin', action='store_true', help='Make the user an admin')

def obtain_session():
  try:
    session = db.get_session()
  except Exception as e:
    raise
  return next(session)

session = obtain_session()

def main(args):
  hashed_password = bcrypt.hashpw(args.password.encode('utf-8'), bcrypt.gensalt())
  db.create_user(session, args.username, hashed_password, args.admin)
  print(f"User {args.username} created successfully")

if __name__ == '__main__':
  args = parser.parse_args()
  main(args)