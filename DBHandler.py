from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Double, create_engine

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship, sessionmaker


Base = declarative_base()

class Core_Invoice_Item_Status(Base):
    __tablename__ = 'core_invoice_item_status'

    id = Column(Integer, primary_key=True)
    label = Column(String(64), nullable=False)

class Core_Invoice(Base):
    number = Column(Integer, autoincrement="auto", primary_key=True)
    issued = Column(Date, nullable=False)
    due = Column(Date, nullable=False)
    payer_id = Column(Integer, ForeignKey('core_payer.id'))
    status = Column(String(20), nullable=False)
    access_code = Column(String(16), nullable=False)
    filename = Column(String(256), nullable=True)
    Note = Column(Text, nullable=True)

class Core_Invoice_Item(Base):
    __tablename__ = 'core_invoice_item'

    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey('core_invoice.id'))
    service_id = Column(Integer, ForeignKey('core_service.id'))
    quantity = Column(Double)

engine = create_engine('sqlite:///test.db', echo=True)
Base.metadata.create_all(engine)

session = sessionmaker(bind=engine)()