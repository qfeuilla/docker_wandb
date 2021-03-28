to build the docker enter this commands :
```
sudo docker build -t test .
```
and to run :
```
sudo docker run --env WANDB_API_KEY=<WANDB_KEY> test
```
and replace <WANDB_KEY> by your wandb api key
