A basic question answering system 

# simple_answering_system
To run mcp server locally - python .\mcp_server\mcp_server.py
To run api locally - python -m simple_answer_system.src.app

Deploy mcp server
To push to container registry
1) docker compose up --build
2) az acr login --name $ACR_NAME
3) docker tag $IMAGE_NAME $ACR_NAME.azurecr.io/$IMAGE_NAME:$TAG
4) docker push $ACR_NAME.azurecr.io/$IMAGE_NAME:$TAG