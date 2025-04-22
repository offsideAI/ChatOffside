import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Response, Query, UploadFile, File 
import database, models
# from sqlalchemy.orm import Session
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
import oauth2
import openai
import base64
import re



router = APIRouter(
    tags = ['offsidei']
)

###############################################################################
## OpenAI

@router.get('/offsideai/jsonfunctioncalling')
def dojsonfunctioncalling(
    *,
    session: Session = Depends(database.get_session),
    current_user: models.User = Depends(oauth2.get_current_user),
    query: str = Query(..., description="The content to send to the OpenAI model")
):
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages = [
            {
                "role": "system",
                "content": "Generate JSON response"   
            },
            {
                "role": "user",
                "content": query
                
            }
        ],
        response_format={ "type": "json_object" }
    )
    return response.choices[0].message.content

@router.get('/offsideai/functioncalling')
def dofunctioncalling(
    *,
    session: Session = Depends(database.get_session),
    current_user: models.User = Depends(oauth2.get_current_user),
    query: str = Query(..., description="The content to send to the OffsideAI model")
):
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages = [
            {
                "role": "system",
                "content": "Generate regular response"   
            },
            {
                "role": "user",
                "content": query
                
            }
        ]
    )
    return response.choices[0].message.content

@router.post('/offsideai/vision')
async def dovisionmagic(
    *,
    # session: Session = Depends(database.get_session),
    # current_user: models.User = Depends(oauth2.get_current_user),
    # query: str = Query(..., description="The content to send to the OffsideAI model"),
    image: UploadFile = File(..., description="Image file to be processed")
    
):
    client = openai.OpenAI()
    
    # Read the image file and convert it to BASE64
    image_content = await image.read()
    base64_image = base64.b64encode(image_content).decode('utf-8')
    query: str = "What's in this image?"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages = [
            {
                "role": "user",
                "content": [
                    {
                     "type": "text",
                     "text": query 
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        } 
                    }
                ]
            }
        ],
        max_tokens = 300
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content


@router.get('/offsideai/urlvision')
async def dourlvisionmagic(
    *,
    # session: Session = Depends(database.get_session),
    # current_user: models.User = Depends(oauth2.get_current_user),
    # query: str = Query(..., description="The content to send to the OffsideAI model"),
    imageurl: str = Query(..., description="The url of the file")
    
):
    client = openai.OpenAI()
    
    # Read the image file and convert it to BASE64
    query: str = "What's in this image?"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages = [
            {
                "role": "user",
                "content": [
                    {
                     "type": "text",
                     "text": query 
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": imageurl
                        } 
                    }
                ]
            }
        ],
        max_tokens = 300
    )
    response_string: str = re.sub("\s+", " ", response.choices[0].message.content)
    print(response_string)
    return response_string 
    # print(response.choices[0].message.content)
    # return response.choices[0].message.content

@router.get('/offsideai/docvision')
async def dodocumentmagic(
    *,
    # session: Session = Depends(database.get_session),
    # current_user: models.User = Depends(oauth2.get_current_user),
    # query: str = Query(..., description="The content to send to the OffsideAI model"),
    imageurl: str = Query(..., description="The url of the file")
    
):
    client = openai.OpenAI()
    
    # Read the image file and convert it to BASE64
    query: str = "Can you take the contents of this image and explain all the details and also interpret and summarize the information and suggest steps?"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages = [
            {
                "role": "user",
                "content": [
                    {
                     "type": "text",
                     "text": query 
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": imageurl
                        } 
                    }
                ]
            }
        ],
        max_tokens = 400
    )
    response_string: str = re.sub("\s+", " ", response.choices[0].message.content)
    response_string = replace_patterns(response_string)
    print(response_string)
    return response_string 

@router.get('/offsideai/visioncounter')
async def dovisioncountermagic(
    *,
    # session: Session = Depends(database.get_session),
    # current_user: models.User = Depends(oauth2.get_current_user),
    # query: str = Query(..., description="The content to send to the OffsideAI model"),
    imageurl: str = Query(..., description="The url of the file")
    
):
    client = openai.OpenAI()
    
    # Read the image file and convert it to BASE64
    query: str = "Can you take the contents of this image and count the number of items in the image? Just return the number and the item name"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages = [
            {
                "role": "user",
                "content": [
                    {
                     "type": "text",
                     "text": query 
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": imageurl
                        } 
                    }
                ]
            }
        ],
        max_tokens = 400
    )
    response_string: str = re.sub("\s+", " ", response.choices[0].message.content)
    response_string = replace_patterns(response_string)
    print(response_string)
    return response_string 

@router.get('/offsideai/visionhashtags')
async def dovisionhashtagsmagic(
    *,
    # session: Session = Depends(database.get_session),
    # current_user: models.User = Depends(oauth2.get_current_user),
    # query: str = Query(..., description="The content to send to the OffsideAI model"),
    imageurl: str = Query(..., description="The url of the file")
    
):
    client = openai.OpenAI()
    
    # Read the image file and convert it to BASE64
    query: str = "Can you take the contents of this image and generate a list of 15 relevant hashtags. Focus on capturing the key themes and elements present in the image. Ensure the hashtags are suitable for use on social media platforms like Instagram and Twitter, emphasizing salient items in the image. Present the hashtags in a clear, space-seperated list, with no numbering. "
    response = client.chat.completions.create(
        model="gpt-4o",
        messages = [
            {
                "role": "user",
                "content": [
                    {
                     "type": "text",
                     "text": query 
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": imageurl
                        } 
                    }
                ]
            }
        ],
        max_tokens = 400
    )
    response_string: str = re.sub("\s+", " ", response.choices[0].message.content)
    response_string = replace_patterns(response_string)
    print(response_string)
    return response_string 





@router.get('/offsideai/assistant')
async def doassistantmagic(
    *,
    # session: Session = Depends(database.get_session),
    # current_user: models.User = Depends(oauth2.get_current_user),
    query: str = Query(..., description="The content to send to the OffsideAI model"),
    # imageurl: str = Query(..., description="The url of the file")
    
):
    client = openai.OpenAI()
    assistant = client.beta.assistants.create(
        name = "Bestie"
    )


def replace_patterns(text):
    # Pattern for **<string>**
    pattern1 = r"\*\*<([^>]*)>\*\*"
    replacement1 = r"<\1> Section"

    # Pattern for ###
    pattern2 = r"###"
    replacement2 = "..."

    # Perform replacements
    text = re.sub(pattern1, replacement1, text)
    text = re.sub(pattern2, replacement2, text)

    return text