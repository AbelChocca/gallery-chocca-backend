
from app.schemas.schema_admin import RegisterAdmin, LoginAdmin

from httpx import AsyncClient
from fastapi import status

async def test_register_admin(client: AsyncClient):
    """
    ## Test para registrar un administrador con exito.

    Parametros
    ----------
    - client -> cliente de prueba para ejecutar el test.
    - session -> session temporal que añadira al admin a la base de datos temporal

    Retorno
    -------
    - status_code -> HTTP_201_CREATED
    """

    # Preparacion de objetos

    admin = RegisterAdmin(
        nombre='AbelMatias',
        email='abelchocca3838@gmail.com',
        password='ElverdaderoGoat',
    )

    # Ejecucion del test
    response = await client.post('/admin/registro', json=admin.model_dump())

    # Verificacion
    assert response.status_code == status.HTTP_201_CREATED

async def test_registrar_admin_duplicado(client: AsyncClient):
    """
    ## Testeo para comprobar la exepcion de la base de datos al crear dos admins con el mismo email.

    Parametros
    ----------
    - client -> cliente de prueba para ejecutar el test.
    - session -> session temporal que añadira al admin a la base de datos temporal

    Retorna
    -------
    - status_code -> HTTP_400_BAD_REQUEST
    """

    # Preparacion de datos:

    admin_1 = RegisterAdmin(
        nombre='Yolo',
        email='yolo@gmail.com',
        password='yoloelmejor',
    )

    admin_2 =RegisterAdmin(
        nombre='Yolo2Xd',
        email='yolo@gmail.com',
        password='yoloelmejor'
    )

    # Ejecucion del primer test

    response_admin_1 = await client.post(url='/admin/registro', json=admin_1.model_dump())

    # Verificacion del primer test

    assert response_admin_1.status_code == status.HTTP_201_CREATED

    # Ejecucion del segundo test

    response_admin_2 = await client.post(url='/admin/registro', json=admin_2.model_dump())

    # Verificacion del segundo test
    assert response_admin_2.status_code == status.HTTP_400_BAD_REQUEST
    assert response_admin_2.json()['detail'] == 'Email duplicado.'

async def test_registrar_logear_admin(client: AsyncClient):
    """
    ## Test para registrar y logear al usuario con respuesta exitosa.

    Parametros
    ----------
    - client -> cliente de prueba para ejecutar el test.
    - session -> session temporal que añadira al admin a la base de datos temporal

    Retorna
    -------
    - status_code -> HTTP_201_CREATED
    - status_code -> HTTP_200_OK
    """
    
    # Preparacion de datos

    admin_registrado = RegisterAdmin(
        nombre='AdminXd',
        email='chocos28@gmail.com',
        password='AbelChocca'
    )

    # Ejecucion del registrado

    response_register = await client.post(url='/admin/registro', json=admin_registrado.model_dump())

    # Verificacion del response
    assert response_register.status_code == status.HTTP_201_CREATED

    # Preparacion de datos para el login
    user_logeado = LoginAdmin(
        email='chocos28@gmail.com',
        password='AbelChocca'
    )

    # Ejecucion del test para logearse

    response_loging = await client.post(url='/admin/login', json=user_logeado.model_dump())

    # Verificacion del response_loging

    assert response_loging.status_code == status.HTTP_200_OK