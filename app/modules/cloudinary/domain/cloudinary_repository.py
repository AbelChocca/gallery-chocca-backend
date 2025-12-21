from abc import ABC, abstractmethod
from app.modules.cloudinary.domain.dto import CloudinaryImageDTO

from typing import BinaryIO

class CloudinaryRepository(ABC):
    @abstractmethod
    def upload_image(self, file: BinaryIO, folder: str) -> CloudinaryImageDTO:
        """
        Method for upload image to cloudinary service
        
        :param self: default
        :param file: the file content of the image
        :type file: BinaryIO
        :param folder: the destinatary folder to upload the image
        :type folder: str
        :return: The image url value and his publid id
        :rtype: CloudinaryImageDTO
        """
        pass

    @abstractmethod
    def delete_image(self, public_id: str) -> None:
        """
        Method to delete an image to the cloudinary service
        
        :param self: default
        :param public_id: the public id of the image to search and delete
        :type public_id: str
        """
        pass