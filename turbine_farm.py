import remote_db

def obtain_session():
  try:
    session = remote_db.get_session()
  except Exception as e:
    raise
  return next(session)

def export_farms_to_json():
  session = obtain_session()
  turbine_farm = remote_db.TurbineFarm
  farms = []
  for row in session.query(turbine_farm).all():
    farms.append({
      "turbinefID": row.turbinefID,
      "turbineID": row.turbineID,
      "turbineStatus": row.turbineStatus,
      "turbineDirection": row.turbineDirection,
      "turbineGeneration": row.turbineGeneration
    })
  return farms
