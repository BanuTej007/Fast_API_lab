## Setting up the lab

1. Create a virtual environment(e.g. **fastapi_lab1_env**).
2. Activate the environment and install the required packages using `pip install -r requirements.txt`.

### Project structure

```
mlops_labs
└── fastapi_lab1
    ├── assets/
    ├── fastapi_lab1_env/
    ├── model/
    │   └── digits_model.pkl
    ├── src/
    │   ├── __init__.py
    │   ├── data.py
    │   ├── main.py
    │   ├── predict.py
    │   └── train.py
    ├── README.md
    └── requirements.txt
```

Note:
- **fastapi[all]** in **requirements.txt** will install optional additional dependencies for fastapi which contains **uvicorn** too.

## Running the Lab

1. First step is to train a Decision Tree Classifier(model/digits_model,pkl). To do this, move into **src/** folder with
    ```bash
    cd src
    ```
2. To train the Decision Tree Classifier, run:
    ```bash
    python train.py
    ```
3. To serve the trained model as an API, run:
    ```bash
    uvicorn app:main --reload
    ```
4. Testing endpoints - to view the documentation of your api model you can use [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (or) [http://localhost:8000/docs](http://localhost:8000/docs) after you run you run your FastAPI app.


### FastAPI Syntax

- The instance of FASTAPI class can be defined as:
    ```bash
    app = FastAPI()
     ```
- When you run a FastAPI application, you often pass this app instance to an ASGI server uvicorn. The server then uses the app instance to handle incoming web requests and send responses based on the routes and logic you’ve defined in your FastAPI application.
- To run a FastAPI application, run:
    ```
    uvicorn main:app --reload
    ```
- In this command, **main** is the name of the Python file containing your app instance (without the .py extension), and **app** is the name of the instance itself. The **--reload** flag tells uvicorn to restart the server whenever code changes are detected, which is useful during development and should not be used in production.
- All the functions which should be used as API should be prefixed by **@app.get("/followed_by_endpoint_name")** or **@app.post("/followed_by_endpoint_name")**. This particular syntax is used to define route handlers (which function should handle an incoming request based on the URL and HTTP method), which are the functions responsible for responding to client requests to a given endpoint.
    1. **Decorator (@)**: This symbol is used to define a decorator, which is a way to dynamically add functionality to functions or methods. In FastAPI, decorators are used to associate a function with a particular HTTP method and path.
    2. **App Instance (app)**: This represents an instance of the FastAPI class. It is the core of your application and maintains the list of defined routes, request handlers, and other configurations.
    3. **HTTP Method (get, post, etc.)**: The HTTP method specifies the type of HTTP request the route will respond to. For example, get is used for retrieving data, and post is used for sending data to the server. FastAPI provides a decorator for each standard HTTP method, such as @app.put, @app.delete, @app.patch, and @app.options, allowing you to define handlers for different types of client requests. For detailed info refer to this webiste by [Mdn](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods).
    4. **Path/Endpoint ("/endpoint_name")**: This is the URL path where the API will be accessible. When a client makes a request to this path using the specified HTTP method, FastAPI will execute the associated function and return the response.
- Using **async** in FastAPI allows for non-blocking operations, enabling the server to handle other requests while waiting for I/O tasks, like database queries or model loading, to complete. This leads to improved concurrency and resource utilization, enhancing the application's ability to manage multiple simultaneous requests efficiently.

### Data Models in FastAPI

##### **1. DigitsData class:**

The request body can be represented using a Pydantic model containing the 64 pixel values required by the Digits model.

For example:

class DigitsData(BaseModel):
    pixel_0: float
    pixel_1: float
    pixel_2: float
    # ...
    pixel_63: float

The model receives the 64 pixel values corresponding to the 8 × 8 handwritten digit image.

#### **2. DigitsResponse class:**

The prediction returned by the API can be represented using another Pydantic model:

class DigitsResponse(BaseModel):
    response: int

The DigitsResponse class defines the structure of the response returned by the prediction endpoint.

When:

response_model=DigitsResponse

is specified in a FastAPI route, FastAPI uses the model to:

Serialize the output: Convert the Python response into the expected JSON structure.
Validate the response: Ensure that the returned data follows the specified format.
Document the API: Display the response structure in the automatically generated API documentation.

For example, a successful prediction could return:

{
    "response": 7
}

where 7 is the digit predicted by the Decision Tree Classifier.

### FastAPI features

**1. Request Body Reading**

When a client sends data to a FastAPI endpoint, the request can contain a body, commonly in JSON format.

For example:

{
    "pixel_0": 0,
    "pixel_1": 0,
    "pixel_2": 5,
    "pixel_3": 13
    ...
}

For a prediction request, the complete request contains the 64 pixel values required by the Digits model.

FastAPI automatically reads the request body based on the Content-Type header, which is typically:

application/json

**2. Data Conversion:**

FastAPI uses Pydantic models to parse and validate incoming JSON data.

For example, if a field is declared as:

pixel_0: float

and the client sends:

{
    "pixel_0": "5"
}

Pydantic can convert the value to a floating-point number.

If the value cannot be converted to the expected type, FastAPI returns a validation error.

**3. Data Validation**

Pydantic checks that:

Required fields are present.
Values have the correct data types.
The request follows the structure defined by the Pydantic model.

If validation fails, FastAPI normally returns a:

422 Unprocessable Entity

response containing details about the validation errors.

**4. Error Handling**

FastAPI provides the HTTPException class for explicitly returning HTTP errors.

Example:

from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):

    item = get_item_by_id(item_id)

    if item is None:
        raise HTTPException(
            status_code=404,
            detail=f"Item with ID {item_id} not found"
        )

    return item

In this example, if an item does not exist, FastAPI returns a 404 Not Found response.

The response would look like:

{
    "detail": "Item with ID 1 not found"
}
- For more information on how to handle errors in FASTAPI refer to this [documentation](https://fastapi.tiangolo.com/tutorial/handling-errors/).
