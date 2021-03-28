to build the docker enter this commands :
```
sudo docker build --build-arg wandb_key=<WANDB_KEY> -t test .
```
and replace <WANDB_KEY> by your wandb api key

and to run :
```
sudo docker run test
```
