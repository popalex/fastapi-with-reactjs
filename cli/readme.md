# Run Mongo Atlas Local:

```shell
docker run -p 27017:27017 mongodb/mongodb-atlas-local
```

# Run MongoSH

```shell
docker run --rm -it rtsp/mongosh mongosh -- mongodb://172.17.0.1:27017
```

# MongoSH commands

```js
use databae_name
db.database_name.items.find().limit(1)
```