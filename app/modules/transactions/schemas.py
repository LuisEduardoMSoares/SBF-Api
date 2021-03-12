from enum import Enum


class TransactionTypeEnum(Enum):
    incoming = 'ENTRADA'
    outgoing = 'SAIDA'