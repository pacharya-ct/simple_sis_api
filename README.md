# simple_sis_api
## Simple python client for SIS Web Services API

A simple wrapper to send a request to a SIS webservice endpoint and return a list of python dictionaries

1. Reads the token file, builds the correct auth header.
2. Accepts filter options and sends request(s) to the SIS web service endpoint and fetches data across all the pages.
3. Extracts information from the JsonAPI document. Reads the "data" and "included" sections and flattens it into a python dictionary.
4. Runs client side filters and custom sorts defined by user.
5. Returns a list of python dictionaries.

## About the library
* The base class does bulk of the work. 
* Use subclasses to define values for endpointurl and allowed filters

## Using the library
Do a local build and install it. First activate your virtualenv if using it. Then in project root run:

`python3 -m pip install -e .`

Save your sis api token to a file and put in path to the token in the ini file (examples/sis_api.ini)

## Examples
* View example1.py for function based examples
* View example2.py for object oriented examples

To run example s1 with data from the sistest instance

`python3 examples/example1.py examples/sis_api.ini test s1`

OR

`python3 examples/example2.py examples/sis_api.ini test s1`

## Testing
Tests are located in simple_sis_api/simple_sis_api/tests. To run them, use 

`python3 -m pytest`
