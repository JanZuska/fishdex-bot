from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session
import json
import os

Base = declarative_base()

class Fish(Base):
    __tablename__ = "fish"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    locations = Column(String(255), nullable=False)

class FishUserData(Base):
    __tablename__ = "fish_user_data"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    fish_id = Column(Integer, ForeignKey("fish.id"), nullable=False)
    caught = Column(Boolean, default=False)
    shiny = Column(Boolean, default=False)

    fish = relationship("Fish")
    __table_args__ = (UniqueConstraint('user_id', 'fish_id', name='_user_fish_uc'),)

engine = create_engine(os.getenv("DATABASE_URL"))
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

def preload_fish_table():
    with open("assets/json/database-table.json", "r") as file:
        fish_data = json.load(file)

    session: Session = SessionLocal()
    try:
        if session.query(Fish).count() > 0:
            print("Fish table already populated.")
            return

        session.add_all([Fish(name=name, locations=locations) for name, locations in fish_data])
        session.commit()
        print(f"Inserted {len(fish_data)} fish into the table.")
    finally:
        session.close()

class Database:
    def __init__(self, user_id: str):
        self.user_id = str(user_id)
        self.session = SessionLocal()

    def _get_or_create_userdata(self, fish_id: int) -> FishUserData:
        userdata = self.session.query(FishUserData).filter_by(
            user_id=self.user_id, fish_id=fish_id
        ).first()
        if not userdata:
            userdata = FishUserData(user_id=self.user_id, fish_id=fish_id)
            self.session.add(userdata)
            self.session.commit()
        return userdata

    def _get_fish_by_location(self, location_id: str) -> list[Fish]:
        query = self.session.query(Fish)
        if location_id == "1":
            query = query.filter(
                (Fish.locations.like(f"%1%")) | (Fish.locations.like(f"%101%"))
            )
        elif location_id == "5":
            query = query.filter(
                (Fish.locations.like(f"%5%")) | (Fish.locations.like(f"%104%"))
            )
        else:
            query = query.filter(Fish.locations.like(f"%{location_id}%"))
        return query.all()

    def Caught(self, location_id: str = None) -> str:
        fish_list = self._get_fish_by_location(location_id) if location_id else self.session.query(Fish).all()
        fish_ids = [f.id for f in fish_list]

        caught = self.session.query(FishUserData).filter(
            FishUserData.user_id == self.user_id,
            FishUserData.fish_id.in_(fish_ids),
            FishUserData.caught.is_(True)
        ).count()

        total = len(fish_ids)
        return f"{caught}/{total}"

    def Shiny(self, location_id: str = None) -> str:
        fish_list = self._get_fish_by_location(location_id) if location_id else self.session.query(Fish).all()
        fish_ids = [f.id for f in fish_list]

        shiny = self.session.query(FishUserData).filter(
            FishUserData.user_id == self.user_id,
            FishUserData.fish_id.in_(fish_ids),
            FishUserData.shiny.is_(True)
        ).count()

        total = len(fish_ids)
        return f"{shiny}/{total}"

    def isCaught(self, fish_name: str) -> bool:
        fish = self.session.query(Fish).filter_by(name=fish_name).first()
        if not fish:
            return False
        userdata = self.session.query(FishUserData).filter_by(
            user_id=self.user_id, fish_id=fish.id
        ).first()
        return bool(userdata and userdata.caught)

    def isShiny(self, fish_name: str) -> bool:
        fish = self.session.query(Fish).filter_by(name=fish_name).first()
        if not fish:
            return False
        userdata = self.session.query(FishUserData).filter_by(
            user_id=self.user_id, fish_id=fish.id
        ).first()
        return bool(userdata and userdata.shiny)

    def SetCaught(self, fish_name: str, value: bool) -> None:
        fish = self.session.query(Fish).filter_by(name=fish_name).first()
        if not fish:
            raise ValueError(f"Fish '{fish_name}' not found.")
        userdata = self._get_or_create_userdata(fish.id)
        userdata.caught = value
        self.session.commit()

    def SetShiny(self, fish_name: str, value: bool) -> None:
        fish = self.session.query(Fish).filter_by(name=fish_name).first()
        if not fish:
            raise ValueError(f"Fish '{fish_name}' not found.")
        userdata = self._get_or_create_userdata(fish.id)
        userdata.shiny = value
        self.session.commit()

    def close(self):
        self.session.close()