# app.tests.test_productos.py
from app.schemas.schema_product import CreateProduct, CreateColorVariant, UpdateProduct, FilteringSchema

from httpx import AsyncClient
from fastapi import status
from time import time

# Pruebas de Testeo

async def test_get_products_and_cache_response(
    client: AsyncClient,
):
    """
    Testeo para obtener todos los productos del endpointt /products correctamente.

    Parametros
    ----------
    client -> fixture TestClient que provee una session de testeo para toda la aplicación.

    Retorna
    -------
    response -> HTTP_200_OK

    """
    # Rellenamos datos a la base de datos de prueba para consultar productos
    test_product = CreateProduct(
        nombre='Test Performance Product',
        descripcion='Producto para el test de rendimiento',
        categoria='Test',
        marca='Test',
        precio=100.0,
        imagenes_url=['test_image.jpg'],
        variants=[CreateColorVariant(color='azul', tallas=['S', 'M'], imagenes_color=['test.png', 'test2.png'])]
    )
    test_product2 = CreateProduct(
        nombre='Test Product',
        descripcion='Producto para el test 2',
        categoria='Test22',
        marca='Test2',
        precio=110.0,
        imagenes_url=['test_image2.jpg'],
        variants=[CreateColorVariant(color='rojo', tallas=['S', 'M'], imagenes_color=['test4.png', 'test3.png'])]
    )

    response_post = await client.post("/products/", json=test_product.model_dump())
    assert response_post.status_code == status.HTTP_201_CREATED
    product_id = response_post.json()["id"]

    response_post = await client.post('/products/', json=test_product2.model_dump())
    assert response_post.status_code == status.HTTP_201_CREATED

    # 2. Primera consulta (debería ir a la base de datos)
    initial_time_db = time()
    response_db = await client.get("/products/filter")
    tiempo_db = time() - initial_time_db

    assert response_db.status_code == status.HTTP_200_OK
    assert any(p["id"] == product_id for p in response_db.json())

    # 3. Segunda consulta (debería pegar al cache)
    initial_time_cache = time()
    response_cache = await client.get("/products/filter")
    tiempo_cache = time() - initial_time_cache

    assert response_cache.status_code == status.HTTP_200_OK
    assert any(p["id"] == product_id for p in response_cache.json())

    # 4. Verificamos que el cache sea más rápido
    assert tiempo_cache < tiempo_db

async def test_publicar_producto(client: AsyncClient):
    """
    Testeo para publicar un producto del endpoint /products con exito.

    Parametros
    ----------
    client -> fixture TestClient que provee una session de testeo para toda la aplicación.
    mock -> Simulación para reemplazar la dependencia de inyección de get_user_session

    Retorna
    -------
    response -> HTTP_200_OK

    """

    # Prearacion de argumentos
    variants = [
        CreateColorVariant(
            color='Azul',
            tallas=['28', '30'],
            imagenes_color=['imagen23.png', 'imagen04.png']
        ),
        CreateColorVariant(
            color='Plomo',
            tallas=['30', '32'],
            imagenes_color=['imagen8342.png', 'imagen342.png']
        )
    ]

    product = CreateProduct(
        nombre='Jean BGO',
        descripcion='Pitillo, suave, tela de calidad.',
        categoria='Pantalon',
        marca='BGO',
        precio=170.0,
        imagenes_url=['image2.png', 'image3.png'],
        etiquetas=['pitillo', 'BGO'],
        variants=variants
    )

    # Ejecución del test
    response = await client.post(
        '/products/', 
        json=product.model_dump(), # Serializamos modelo pydantic en diccionarioo json
        )

    # Verificación del test
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['nombre'] == 'Jean BGO'

async def test_faltan_variantes(client: AsyncClient):
    """
    Test para probar el salto de exepcion ya que faltan variantes a nuestros productos.

    Parametros
    ----------
    client -> Cliente que provee una session TestClient en nuestra app.
    mocker -> Mocker para reemaplazar la session

    Retorna
    -------
    response -> HTTP__400_BAD_REQUEST
    """


    # Preparación de datos
    variants = []

    product = CreateProduct(
        nombre='Jean BGO',
        descripcion='El mejor jean',
        categoria='Pantalon',
        marca='BGO',
        precio='160.0',
        imagenes_url=['image23.png'],
        etiquetas=['hola', 'xd'],
        variants=variants
    )

    # Ejecución
    response = await client.post(
        '/products/', 
        json=product.model_dump()
        )

    # Verificación
    assert response.status_code == status.HTTP_400_BAD_REQUEST

async def test_registrar_actualizar_y_no_encontrado_producto(client: AsyncClient):
    """
    ## Test para registrar un producto con exito y actualizarlo con exito.

    Parametros
    ----------
    - client: cliente de prueba para ejecutar el test.

    Retorna
    -------
    - status_code -> HTTP_200_OK
    """

    # Preparar items para registrar y actualizar

    ## Para registrar
    created_variants = [
    CreateColorVariant(
        color='Azul',
        tallas=['28', '30', '32'],
        imagenes_color=['image32.png', 'image843.png']
    ),
    CreateColorVariant(
        color='Plomo',
        tallas=['30', '32', '34'],
        imagenes_color=['image433.png', 'image423.png']
    )
    ]

    created_product = CreateProduct(
        nombre='Jean Bgo Pitillo',
        descripcion='El mejor jean de todos',
        categoria='Pantalon',
        marca='BGO',
        precio=150,
        imagenes_url=['image32.png', 'image843.png'],
        etiquetas=['bgo', 'elmejor', 'azul'],
        variants=created_variants
    )

    # Para actualizar
    update_product = UpdateProduct(
        nombre='Jean BGOº Pitillo Drill'
    )


    # Ejecutar el registro del producto
    response_created = await client.post(url='/products/', json=created_product.model_dump())

    # Verificar el registro del producto
    assert response_created.status_code == status.HTTP_201_CREATED

    # Obtener id del registro
    product_id = response_created.json()['id']
    producto_diccionario = update_product.model_dump(exclude_unset=True)

    # Ejecutar la actualizacion del proyecto
    response_update = await client.patch(url=f'/products/{product_id}', json=producto_diccionario)

    # Verificar la actualizacion del producto
    assert response_update.status_code == status.HTTP_200_OK
    assert response_update.json()['nombre'] == 'Jean BGOº Pitillo Drill'

    # Hacemos un test para ejecutar el exito del error HTTP_404_NOT_FOUND (no encontrado)

    response_no_encontrado = await client.patch(url=f'/products/{99}', json=producto_diccionario)

    # Verificar
    assert response_no_encontrado.status_code == status.HTTP_404_NOT_FOUND

async def test_post_products_and_get_filtering(client: AsyncClient):
    """
    Creating two products and use filtering schema to get one of these that achieve the filters

    ## Args
    - client [AsyncClient] -> principal's client of the tests

    ## Return
    - asserts status.HTTP_200_OK
    """

    # Preparing the product's models
    product_test_1 = CreateProduct(
        nombre='test2',
        descripcion='test24',
        categoria='jean',
        marca='43tde',
        precio=200.4,
        imagenes_url=['342ife.png', 'feir2.png'],
        etiquetas=['43242c', '34cj3x3'],
        variants=[
            CreateColorVariant(
                color='blue',
                tallas=['S', 'XL'],
                imagenes_color=['39sidis.png', 'olooteest.png']
            )
        ]
    )

    product_test_2 = CreateProduct(
        nombre='test43',
        descripcion='tes554t24',
        categoria='jean',
        marca='43td43e',
        precio=203.4,
        imagenes_url=['34242ife.png', 'feir2423.png'],
        etiquetas=['43242342c', '34c423j3x3'],
        variants=[
            CreateColorVariant(
                color='red',
                tallas=['S', 'XL'],
                imagenes_color=['39sidis.png', 'olooteest.png']
            )
        ]
    )

    filtering_schema = FilteringSchema(
        category='jean',
        color='blue'
    )

    # calls to api
    response = await client.post('/products/', json=product_test_1.model_dump())
    
    # assert 1
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['nombre'] == 'test2'

    # call two 
    response2 = await client.post('/products/', json=product_test_2.model_dump())

    # assert 2
    assert response2.status_code == status.HTTP_201_CREATED
    assert response2.json()['nombre'] == 'test43'

    # call three
    response_products = await client.get('/products/filter', params=filtering_schema.model_dump())

    assert response_products.status_code == status.HTTP_200_OK
    assert response_products.json()[0]['nombre'] == 'test2'

    # 🔥 Extra case: filter by non-existent color
    non_existent_filter = FilteringSchema(
        category='jean',
        color='green'
    )
    response_empty = await client.get('/products/filter', params=non_existent_filter.model_dump())
    assert response_empty.status_code == status.HTTP_200_OK
    assert response_empty.json() == []

async def test_post_products_patch_product(client: AsyncClient):
    """
    Post two products and then get these with filter of descount

    Args
    - client [AsyncClient] -> principal's client of the tests
    """

    # Prepare principal products

    product_1 = CreateProduct(
        nombre='Test33',
        descripcion='test9953',
        categoria='Pantalones',
        marca='test4',
        precio=175.00,
        descuento=20,
        promocion=True,
        imagenes_url=['test553'],
        variants=[
            CreateColorVariant(
                color='test43',
                tallas=['X', 'XS'],
                imagenes_color=['OLO.png']
            )
            ]
    )
    product_2 = CreateProduct(
        nombre='Test3343',
        descripcion='test9954323',
        categoria='Pantalones',
        marca='test443',
        precio=179.00,
        descuento=0.00,
        promocion=False,
        imagenes_url=['test55433'],
        variants=[
            CreateColorVariant(
                color='test43243',
                tallas=['X', 'XS', 'S'],
                imagenes_color=['OLO432.png']
            )
            ]
    )

    # Post products
    response_1 = await client.post('/products/', json=product_1.model_dump())
    assert response_1.status_code == status.HTTP_201_CREATED
    assert response_1.json()['nombre'] == 'Test33'
    assert response_1.json()['promocion'] == True

    response_2 = await client.post('/products/', json=product_2.model_dump())
    assert response_2.status_code == status.HTTP_201_CREATED
    assert response_2.json()['nombre'] == 'Test3343'
    assert response_2.json()['id'] == 2

    # Prepare filter schema
    filters = FilteringSchema(
        promocion=True
    )

    # Call products with filter schema
    response_products = await client.get('/products/filter', params=filters.model_dump())
    assert response_products.status_code == status.HTTP_200_OK
    print("Response JSON:", response_products.json())
    assert response_products.json()[0]['nombre'] == 'Test33'
    assert len(response_products.json()) == 1

    # Let's patch the second product
    new_product_2 = UpdateProduct(
        promocion=True
    )

    response_patch = await client.patch(f'/products/{2}', json=new_product_2.model_dump(exclude_unset=True))
    assert response_patch.status_code == status.HTTP_200_OK
    assert response_patch.json()['promocion'] == True

async def test_post_and_delete_product(client: AsyncClient):
    """
    Post an product and then delete it

    Args
    - client -> AsyncClient
    """
    
    product_test = CreateProduct(
        nombre='producttest',
        descripcion='prouctsd343',
        categoria='test32',
        marca='3ds434',
        precio=92.4,
        descuento=20,
        promocion=True,
        imagenes_url=['idusex.png'],
        etiquetas=['iisdj34', 'ms43s'],
        variants=[
            CreateColorVariant(
                color='test',
                tallas=['X', 'S'],
                imagenes_color=['isfer3.png', '345943.png']
            )
            ]
    )

    response_1 = await client.post('/products/', json=product_test.model_dump())
    assert response_1.status_code == status.HTTP_201_CREATED
    
    delete_response = await client.delete(f'products/{1}')
    assert delete_response.status_code == status.HTTP_202_ACCEPTED
