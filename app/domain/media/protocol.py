from app.domain.media.dto import MediaImageDTO

from typing import BinaryIO, Protocol

class MediaProtocol(Protocol):
    def upload_image(self, file: BinaryIO, folder: str) -> MediaImageDTO:
        """
        Method for upload image to cloudinary service
        
        :param self: default
        :param file: the file content of the image
        :type file: BinaryIO
        :param folder: the destinatary folder to upload the image
        :type folder: str
        :return: The image url value and his publid id
        :rtype: MediaImageDTO
        """
        ...

    def delete_image(self, public_id: str) -> None:
        """
        Method to delete an image to the cloudinary service
        
        :param self: default
        :param public_id: the public id of the image to search and delete
        :type public_id: str
        """
        ...