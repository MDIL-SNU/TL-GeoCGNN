# TL-GeoCGNN
Code and example database for employing transfer learning in GeoCGNN
## Features
This repository includes the following:
  
- Modified python code of GeoCGNN model
  - process_geo_CGNN.py
- Pre-trained model
  - pre_trained/pre_trained_model.pth
- Example inputs
  - Crystal structure: database/cif
  - Crystal graph: database/npz
  - Target property: database/targets_melting.csv
  - Orthogonal array for the Taguchi method: database/orthogonal_array.csv
- Database used for training model
  - Pre-training features: database/targets_atomization.csv
  - Target materials list: database/forumla_CAS.csv
- Utils for updating the atomization energy database
  - database/update_atomization.py

Note that melting points in `targets_melting.csv` are arbitrary values.

## Installation
1. Install GeoCGNN from https://github.com/Tinystormjojo/geo-CGNN
2. Change `process_geo_CGNN.py` with the one in this repository.

## Usage
### Preparation of inputs
The basic method of running GeoCGNN is described in https://github.com/Tinystormjojo/geo-CGNN  
Key modifications in the code include:
- Selective freezing of `embedding` and `gated convolution` layers
- Application of different learning rates in `embedding`, `gated convolution`, and `output block`.
  
To utilize these features:  
1. Prepare rows to be tested in `data/orthogonal_array.csv`.  
2. Write the names of the modules in the first row for each corresponding column.  
3. Each layer would be frozen if the corresponding column is 1, trainable if 0.
4. Add a column named `lr` for applying different learning rates.
5. Value in this column would be multiplied by the original learning rate in `embedding` and `gated convolution`.
  
For example with a model with two gated convolution layers:  
|embedding|embedding|conv|conv|MLP_psi2n|MLP_psi2n|lr|
|---|---|---|---|---|---|---|
|1|0|0|1|1|0|0.75|

- The first layer of the `embedding` module is frozen.
- The `conv` module in the second `gated convolution` layer is frozen.
- The `MLP_psi2n` module in the first `gated convolution` layer is frozen.
- Other layers remain trainable, but with a learning rate reduced by 0.75 times.

Please provide an appropriate orthogonal array depending on your hyperparameter selection.  
(Note that the second column of embedding corresponds to the activation function, and freezing it is only meaningful when using parametric activations.)

### Running the code
To run TL-GeoCGNN, use the following command.  
```
python process_geo_CGNN.py --n_hidden_feat 192 --n_GCN_feat 192 --cutoff 8 --max_nei 12 --n_MLP_LR 3 --num_epochs 300 --batch_size 3 --target_name melting_point --milestones 250 --gamma 0.1 --test_ratio 0.2 --datafile_name my_graph_data_MP_8_12_100 --database melting --n_grid_K 4 --n_Gaussian 64 --N_block 5 --lr 1e-3 --load_model --pre_trained_model_path pre_trained/pre_trained_model.pth --orthogonal_row 1
```
For argument `--pre_trained_model_path`, the path for the pre-trained model should be provided.  
For argument `--orthogonal_row`, the row number for testing should be provided.

More details about each part of the model can be found in [1]  

## Updating atomization energy
For further updates in the Materials Project[2], updating atomization energy might be necessary.  
To update specific Materials Project id, (e.g. `mp-1234` and `mp-2345`)
```
python update_atomization.py --id mp-1234 mp-2345 --api_key {your API key}
```
  
To update every database,
```
python update_atomization.py --all --api_key {your API key}
```
This would make a new CSV file, `targets_atomization_updated.csv`.

## Reference
[1] : https://doi.org/10.1038/s43246-021-00194-3  
[2] : https://next-gen.materialsproject.org/
