MODEL_NAME=$1

echo "compiling model $MODEL_NAME"
cd PMGBP
make clean
make all

echo "moving model to final destintation:"
echo "MPath_MS/compiled_models/$MODEL_NAME"
echo "MPath_MS/models_parameters/$MODEL_NAME.xml"

mv bin/model ../compiled_models/$MODEL_NAME
mv parameters.xml ../model_parameters/$MODEL_NAME.xml