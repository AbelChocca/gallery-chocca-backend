from abc import ABC, abstractmethod

class SlugRepository(ABC):
    @abstractmethod
    def generate(self, value: str) -> str:
        """
        Generate the slug's value of the value prop
        
        :param self: Default
        :param value: Value to slugify
        :type value: str
        :return: The slug's value of the string prop
        :rtype: str
        """
        pass