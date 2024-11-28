from database.connect_db import connection
from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    zipcode: str| None
    latitude: float| None
    longitude: float| None
    city: str| None
    state_id: str| None
    state_name: str| None
    density: float| None
    county_fips: float| None
    county_name: str| None
    timezone: str| None
    hispanos_in_us: int | None
    population: int | None

conn= connection()
cursor = conn.cursor()

def insert_data(zipcode, latitude, longitude, city, state_id, state_name, density, county_fips, county_name, timezone, hispanos_in_us, population):
    cursor.execute("INSERT INTO audiencias (zipcode, latitude, longitude, city, state_id, state_name, density, county_fips, county_name, timezone, hispanos_in_us, population) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",(zipcode, latitude, longitude, city, state_id, state_name, density, county_fips, county_name, timezone, hispanos_in_us, population))
    conn.commit()
    #conn.close()

def get_data(limit: int, offset: int) -> List[Item]:
    cursor.execute("SELECT * FROM audiencias LIMIT ? OFFSET ?",(limit, offset))
    rows = cursor.fetchall()
    #conn.close

    items = [Item(zipcode=row[1], latitude=row[2], longitude=row[3], city=row[4], state_id=row[5], state_name=row[6], density=row[7], county_fips=row[8], county_name=row[9], timezone=row[10], hispanos_in_us=row[11], population=row[12]) for row in rows]
    return items

def get_total_count() -> int:
    cursor.execute("SELECT COUNT(*) FROM audiencias")
    total = cursor.fetchone()[0]
    #conn.close()
    return total
