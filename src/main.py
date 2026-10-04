from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, field_validator
from predict import predict_data
from typing import List


app = FastAPI()

class DigitsData(BaseModel):
    """
    Pydantic BaseModel representing iris flower measurements.

    Attributes:
        pixels (List[float]): 64 pixel values (flattened 8x8 image),
            each between 0 and 16, in row-major order.
    """
    pixels: List[float]
    
    @field_validator("pixels")
    @classmethod
    def validate_pixels(cls, value):
        if len(value)!=64:
            raise ValueError(f"Expected 64 pixels, got {len(value)}")
        if any(p<0 or p>16 for p in value):
            raise ValueError(f"Pixel value should be between 0 and 16")
        return value
    

class DigitsResponse(BaseModel):
    response:int



"""Modern web apps use a technique named routing. This helps the user remember the URLs. 
For instance, instead of having /booking.php they see /booking/. Instead of /account.asp?id=1234/ 
they’d see /account/1234/."""

@app.get("/", status_code=status.HTTP_200_OK)
async def health_ping():
    """Concurrent (multiple tasks can run simultaneously)"""
    return {"status": "healthy"}

@app.post("/predict", response_model=DigitsResponse)
async def predict_digit(digits_features: DigitsData):
    """
    Predict which digit (0-9) an 8x8 image represents.
    This endpoint accepts the flattened pixel values of a handwritten digit
    image and returns the predicted digit class.
    Args:
        digits_features (DigitsData): A DigitsData object containing:
            - pixels (List[float]): 64 pixel values (flattened 8x8 image in
              row-major order), each between 0 and 16
    Returns:
        DigitsResponse: A response object containing:
            - response (int): The predicted digit (0 to 9)
    Raises:
        HTTPException: Returns a 500 status code with error details if prediction fails.
        (FastAPI automatically returns a 422 if pixels does not contain exactly
        64 values or any value is outside 0-16.)
    Example:
        POST /predict
        {
            "pixels": [0, 0, 5, 13, 9, 1, 0, 0, ... 64 values total]
        }
        Response:
        {
            "response": 0
        }
    """
    try:
        features = [digits_features.pixels]

        prediction = predict_data(features)
        return DigitsResponse(response=int(prediction[0]))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


    
