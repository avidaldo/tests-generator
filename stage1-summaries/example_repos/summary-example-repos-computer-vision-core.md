<!-- markdownlint-disable MD025 -->

# File Inventory

| # | File | Type | Relevant |
| --- | --- | --- | --- |
| 1 | README.md | `.md` | ✅ |
| 2 | vectors_and_embeddings.ipynb | `.ipynb` | ✅ |
| 3 | chromadb_intro.ipynb | `.ipynb` | ✅ |
| 4 | face_recognition_pipeline.ipynb | `.ipynb` | ✅ |

# Content

## [Source: README.md]

The README defines the repository as a computer-vision module with three intentionally separable areas:

- OpenCV foundations,
- YOLO object detection,
- embeddings, vector databases, and recognition.

This Stage 1 unit covers the third area, which the README presents as the conceptual path from vector representations to a face-authentication prototype. The suggested project at the end of the README is especially important: it turns the notebooks into a coherent application idea rather than a set of isolated demonstrations.

The proposed workflow is:

1. capture faces,
2. detect and crop them,
3. embed them with CLIP,
4. store them in ChromaDB,
5. verify identity through similarity search with a threshold.

## [Source: vectors_and_embeddings.ipynb]

This notebook builds the conceptual foundation for everything that follows.

It starts by contrasting object detection with embedding-based questions. Bounding boxes answer what is present and where, but not whether two images are semantically similar or whether a new face matches a previously seen one.

The notebook then introduces vectors and distance metrics, especially:

- Euclidean distance when magnitude matters,
- cosine similarity when direction matters more than scale.

That distinction is tied directly to embeddings: for semantic identity tasks, a brighter image of the same face should remain close to the original even if pixel magnitudes change.

The notebook then defines embeddings as learned mappings from raw inputs to dense semantic vectors and introduces CLIP as the central model for the rest of the module. Two ideas are emphasized:

- images and text can live in the same semantic space,
- similarity in that space is more useful than raw-pixel comparison for recognition tasks.

It also uses PCA as a visualization bridge and closes by connecting image embeddings to NLP, contextual text embeddings, and retrieval-augmented generation. That makes the notebook broader than face recognition alone: it is really a general introduction to semantic vector spaces.

## [Source: chromadb_intro.ipynb]

The ChromaDB notebook explains why embeddings become practically useful only when we can store and retrieve them by similarity.

It contrasts relational databases with vector databases along the key axis of query type:

- SQL databases excel at exact matching and structured queries,
- vector databases excel at nearest-neighbour retrieval in high-dimensional spaces.

The notebook introduces the core ChromaDB concepts:

- client,
- collection,
- ID,
- embedding,
- document,
- metadata.

It then explains the difference between ephemeral and persistent clients, which is crucial for later application design. In-memory collections are fine for teaching and quick experimentation, but authentication or retrieval systems need persistence across sessions.

The similarity-search section is carefully written. It notes that ChromaDB returns distances rather than similarities and explains how cosine distance relates to cosine similarity. It also introduces metadata filtering as a way to constrain the search space before nearest-neighbour lookup.

Finally, the notebook explains the role of HNSW approximate nearest-neighbour indexing. This is one of the strongest engineering sections in the core unit because it connects abstract similarity search to scaling behavior and metric choice.

## [Source: face_recognition_pipeline.ipynb]

This notebook turns the previous two ideas into a complete application pipeline.

Its architecture is explicit:

1. capture an image,
2. detect a face with YOLO,
3. convert the face crop into a CLIP embedding,
4. store that embedding with metadata,
5. verify identity by querying nearest neighbours and thresholding similarity.

Several implementation details are highlighted because they materially affect correctness:

- padding around detected boxes helps preserve useful facial context,
- BGR-to-RGB conversion is required when moving from OpenCV to PIL/CLIP,
- L2 normalization of embeddings is required so cosine-based lookup behaves properly,
- threshold choice trades false rejection against false acceptance.

The notebook also distinguishes enrollment from verification, which is important because they use the same primitives but in different phases of an authentication workflow.

One of the strongest parts of the notebook is the mapping from notebook steps to a fuller project implementation. That reinforces the idea that the notebook is not a toy detour, but a compressed version of a production-shaped pipeline.

# Cross-References

## Conceptual progression across the unit

- The README's proposed face-authentication project is exactly the composition of the three notebooks: embeddings define the representation, ChromaDB defines the retrieval layer, and the face-recognition notebook composes them into an end-to-end workflow. [Source: README.md; Source: vectors_and_embeddings.ipynb; Source: chromadb_intro.ipynb; Source: face_recognition_pipeline.ipynb]
- The embeddings notebook explains why cosine-style semantic proximity matters; the ChromaDB notebook explains how to store and search by that proximity; the face-recognition notebook then uses both to make an authentication decision. [Source: vectors_and_embeddings.ipynb; Source: chromadb_intro.ipynb; Source: face_recognition_pipeline.ipynb]
- The face pipeline depends on the earlier notebook distinction between representation and retrieval: without a meaningful embedding space there is nothing useful to index, and without a vector database there is no scalable verification step. [Source: vectors_and_embeddings.ipynb; Source: chromadb_intro.ipynb; Source: face_recognition_pipeline.ipynb]

## Engineering choices and constraints

- The choice of cosine-oriented similarity in the embeddings notebook is carried through the ChromaDB notebook's distance discussion and then into the face-verification thresholding logic. [Source: vectors_and_embeddings.ipynb; Source: chromadb_intro.ipynb; Source: face_recognition_pipeline.ipynb]
- The ChromaDB notebook's contrast between ephemeral and persistent clients becomes operationally important in the face-recognition notebook, because enrolled identities must survive between sessions in any realistic system. [Source: chromadb_intro.ipynb; Source: face_recognition_pipeline.ipynb]
- The README's suggested project extensions, such as multiple enrollment captures and quality checks, are natural responses to the limitations the face-recognition notebook already surfaces around thresholds, crop quality, and deployment reliability. [Source: README.md; Source: face_recognition_pipeline.ipynb]

## Decision criteria and trade-offs

- Use embeddings instead of raw-pixel comparison when semantic identity matters more than exact appearance. The module repeatedly argues that robustness to lighting, pose, and context is the real reason to move into vector space. [Source: vectors_and_embeddings.ipynb]
- Use a vector database rather than ad hoc linear search when the retrieval problem is fundamentally nearest-neighbour search over many embeddings or when persistence and metadata filtering matter. [Source: chromadb_intro.ipynb]
- Treat the verification threshold as a policy decision, not a fixed truth: raising it improves security but increases false rejections, while lowering it improves convenience but increases spoof risk. [Source: face_recognition_pipeline.ipynb]
- Treat the gap between notebook prototype and deployment as mostly reliability engineering rather than algorithmic novelty. The README makes that explicit, and the face-recognition notebook's project mapping supports it. [Source: README.md; Source: face_recognition_pipeline.ipynb]
