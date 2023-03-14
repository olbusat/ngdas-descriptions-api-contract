# NGC CATALOG DATA MODEL

These files represent how data is stored internally and shared with users of the catalog. They are in YAML format and conform to [JSON Schema](http://json-schema.org/draft-07/schema#).  
The files here are used to generate Swagger documentaion for the Catalog API. If an update is made to these files follow the steps below to apply the changes to swagger.

- Run the python script located in the swagger folder

```sh
    source ../ngc-venv/bin/activate
    cd swagger
    python convert_model_to_swagger.py
```

- This should output a models.js file in the swagger directory.
- Copy this file to the service-layer directory

```sh
    cp models.js ../../service-layer/models/models.js
```
