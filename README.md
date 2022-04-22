# padam
Python Aided Design and Manifacturing


### Activate environment
conda activate cadquery

### Add module to path
ln -s `realpath padam` ~/.conda/envs/cadquery/lib/python3.10/site-packages/padam

### CadQuery server
docker run --rm -d -p 5000:5000 -v ${PWD}/padam:/opt/conda/envs/cq/lib/python3.8/site-packages/padam:ro --name cqs cadquery/cadquery-server
docker logs -f cqs
docker stop cqs
