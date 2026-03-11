# Quick Start

To start using Hyperspace, follow these steps:

### 1. Install the Hyperspace API Client

Run the following shell command in your code or your data terminal –

d host address, use the following code to connect to the database through the Hyperspace API.

{% tabs %}
{% tab title="Python" %}
{% code lineNumbers="true" %}

```python
pip install hyperspace-py
```

{% endcode %}
{% endtab %}

{% tab title="JavaScript" %}
{% code lineNumbers="true" %}

```python
npm install https://github.com/hyper-space-io/hyperspace-js
```

{% endcode %}
{% endtab %}
{% endtabs %}

for more information, see [here](https://docs.hyper-space.io/hyperspace-docs/projects/setting-up/installing-the-hyperspace-api-client).

### **2. Create a local instance of the Hyperspace client**&#x20;

Once you receive credentials and host address, use the following code to connect to the database through the Hyperspace API.

{% tabs %}
{% tab title="Python" %}
{% code lineNumbers="true" %}

```python
hyperspace_client = hyperspace.HyperspaceClientApi(host=host_address,
                                                      username=username,
                                                      password=password)
```

{% endcode %}
{% endtab %}

{% tab title="Java" %}
{% code lineNumbers="true" %}

```java
import io.hyperspace.client.HyperspaceClient;
HyperspaceClient client = new HyperspaceClient(host, username, password);
```

{% endcode %}
{% endtab %}

{% tab title="JavaScript" %}
{% code lineNumbers="true" %}

```javascript
const hs = require('hyperspace-js')
const hyperspaceClient = new hs.HyperspaceClient(host, username, password)
```

{% endcode %}
{% endtab %}
{% endtabs %}

### **3. Run Hyperspace queries**

#### **Create a schema file**

The schema files outline the data structure, index and metric types, and similar configurations. More info can be found in the [configuration file](https://docs.hyper-space.io/hyperspace-docs/projects/setting-up/creating-a-database-schema-configuration-file) section.&#x20;

#### **Create a collection**

Copy the following code snippet to create a collection

{% tabs %}
{% tab title="Python" %}
{% code lineNumbers="true" %}

```python
collection_name = 'new_collection'
hyperspace_client.create_collection('schema.json', collection_name)
```

{% endcode %}
{% endtab %}

{% tab title="Java" %}
{% code lineNumbers="true" %}

```java
JsonObject schema = (JsonObject) 
JsonParser.parseReader(new FileReader("schema.json"));
client.createCollection(collectionName, schema);
```

{% endcode %}
{% endtab %}

{% tab title="JavaScript" %}
{% code lineNumbers="true" %}

```javascript
const collection_name = 'new_collection'
await hyperspaceClient.createCollection('schema.json', collection_name)
```

{% endcode %}
{% endtab %}
{% endtabs %}

**Where** –

* '<mark style="color:purple;">schema.json</mark>' – Specifies the path to the configuration file that you created locally on your machine.
* <mark style="color:purple;">collection\_name</mark>' – Specifies the name of the collection to be created in the Hyperspace database.&#x20;

Alternatively, you can define the database config schema as a local python object

{% tabs %}
{% tab title="Python" %}
{% code lineNumbers="true" %}

```python
schema = {
        "configuration": {
            "name": {
                "type": "keyword"
            },
            "id": {
                "type": "keyword",
                "id": True,
            }
        }
    }
hyperspace_client.create_collection(schema, 'collection_name')
```

{% endcode %}
{% endtab %}

{% tab title="Java" %}
{% code lineNumbers="true" %}

```java
String schema = "{" +
                "  \"configuration\": {" +
                "  \"name\": {" +
                "               \"type\":\"keyword\"" +
                "            }" +
                "  \"id\":   {" +
                "               \"type\":\"keyword\"" +
                "               \"id\":\"true\"" +                
                "            }" +    
                "        }" +
                "      }";
                

hyperspaceClient.createCollection(collectionName, schema);
```

{% endcode %}
{% endtab %}

{% tab title="JavaScript" %}
{% code lineNumbers="true" %}

```python
const schema = {
    "configuration": {
        "name": {
            "type": "keyword"
        },
        "id": {
            "type": "keyword",
            "id": true,
        }
    }
};

await hyperspaceClient.createCollection(collectionName, schema);
```

{% endcode %}
{% endtab %}
{% endtabs %}

**Where** –

* <mark style="color:purple;">schema</mark> – Specifies the python dictionary that outlines the configuration schema.
* '<mark style="color:purple;">collection\_name</mark>' – Specifies the name of the collection to be created in the Hyperspace database.&#x20;

#### **Upload Data**&#x20;

Data can be uploaded in batches. Copy the following code snippet to upload data

{% tabs %}
{% tab title="Python" %}
{% code lineNumbers="true" %}

```python
batch_size = 250
batch = []

for i, data_point in enumerate(documents):
   batch.append(data_point)
   if (i+1) % batch_size == 0:
      response = hyperspace_client.add_batch(batch, collection_name)
      batch.clear()
      
if batch:
  response = hyperspace_client.add_batch(batch, collection_name)
  
hyperspace_client.commit(collection_name)
```

{% endcode %}
{% endtab %}

{% tab title="Java" %}
{% code lineNumbers="true" %}

```java
import java.util.ArrayList;
final int batchSize = 250;

for (int i= 0; index < documents.size(); i++) {
    batch.add(documents.get(i));
    if ((i+ 1) % batchSize == 0) {
          List<DataPoint> batchCopy = new ArrayList<>(batch);
          futures.add(hyperspaceClient.addBatch(batchCopy, collectionName));
          batch.clear();
      }    
}

if (!batch.isEmpty()) {
    futures.add(hyperspaceClient.addBatch(new ArrayList<>(batch), collectionName));
}
CompletableFuture.allOf(futures.toArray(new CompletableFuture[0])).join();
hyperspaceClient.commit(collectionName).join();
```

{% endcode %}
{% endtab %}

{% tab title="JavaScript" %}
{% code lineNumbers="true" %}

```javascript
let BATCH_SIZE = 250;
let batch: any[] = [];
let collectionName = "new_collection";

for (const [i, document] of documents.entries()) {
    batch.push(document);
    if ((i + 1) % BATCH_SIZE == 0) {
        await client.addBatch(collectionName, batch);
        batch = [];
    }
}

if (batch.length != 0) {
    await client.addBatch(collectionName, batch);
}
await client.commit(collectionName)
```

{% endcode %}
{% endtab %}
{% endtabs %}

**Where** –

* <mark style="color:purple;">data\_point</mark> – Represents the document to upload. Each document must have dictionary like structure with a keys according to the database schema configuration file.
* <mark style="color:purple;">batch\_size</mark> – Specifies the number of documents in a batch.
* `commit` is required for vector search only

#### **Build and run a query (Python only)**

Hyperspace queries can be of one of the following types  –

* **Lexical Search**
* **Vector Search**
* **Hybrid Search**&#x20;

Lexical search can be performed in DSL syntax, or as using a [score function](https://docs.hyper-space.io/hyperspace-docs/projects/score-function-commands) of the following form:

{% code lineNumbers="true" %}

```python
 def score_function (params , doc) :
     score = 0.0
     if match ('metadata field 1'):
       score = 1.0
       if match ('metadata field 1'):
          score 2.0
 return score
```

{% endcode %}

#### **To set a hybrid or lexical search query –**

Specify that this score function file is to be used for the Search, as follows –

{% tabs %}
{% tab title="Python" %}
{% code lineNumbers="true" %}

```python
hyperspace_client.set_function(score_function_name,
                                collection_name=collection_name,
                                function_name='score_function')
```

{% endcode %}
{% endtab %}

{% tab title="Java" %}
{% code lineNumbers="true" %}

```javascript
String function = Files.readString(Paths.get("score_function.py"));
client.setFunction(collectionName, "score_function", function);
```

{% endcode %}
{% endtab %}

{% tab title="JavaScript" %}
{% code lineNumbers="true" %}

```python
await hyperspaceClient.setFunction(score_function_name,
                                collection_name=collection_name,
                                function_name='score_function')
```

{% endcode %}
{% endtab %}
{% endtabs %}

#### **To run a hybrid or lexical search query  –**

define the query schema and run&#x20;

{% tabs %}
{% tab title="Python" %}
{% code lineNumbers="true" %}

```python
params= {
         "name": "John"
        }
results = hyperspace_client.search(params,
                                   size=10,                 
                                   collection_name=collection_name
                                   function_name='score_function')
```

{% endcode %}
{% endtab %}

{% tab title="Java" %}
{% code lineNumbers="true" %}

```java
JsonObject params = new JsonObject();
params.add("name", new JsonPrimitive("John"));
JsonObject query = new JsonObject();
query.add("query", params);

Object response = client.search(collectionName, 10, query, "my_score_function");
```

{% endcode %}
{% endtab %}

{% tab title="JavaScript" %}
{% code lineNumbers="true" %}

```python
const size = 10;
let params= {
    "name": "John"
}
let functionName = 'score_function';
await hyperspaceClient.search(collectionName, size, params, functionName)
```

{% endcode %}
{% endtab %}
{% endtabs %}

`query_body` is the query in DSL syntax. `query_body`  must have a similar structure to the database documents, according to the query schema config file. If query\_body includes fields of type&#x20;

#### **To run a lexical search query in DSL syntax–**

define the query schema and run&#x20;

{% tabs %}
{% tab title="Python" %}
{% code lineNumbers="true" %}

```python
results = hyperspace_client.dsl_search({'params': query_body},
                                   size=10,                 
                                   collection_name=collection_name)
```

{% endcode %}
{% endtab %}

{% tab title="Java" %}
{% code lineNumbers="true" %}

```java
String queryJson =  "{" +
                    "  \"query\": {" +
                    "    \"bool\": {" +
                    "      \"must\": [" +
                    "        {" +
                    "          \"term\":{" +
                    "            \"name\":\"John\"" +
                    "           }" +
                    "        }" +
                    "      ]" +
                    "    }" +
                    "  }" +
                    "}";
JsonObject query = JsonParser.parseString(queryJson).getAsJsonObject();
Object response = hyperspaceClient.dslSearch(collectionName, 10, query));
JsonObject queryResponse = new Gson().toJsonTree(response).getAsJsonObject();
System.out.println(queryResponse);
```

{% endcode %}
{% endtab %}

{% tab title="JavaScript" %}
{% code lineNumbers="true" %}

```javascript
const size = 10;
const query = {
    "query": {
        "bool": {
            "must": [
                {"term": {"name": "John"}}
            ]
        }
    }
}
await hyperspaceClient.search(collectionName, size, query)

```

{% endcode %}
{% endtab %}
{% endtabs %}

`query_body` is the query in DSL syntax.

<mark style="color:purple;">results</mark> is a dictionary with two keys – {'similarity': {}, 'took\_ms': ..}

* <mark style="color:purple;">took\_ms</mark> – is a float value that specifies how long the query took to run, such as 8.73ms
* <mark style="color:purple;">similarity</mark> – Returns a list. Each element of the list represents a matching document. For each document, it specifies the score and the vector\_id that you can use to retrieve the document from the Collection.

Here is an example of what results might look like if they were printed on the screen –

{% code lineNumbers="true" %}

```python
print(results['similarity']) 
```

{% endcode %}

\[{'score: 513.7000122070312, 'vector\_id': '78254'},\
&#x20;{'score: 512.5500126784442, 'vector\_id': '23091'},\
&#x20;{'score: 485.5471220787652, 'vector\_id': '85432'}]

You can retrieve additional document fields in the query, using the "fields" keyword.&#x20;

#### **To run a lexical search query in DSL syntax–**

define the query schema and run&#x20;

{% tabs %}
{% tab title="Python" %}
{% code lineNumbers="true" %}

```python
query = {
    "query": {
        "bool": {
            "must": [
                {"term": {"name": "John"}}
            ]
        }
    }
}
results = hyperspace_client.search({'params': query_body},
                                   size=10,                 
                                   collection_name=collection_name
                                   function_name='score_function',
                                   fields = ["title", "date"])
```

{% endcode %}
{% endtab %}

{% tab title="Java" %}
{% code lineNumbers="true" %}

```java
String queryJson =  "{" +
                    "  \"query\": {" +
                    "    \"bool\": {" +
                    "      \"must\": [" +
                    "        {" +
                    "          \"term\":{" +
                    "            \"name\":\"John\"" +
                    "           }" +
                    "        }" +
                    "      ]" +
                    "    }" +
                    "  }" +
                    "}";
JsonObject query = JsonParser.parseString(queryJson).getAsJsonObject();
Object response = client.dslSearch(collectionName, 10, query));
```

{% endcode %}
{% endtab %}

{% tab title="JavaScript" %}
{% code lineNumbers="true" %}

```javascript
const size = 10;
const query = {
    "query": {
        "bool": {
            "must": [
                {"term": {"name": "John"}}
            ]
        }
    }
}
await hyperspaceClient.dslSearch(collectionName, size, query,
                                    fields = ["title", "date"])
```

{% endcode %}
{% endtab %}
{% endtabs %}

`query_body` is the query in DSL syntax.

In this scenario, each entry in <mark style="color:purple;">results\['similarity']</mark> includes a key named "<mark style="color:purple;">fields</mark>",  that includes the fields "<mark style="color:purple;">title</mark>" and "<mark style="color:purple;">date</mark>" per retrieved document.

a more detailed guide is available [here](https://docs.hyper-space.io/hyperspace-docs/projects/setting-up).
