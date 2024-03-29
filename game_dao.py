from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column, ForeignKey, select
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from model.game import Game
from model.player import Player
from model.vessel import Vessel

engine = create_engine('sqlite:////tmp/tdlog.db', echo=True, future=True)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)


class GameEntity(Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True)
    player = relationship("PlayerEntity", back_populates="game",
                          cascade="all, delete-orphan")


class PlayerEntity(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    game_id = Column(Integer, ForeignKey("game.id"), nullable=False)
    game = relationship("GameEntity", back_populates="player")
    battle_field = relationship("BattlefieldEntity", back_populates="player", uselist=False,
                                cascade="all, delete-orphan")


class BattlefieldEntity(Base):
    __tablename__ = 'battlefield'
    id = Column(Integer, primary_key=True)
    min_x = Column(Integer)
    min_y = Column(Integer)
    min_z = Column(Integer)
    max_x = Column(Integer)
    max_y = Column(Integer)
    max_z = Column(Integer)
    max_power = Column(Integer)
    player_id = Column(Integer, ForeignKey("player.id"), nullable=False)
    player = relationship("PlayerEntity", back_populates="battle_field")
    vessel = relationship("VesselEntity", back_populates="vessel", uselist=False, cascade="all, delete-orphan")


class VesselEntity(Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True)
    coord_x = Column(Integer)
    coord_y = Column(Integer)
    coord_z = Column(Integer)
    hits_to_be_destroyed = Column(Integer)
    type = Column(String)
    Battle_field_id = Column(Integer, ForeignKey("battlefield.id"), nullable=False)
    battle_field = relationship("BattlefieldEntity", back_populates="battle_field")
    weapon = relationship("WeaponEntity", back_populates="vessel", uselist=False, cascade="all, delete-orphan")


class WeaponEntity(Base):
    id = Column(Integer, primary_key=True)
    ammunations = Column(Integer)
    range = Column(Integer)
    type = Column(String)
    vessel_id = Column(Integer, ForeignKey("vessel.id"), nullable=False)
    vessel = relationship("BattlefieldEntity", back_populates="weapons")


class GameDao:

    def __init__(self):
        Base.metadata.create_all()
        self.db_session = Session()

    def create_game(self, game: Game) -> int:
        game_entity = map_to_game_entity(game)
        self.db_session.add(game_entity)
        self.db_session.commit()
        return game_entity.id

    def find_game(self, game_id: int) -> Game:
        stmt = select(GameEntity).where(GameEntity.id == game_id)
        game_entity = self.db_session.scalars(stmt).one()
        return map_to_game(game_entity)

    def map_to_game_entity(game: Game) -> GameEntity:
        game_entity = GameEntity()
        # in case there were no players in the data base
        try:
            game_entity.players = game.players
        except:
            pass
        return game_entity

    def map_to_game(game_entity: GameEntity) -> Game:
        game = Game(GameEntity.id)
        return game


class PlayerDao:
    def map_to_player_entity(player: Player) -> PlayerEntity:
        player_entity = PlayerEntity()
        player_entity.name = player.name
        player_entity.battle_field = player.battle_field
        return GameEntity

    def map_to_player(player_entity: PlayerEntity) -> Player:
        player = Player(player_entity.name, player_entity.battle_field)
        player.id = (player_entity.id)
        return player

    def __init__(self):
        Base.metadata.create_all()
        self.db_session = Session()

    def create_player(self, player: Player) -> int:
        player_entity = map_to_player(Player)
        self.db_session.add(player_entity)
        self.db_session.commit()
        return player_entity.id

    def find_player(self, player_id: int) -> Player:
        stmt = select(PlayerEntity).where(PlayerEntity.id == player_id)
        player_entity = self.db_session.scalars(stmt).one()
        return map_to_player(player_entity)


class VesselDao:
    def map_to_vessel_entity(vessel: Vessel, type) -> VesselEntity:
        vessel_entity = VesselEntity()
        vessel_entity.coordinates = (VesselEntity.coord_x, VesselEntity.coord_y, VesselEntity.coord_z)
        vessel_entity.hits_to_be_destroyed = vessel.max_hits
        vessel_entity.weapon = vessel.weapon
        vessel_entity.type = type

        return vessel_entity

    def map_to_vessel(vessel_entity: VesselEntity, type) -> Vessel:
        vessel = Vessel((vessel_entity.coord_x, vessel_entity.coord_y, vessel_entity.coord_z),
                        vessel_entity.hits_to_be_destroyed, vessel_entity.weapon)
        vessel.id = (vessel_entity.id)
        return vessel

    def __init__(self):
        Base.metadata.create_all()
        self.db_session = Session()

    def create_vessel(self, vessel: Vessel) -> int:
        vessel_entity = map_to_vessel(vessel)
        self.db_session.add(vessel_entity)
        self.db_session.commit()
        return vessel_entity.id

    def find_vessel(self, vessel_id: int) -> Vessel:
        stmt = select(VesselEntity).where(Vessel.id == vessel_id)
        vessel_entity = self.db_session.scalars(stmt).one()
        return map_to_vessel(vessel_entity)
