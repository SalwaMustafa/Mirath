from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from controllers import UploadDataController
from scheme import DoUpload



upload_data_router = APIRouter() 

@upload_data_router.post("/upload/papers")
async def upload_researches(request: Request, do_upload: DoUpload):
    
    db_client = request.app.db_client
    file =  do_upload.file
    survey = do_upload.survey

    upload_data_controller = UploadDataController(file = file, db_client = db_client, survey = survey)

    counter, message = await upload_data_controller.upload_data()

    if counter==0 :
        return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        "signal": message
                    }
                )
    else:
         return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "signal": message
                    }
                )