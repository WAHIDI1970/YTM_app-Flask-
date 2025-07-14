from datetime import datetime
dummy_date_ec = datetime(2023, 1, 1) # Example date
dummy_date_em = datetime(2023, 1, 1) # Example date
dummy_date_v = datetime(2023, 1, 15) # Example date
dummy_date_dC = datetime(2022, 12, 15) # Example date

def calcule_prix_dirty_corrected(face_value, coupon_payment, discount_rate, periods):

  P_dirty = 0
  for i in range(1, periods + 1):
      if i == periods:
          P_dirty += (coupon_payment + face_value) / (1 + discount_rate)**i
      else:
          P_dirty += coupon_payment / (1 + discount_rate)**i
  return P_dirty
