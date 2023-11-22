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

To utilize these features, prepare some rows to be tested in `data/orthogonal_array.csv`.  
Please write the name of the module at the first row for each corresponding column.  
Each layer would be frozen if corresponding column is 1, trainable if 0.  
  
Additionally, please add column named `lr` for applying different learning rate.  
Value in this column would be multiplied to original learning rate in `embedding`, `gated convolution`.
Multiple learning rate is implemented for Adam optimizer.
  
For example in 2 gated convolution model,  
|embedding|embedding|conv|conv|MLP_psi2n|MLP_psi2n|lr|
|---|---|---|---|---|---|---|
|1|0|0|1|1|0|0.75|

- First layer of `embedding` module
- `conv` module in second `gated convolution` module
- `MLP_psi2n` module in first `gated convolution` module
would be frozen, while other layers remain trainable and learning rate would be reduced by 0.75 times.

## Reference
[1] : https://doi.org/10.1038/s43246-021-00194-3
