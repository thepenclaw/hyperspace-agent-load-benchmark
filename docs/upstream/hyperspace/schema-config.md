# Creating a Database Schema Configuration File

The local Hyperspace Client uses a database configuration schema (can be provided as a Python dictionary or as a file, for example, named 'schema.json') to define the Collection to be created (as described in the next step). Similar to other search databases, the Hyperspace database leverages this file to outline the data scheme and required customized settings.

The database configuration schema consists of a dictionary containing key-value pairs that lay out the structure (data schema fields) of the data to be uploaded into a Collection. Defined in standard .json format, the configuration is provided under the dict key 'configuration' in the form {'configuration': {'fieldname1': type}, {'fieldname2': type}, ...}. Each attribute (field) is described by an attribute name (such as city, country, and street), key (attribute of the value, such as type and low\_cardinality), and value (property, such as keyword, boolean, and true).

**Create a data schema document as a local variable –**

The data schema should be provided as .json file, or as a python dictionary with the following structure:

{% tabs %}
{% tab title="Python" %}
{% code lineNumbers="true" %}

```python
configuration_schema = {
                        'configuration': { 
                        'Metadata key1': {'type': 'keyword'},
                        'Metadata key2': {'type': 'int'},
                        'Metadata key3': {'type': 'float',
                                          'struct_type': 'list'},
                        'vector1': {
                                    'type': 'dense_vector',
                                    'index_type': 'index type',
                                    'dim': dimension
                                   },
                        'vector2':{
                                   'type': 'dense_vector',
                                   'index_type': 'index type',
                                   'dim': dimension,
                                   }
                       }  
```

{% endcode %}
{% endtab %}

{% tab title="Java" %}
{% code lineNumbers="true" %}

```java
String configuration_schema = "{ " + 
             " \"configuration\": { " + 
             " \"Metadata key1\": {\"type\": \"keyword\"}, " + 
             " \"Metadata key2\": {\"type\": \"int\"}, " + 
             " \"Metadata key3\": {\"type\": \"float\", " + 
                               " \"struct_type\": \"list\"}, " + 
             " \"vector1\": { " + 
                         " \"type\": \"dense_vector\", " + 
                         " \"index_type\": \"index type\", " + 
                         " \"dim\": dimension " + 
                        },
             " \"vector2\":{ " + 
                        " \"type\": \"dense_vector\", " + 
                        " \"index_type\": \"index type\", " + 
                        " \"dim\": dimension, " + 
                        "} " + 
            " }";
```

{% endcode %}
{% endtab %}

{% tab title="JavaScript" %}

<pre class="language-javascript" data-line-numbers><code class="lang-javascript"><strong>const configuration_schema = {
</strong>             'configuration': { 
             'Metadata key1': {'type': 'keyword'},
             'Metadata key2': {'type': 'int'},
             'Metadata key3': {'type': 'float',
                               'struct_type': 'list'},
             'vector1': {
                         'type': 'dense_vector',
                         'index_type': 'index type',
                         'dim': dimension
                        },
             'vector2':{
                        'type': 'dense_vector',
                        'index_type': 'index type',
                        'dim': dimension,
                        }
            };
</code></pre>

{% endtab %}
{% endtabs %}

Vector fields should be given the type "<mark style="color:purple;">dense\_vector</mark>", while metadata fields can be given any type from the [supported data types list.](https://docs.hyper-space.io/hyperspace-docs/~/changes/uCQNjcW7J3OXknfYJaVa/projects/managing-data-collections/supported-data-types)

{% hint style="info" %}
Hyperspace does not currently support signed integers.
{% endhint %}

## **Optional Fields**

The following optional type attributes can be added –

### **Index**

The key ‘<mark style="color:purple;">index</mark>’ allows to disable the indexing of a field. When set to False, the relevant field will be included in the dataset, but will not be indexed and will not contribute to search results. The default value for ‘index’ is True. See example of usage under ‘<mark style="color:purple;">open\_now</mark>’ in the above example.

### **Struct\_type – List**

Values (non-keyword fields) are configured as scalars by default.

To build a list of the same data type, add the key and value '**struct\_type**': 'list'. For example –

{% code lineNumbers="true" %}

```python
'genres': {
    'struct_type': 'list',
    'type': 'int'
}
```

{% endcode %}

**For example –**

{% code lineNumbers="true" %}

```python
document['genres'] = [0, 1, 0]
```

{% endcode %}

{% hint style="info" %}
Metadata fields of type "keyword" can describe a keyword (str) or lists of keywords (list\[str]), without the need to state type "list".&#x20;

The length of each keyword is limited to 256 characters.
{% endhint %}

### **Nested Objects**

Hyperspace supports the use of nested objects as part of a document. To include nested objects, define the relevant field type as 'nested', and the corresponding sub items under the 'fields' key.

**For example –**

{% tabs %}
{% tab title="Python" %}
{% code lineNumbers="true" %}

```python
config = {
    "configuration": {
            "description": {
                "type": "keyword",
            }
            "paragraphs": {
                "type": "nested",
                "fields": {
                    "text": {
                        "type": "keyword"
                    },
                    "count": {
                        "type": "integer"
                    },
                    "value": {
                        "type": "float"
                    }
                },
        },
    }
}
```

{% endcode %}
{% endtab %}

{% tab title="Java" %}
{% code lineNumbers="true" %}

```java
String configuration_schema = "{"+
                    	 "\"configuration\": {"+
                            "\"description\": {"+
                                "\"type\": \"keyword\","+
                            "}"+
                            "\"paragraphs\": {"+
                                "\"type\": \"nested\","+
                                "\"fields\": {"+
                                    "\"text\": {"+
                                        "\"type\": \"keyword\""+
                                    "},"+
                                    "\"count\": {"+
                                        "\"type\": \"integer\""+
                                    "},"+
                                    "\"value\": {"+
                                        "\"type\": \"float\""+
                                    "}"+
                                "},"+
                        "},"+
                    "}"+
                "}";
```

{% endcode %}
{% endtab %}

{% tab title="JavaScript" %}
{% code lineNumbers="true" %}

```javascript
const config = {
    "configuration": {
            "description": {
                "type": "keyword",
            }
            "paragraphs": {
                "type": "nested",
                "fields": {
                    "text": {
                        "type": "keyword"
                    },
                    "count": {
                        "type": "integer"
                    },
                    "value": {
                        "type": "float"
                    }
                },
        },
    }
}
```

{% endcode %}
{% endtab %}
{% endtabs %}

Vector fields should be given the type "<mark style="color:purple;">dense\_vector</mark>", while metadata fields can be given any type from the [supported data types list.](https://docs.hyper-space.io/hyperspace-docs/~/changes/uCQNjcW7J3OXknfYJaVa/projects/managing-data-collections/supported-data-types)

In the above example, "paragraphs" is a nested object with subfields named "text", "count" and "value".

### **Cardinality**

Cardinality refers to the number of unique values an attribute can have.

Hyperspace provides the option to accelerate search performance by setting one of the following cardinality attributes to true.

To accelerate the search, apply the appropriate cardinality attribute where relevant –

* '<mark style="color:purple;">low\_cardinality</mark>' – Indicates that this attribute has up to 10 possible unique values. It is suitable for fields with a limited set of possible values.
* '<mark style="color:purple;">high\_cardinality</mark>' – Indicates that this attribute has more than 100 possible values. It indicates that this attribute has more than 100 possible unique values, meaning that it has a broader range of distinct possible values.

To accelerate the search, apply the appropriate cardinality attribute where relevant.

**For example –**&#x20;

{% code lineNumbers="true" %}

```python
'vertical': {
    'type': 'keyword', 
    'low_cardinality': true
}
```

{% endcode %}

### **Dense Vector**

The '<mark style="color:purple;">dense\_vector</mark>' value assigned to the '<mark style="color:purple;">type</mark>' attribute instructs Hyperspace to index and map the imported data to be suitable for a Vector Search.

**Note** – Currently, '<mark style="color:purple;">dense\_vector</mark>' is the only '<mark style="color:purple;">type</mark>' attribute value that is supported for Vector Search. In the future, an additional option called '<mark style="color:purple;">sparse\_vector</mark>' will be supported.

* **'**<mark style="color:purple;">**type**</mark><mark style="color:purple;">' \[string]</mark> – For vectors, specify '<mark style="color:purple;">dense\_vector</mark>'.
* <mark style="color:purple;">'</mark><mark style="color:purple;">**dim**</mark><mark style="color:purple;">' \[integer]</mark> – Specifies the dimension of the vector, which indicates the number of values that the vector will contain. This is essential storage and search optimization in the database in order to enable efficient and accurate handling of vector operations. For binary vectors, this number must be divisible by 8.\
  **Note** – 'index\_type' and 'dim' must always be provided together or not at all, and they cannot be used in combination with '<mark style="color:purple;">struct\_type</mark>', '<mark style="color:purple;">low\_cardinality</mark>', or '<mark style="color:purple;">high\_cardinality</mark>'.
* <mark style="color:purple;">'</mark><mark style="color:purple;">**index\_type**</mark><mark style="color:purple;">' \[string]</mark> – Specifies the indexing method (data distribution) to be used for this vector, which influences both the speed of operations performed on the vector and their accuracy. Choosing the highest speed may necessitate a minor trade-off in accuracy. This choice also impacts the types of mathematical operations that can be conducted.
  * <mark style="color:purple;">**'brute\_force'**</mark> – KNN using brute force, which is accurate yet time-consuming.
  * <mark style="color:purple;">'</mark><mark style="color:purple;">**hnsw**</mark><mark style="color:purple;">'</mark> – Indexing by Hierarchical Navigable Small World method.
  * <mark style="color:purple;">'</mark><mark style="color:purple;">**ivf**</mark><mark style="color:purple;">'</mark> – Indexing by Inverted File Index scheme.
  * <mark style="color:purple;">'</mark><mark style="color:purple;">**bin\_ivf**</mark><mark style="color:purple;">'</mark> – Indexing by Inverted File Index scheme for binary vectors.

{% code lineNumbers="true" %}

```
{
  'xyz': {
  'type': 'dense_vector',   
  'index_type': 'hnsw',
  'dim': 768,
  'metric': 'ip' 
   }
}
```

{% endcode %}

* <mark style="color:purple;">'</mark><mark style="color:purple;">**metric**</mark><mark style="color:purple;">'</mark> – Specifies the metric to be employed to calculate the similarity (or distance) between vectors as one of the following options –

  * <mark style="color:purple;">**'ip'**</mark> – Inner Product / Cosine Similarity – This option must be specified when the <mark style="color:purple;">'</mark><mark style="color:purple;">**hnsw**</mark><mark style="color:purple;">'</mark> or the <mark style="color:purple;">'</mark><mark style="color:purple;">**ivf**</mark><mark style="color:purple;">'</mark> 'index\_type' (described above) is selected.
  * <mark style="color:purple;">'</mark><mark style="color:purple;">**hamming**</mark><mark style="color:purple;">'</mark> – Hamming Distance – This option must be specified when the <mark style="color:purple;">'</mark><mark style="color:purple;">**bin\_ivf**</mark><mark style="color:purple;">' '</mark><mark style="color:purple;">**index\_type**</mark><mark style="color:purple;">'</mark> (described above) is selected.

  See additional info [here](https://docs.hyper-space.io/hyperspace-docs/projects/setting-up/creating-a-database-schema-configuration-file/vector-search-metrics).
* <mark style="color:purple;">'</mark><mark style="color:purple;">**nlist**</mark>' (int, default 128) – Only used for index\_type = ivf or bin\_ivf. This option is used during index creation and represents the number of buckets used during clustering. A larger nlist leads to quicker search with lower accuracy.
* &#x20;<mark style="color:purple;">'</mark><mark style="color:purple;">**m**</mark><mark style="color:purple;">'</mark> (int, default 30): Used exclusively for index\_type = hnsw. It specifies the number of arcs per new element. A higher M value should correspond to datasets with higher intrinsic dimensionality and/or higher recall. This means that if the dataset has more complex features or you want more accurate results, consider using a higher M value.
* <mark style="color:purple;">'</mark><mark style="color:purple;">**ef**</mark><mark style="color:purple;">'</mark> (int, default 16) – Used exclusively for 'index\_type = hnsw'. This represents the dynamic list size for nearest neighbors. A larger ef value results in better accuracy but slower search times. Essentially, by setting a larger ef, you're allowing the algorithm to consider more potential neighbors for a better match, but this comes at the cost of longer processing times. ef must be larger than the number of queried nearest neighbors (NN).
* <mark style="color:purple;">'</mark><mark style="color:purple;">**ef\_construction**</mark><mark style="color:purple;">'</mark> (int, default 360) – Used exclusively for index\_type = hnsw. It is similar to ef, but used for index creation. Though the upload and index creation may require more time, this option provides a more precise search outcome.

## Example Configuration

The following configurations describes a hybrid combination of vector fields (vector1 and vector2) designated for vector search, with various metadata fields (series, genres, etc.), that can be used as part of classic search.

{% code lineNumbers="true" %}

```python
{
  'configuration': { 
             'series': {'type': 'keyword'},
             'genre_ids': {'struct_type': 'list', 
                           'type': 'int', 
                           'low_cardinality': true},
             'text embedding': {'dim': 1024, 
                                   'metric': 'IP', 
                                   'type': 'dense_vector, 
                                   'index_type': 'hnsw'},
             'production_companies': {'type': 'keyword'},
             'production_countries': {'type': 'keyword'},
             'rating': {'type': 'float'},
             'spoken_languages': {'struct_type': 'list', 'type': 'keyword'},
             'title': {'type': 'keyword'}},
             'vector1': {'type': 'dense_vector',
                         'index_type': 'hnsw',
           	         'dim': 768
           	        },
             'vector2':{'type': 'dense_vector',
                                'index_type': 'hnsw',
                                'dim': 768,
                                'm': 15,
                                'ef': 100,
                                'ef_construction': 192
                        }
}  

```

{% endcode %}

The following is a second example file –

{% code lineNumbers="true" %}

```python
{
 'configuration': {
           'city': {'type': 'keyword'},
           'country': {'type': 'keyword'},
           'open_now': {'type': 'boolean', ‘index’: false},
           'zip_code': {'type': 'integer'},
           'street': {'type': 'keyword'},
           'vertical': {'type': 'keyword', 'low_cardinality': true},
           'embedded_name': {
               'type': 'dense_vector',
               'index_type': 'bin_ivf',
               'dim': 768
               "metric_type":"hamming"
           }
       }
}
```

{% endcode %}

The '<mark style="color:purple;">type</mark>' attribute is valid for both Classic and Vector search.

<mark style="color:purple;">struct\_type</mark>, <mark style="color:purple;">low\_cardinality</mark> and <mark style="color:purple;">high\_cardinality</mark> are only valid for <mark style="color:purple;">**Classic Search**</mark>.

<mark style="color:purple;">dense\_vector</mark>, <mark style="color:purple;">index\_type</mark>, <mark style="color:purple;">dim</mark> and <mark style="color:purple;">metric</mark> are only valid for <mark style="color:purple;">**Vector Search**</mark>.

In the example above, the **city**, **country**, **open\_now**, **zip\_code** and **street** attributes are valid for both Classic Search and Vector Search. The **vertical** attribute is only valid for Classic Search. The **embedded\_name**  attribute is only valid for Vector Search.
