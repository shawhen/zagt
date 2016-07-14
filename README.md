# What's this
This project can be a replacement of tornado+gevent combination.But what it changed is that it can return "Transfer-Encoding: chunk" response, so we can build a comet communication.

# Progress
Now the project is just beginning, many of features should be implemented.

# Supported python versions
Because of the wave of time, currently will just focus on python3.x, but 2.x contribution is absolutely welcome.

# Example
See the examples directory.
## comet
- server: `python3 comet.py`
- client: `curl localhost:8000`
- 
> {"progress": "10%"}
>
> {"progress": "20%"}
>
> {"progress": "30%"}
>
> {"progress": "40%"}
>
> {"progress": "50%"}
>
> {"progress": "60%"}
>
> {"progress": "70%"}
>
> {"progress": "80%"}
>
> {"progress": "90%"}
>
> {"progress": "100%"}

# License
MIT
