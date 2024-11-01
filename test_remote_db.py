import remote_db

def obtain_session():
  try:
    session = remote_db.get_session()
  except Exception as e:
    raise
  return next(session)

def select_turbine_farm(session):
  turbine_farm = remote_db.TurbineFarm
  for row in session.query(turbine_farm).all():
    print(f"Farm ID: {row.turbinefID}, Turbine ID: {row.turbineID}, Turbine Status: {row.turbineStatus}, Turbine Direction: {row.turbineDirection}, Turbine Generation: {row.turbineGeneration}")

if __name__ == '__main__':
  session = obtain_session()
  select_turbine_farm(session)
