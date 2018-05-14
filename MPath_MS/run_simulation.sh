MODEL_NAME=$1
COLLECTION_NAME=$2

echo "running simulation $MODEL_NAME"
cd compiled_models
./$MODEL_NAME $COLLECTION_NAME