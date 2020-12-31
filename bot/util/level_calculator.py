from typing import List
from discord import User, Message


class LevelCalculator:

    @staticmethod
    def calculate_next_level(level: int) -> int:
        """
        Calculates xp needed for next level and return it
        """
        return 500 * (level ^ 2) - (500 * level)

    @staticmethod
    def is_spam(user: User, history: List[Message]) -> bool:
        for msg in history:
            if user.id != msg.author.id:
                return False
        return True

    @classmethod
    def calculate_text_xp(cls, msg: Message, history: List[Message]) -> int:
        xp = 20

        if not cls.is_spam(history):
            for prev_msg in history:
                space_between = msg.created_at.timestamp() - prev_msg.created_at.timestamp()

                if space_between < 60:
                    if prev_msg.author.id != msg.user.id:
                        xp += 2
                else:
                    break
        else:
            xp = 0

        return xp