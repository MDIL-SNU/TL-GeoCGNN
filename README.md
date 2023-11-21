# Melting-point-prediction
This repository includes followings:
```
- Modified python code of GeoCGNN (process_geo_CGNN.py)
- Example inputs for running (database/cif/, database/npz/, database/targets_melting.csv, database/orthogonal_array.csv)
- Database used for training model (database/targets_atomization.csv, database/forumla_CAS.csv)
```

## Installation
First, install GeoCGNN provided in https://github.com/Tinystormjojo/geo-CGNN  
Then, change `process_geo_CGNN.py` with the one in this repository.

## Running the code
The basic method of running GeoCGNN is already well described in https://github.com/Tinystormjojo/geo-CGNN  
Major difference of the code is
- It can now selectively freeze the layers of `embedding` and `gated convolution`.
- It can apply different learning rate in `embedding`, `gated convolution` and `output block`.  
(More details about each part of the model can be found in [1])

## Reference
[1] (https://doi.org/10.1038/s43246-021-00194-3) GeoCGNN
