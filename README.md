# LEGO
AID: Automatic API Identification from Smart Home Device SDKs via Dataflow-enhanced Call Graph Analysis

This repository is dedicated to sharing the tool AID and the data for the Internetware 2025 paper entitled AID: Automatic API Identification from Smart Home Device SDKs via Dataflow-enhanced Call Graph Analysis.

## Getting AID to run

Prerequisites:
* Python >= 3.8

Project structure:
* AID: source codes of AID
* pycg: source codes of PyCG
* SDK_dataset: dataset of 50 SDKs
* micro-benchmark: 123 Python programs of 18 categories
* RQ1-2: evaluation of RQ1 and RQ2
* RQ3: evaluation of RQ3

AID usage:

```bash
$ python AID/__main__.py [module_path1 module_path2 module_path3...] [-o output_path]
# [module_path1, module_path2, ...] represents a list of paths to Python files, which can include any number of paths.
# The generated call relations are stored in a JSON file at the path specified by output_path.
```

*Example :* analyze SDK_dataset/broadlink/light.py.

```bash
$ python AID/__main__.py SDK_dataset/broadlink/light.py -o cg.json
```

The identified SDK APIs are printed out:

```
API number:4
SDK_dataset\broadlink\light.lb2.set_state
SDK_dataset\broadlink\light.lb2.get_state
SDK_dataset\broadlink\light.lb1.get_state
SDK_dataset\broadlink\light.lb1.set_state
```

## Evaluation 

### RQ1 and RQ2 Evaluation

Run AID and AID-PyCG to identify APIs from 50 SDKs in **SDK_dataset**.

```bash
# 1. run the script of testing AID
$ python RQ1-2/DECG_run.py
# 2. run the script of testing AID-PyCG
$ python RQ1-2/PyCG_run.py     
```

The output results of AID are stored in **RQ1-2/DECG_results**, and the output results of AID-PyCG are also stored in **RQ1-2/PyCG_results**.

The format of the results is as follows:
```
API number:9
SDK_dataset\aiohue\v2\controllers\lights.LightsController.set_color
SDK_dataset\aiohue\v2\controllers\lights.LightsController.set_color_temperature
SDK_dataset\aiohue\v2\controllers\lights.LightsController.turn_off
SDK_dataset\aiohue\v2\controllers\lights.LightsController.set_flash
SDK_dataset\aiohue\v2\controllers\lights.LightsController.set_brightness
SDK_dataset\aiohue\v2\controllers\base.BaseResourcesController.create
SDK_dataset\aiohue\v2\controllers\devices.DevicesController.set_identify
SDK_dataset\aiohue\v2\controllers\lights.LightsController.turn_on
SDK_dataset\aiohue\v2\__init__.HueBridgeV2.get_diagnostics
```

The ground truth of the SDK API is recorded in **RQ1-2/ground_truth**, which includes both control APIs and status query APIs.


```
Control APIs:
1.SDK_dataset\aiohue\v2\controllers\lights.LightsController.turn_on
2.SDK_dataset\aiohue\v2\controllers\lights.LightsController.turn_off
3.SDK_dataset\aiohue\v2\controllers\lights.LightsController.set_brightness
4.SDK_dataset\aiohue\v2\controllers\lights.LightsController.set_color
5.SDK_dataset\aiohue\v2\controllers\lights.LightsController.set_color_temperature
6.SDK_dataset\aiohue\v2\controllers\lights.LightsController.set_flash

Status query APIs:
1.SDK_dataset\aiohue\v2\models\light.Light.is_on
2.SDK_dataset\aiohue\v2\models\light.Light.brightness    
```

The precision and recall of two approaches can be calculated by comparing their identification results with the ground truth.


### RQ3 Evaluation

Run 18 categories of programs in **micro-benchmark** to evaluate the accuracy of call graph generation.

It is important to note that except for testing the category *dataflow*, the testing of the other 17 categories requires commenting out lines 256-258 in **AID\AID.py**, i.e., the following code:

```
dataflow.get_all_methods()
dataflow.get_assign()
dataflow.get_return()
```

*Example1:* test 4 programs in category *dataflow*.

```bash
$ python RQ3/dataflows_test.py     
```

*Example2:* test 6 programs in category *args*.

```bash
$ python RQ3/args_test.py     
```


The accuracy results of DECG and PyCG are printed out in the following format:

```bash
Testing: micro-benchmark\dataflows\new
DECG Accuracy: 4/4
PyCG Accuracy: 0/4
```

