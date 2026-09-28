
## Question and distractors design (problems found in previous uses)


- Si una pregunta cita 3 elementos, por ejemplo "¿Qué afirmación distingue mejor elección del optimizador, regularization y learning rate scheduling como palancas distintas del entrenamiento?"; respuestas que ignoran uno de ellos suelen ser claramente erroneas y muestra de pereza en el diseño del distractor, por ejemplo "Regularization y scheduling son equivalentes; ambos solo cambian el número de épocas."
- Es preferible evitar preguntas que ya den información implícita. Por ejemplo "¿Por qué una excepción personalizada puede ser preferible a una genérica cuando falla una regla de negocio?" implica  ya que sí puede serlo, haciendo que la respuesta "Una excepción personalizada solo añade complejidad a la API si el error ya puede expresarse con un mensaje genérico." sea claramente descartable y, de nuevo, un mal distractor. Es mejor formular preguntas directas y más abiertas. Otra respuesta generada a esa pregunta ha sido "Una excepción genérica basta porque las capas superiores solo necesitan saber que la operación falló, no qué regla del dominio se incumplió." que también es fácilmente descartable por no responder directamente a la pregunta en su estilo de redacción; todos los distractores en este caso deberían como la respuesta correcta empezar por "Porque..." dando una hipótesis que pueda parecer razonable.
- La redacción de un distractor nunca debe negar cualquier elemento lógicamente implícito en la redacción de la pregunta. Por ejemplo ante la pregunta "¿Por qué Python se describe como un lenguaje "híbrido" en lugar de simplemente interpretado o compilado?", un distractor como "Python debe considerarse completamente compilado porque genera bytecode antes de ejecutar, aunque ese bytecode no sea el ejecutable final." es claramente descartable por que ya la pregunta afirma que es híbrido, por lo que no puede ser completamente compilado. Del mismo modo, la pregunta "¿Por qué la definición def configure(debug=True, verbose, output_file): genera un error de sintaxis?" no puede tener un distractor como "No hay error; esta definición es válida porque los valores por defecto se pueden colocar en cualquier lugar.!." porque la pregunta ya afirma que genera un error de sintaxis, por lo que no puede ser válida. En general, los distractores no pueden contradecir la información dada en la pregunta, aunque sí pueden ignorarla o no responder directamente a ella.
- Las preguntas tienen que ser autocontenidas, no hacer referencia al material implícita o explícitamente. Pueden ser todo lo largas que sea necesario.
- nunca usar expresiones como "y confiar en que..."; en el ámbito tecnológico es claro que las cosas se hacen de uno u otro modo, pero no se basan normalmente en confiar en que algo salga como esperas.
- Evitar adjetivos que claramente tienen connotación negativa indicando abiertamente una tipica descripción de algo que está mal, como "enorme" o "confuso"?
- Evitar distractores infantiles como 'VS Code no puede ser un IDE real porque no es un "verdadero IDE" como PyCharm.'
- Los distractores deben ser manifiestamente erroreos, pese a disimularlo. Nunca ser una opción menos correcta que otra.
- Es necesario mejorar el estilo de la redacción. Si bien la dificultad conceptual es importante, también lo es la claridad, si un estilo recargado o innecesariamente formal y complejo.
- Evitar preguntar sobre varios conceptos a la vez si no hay ninguna relación entre ellos relacionada con aquello que se pregunta, como "¿Qué combinación describe mejor cómo kernel size, stride, padding y pooling afectan la salida espacial de una CNN?". Además, esta pregunta rompe la idea de no usar graduaciones como "mejor".
- Hay un claro abuso de formulaciones como "¿Qué comparación describe mejor..."; de nuevo con graduación. Debe evitarse en favor de un estilo más directo.
- Evita preguntas que ya den información en el propio enunciado como "Una noticia puede etiquetarse simultáneamente como "economía", "energía" y "política internacional". ¿Por qué esta tarea encaja mejor con multilabel classification que con multiclass classification?"; es mejor preguntar "Qué tipo de problema de IA lo explica mejor y por qué", no informando así por adelantado que ya es, indeed, multilabel classification.
- Evitar respuestas que contradigan lógicamente el enunciado de la pregunta, como "El random forest ofrece una interpretabilidad muy superior a la de un árbol de decisión individual..." ante la pregunta "¿Por qué un random forest puede ser más preciso que un single decision tree y, al mismo tiempo, menos interpretable?". Todos los distractores TIENEN que ser una respuesta lógicamente plausible de la pregunta, si bien introduciendo errores categoricos o de razonamiento, pero no contradiciendo la información dada en la pregunta ni enunciando algo que no sea una respuesta a la pregunta.
- Evita redactar preguntas que incluyan información en el propio enunciado como "¿Por qué logistic regression se considera un modelo de clasificación aunque su nombre contenga la palabra regression?"; es mejor preguntar "¿Qué tipo de modelo de IA es logistic regression y por qué?".
- Evitar preguntar sobre varios conceptos a la vez si no hay ninguna relación entre ellos relacionada con aquello que se pregunta, como "¿Qué combinación describe mejor cómo kernel size, stride, padding y pooling afectan la salida espacial de una CNN?". Además, esta pregunta rompe la idea de no usar graduaciones como "mejor". Otro ejemplo es "¿Por qué dataloaders, mini-batches y device consistency importan en el entrenamiento práctico de redes neuronales?". Si el objetivo de la pregunta no tiene que ver con la relación entre los conceptos, no deben preguntarse juntos sino subdividir en distintas preguntas.
- Hay un claro abuso de formulaciones como "¿Qué comparación describe mejor..."; de nuevo con graduación. Debe evitarse en favor de un estilo más directo.
- Si una pregunta empieza por "Por qué", es esperable que las respuestas empiecen por "Porque".

---

## Patrones de fallo adicionales identificados en la revisión SAA25 (2025-06)

### 1. Random Syllabus Noise (ruido aleatorio del temario)

El error más frecuente y más dañino. El distractor introduce conceptos de un tema completamente diferente al de la pregunta, sin ninguna conexión plausible. Ejemplos observados:

- Una pregunta sobre la ecuación de Bellman tenía un distractor que mencionaba "la primera componente principal de PCA calculada sobre la matriz de covarianza de las acciones".
- Una pregunta sobre epsilon-greedy tenía un distractor sobre "la derivada de la función de activación sigmoide en la capa final".
- Una pregunta sobre Q-learning tenía un distractor sobre "una proyección ortogonal PCA de los estados de entrada".

Este tipo de distractor es fácilmente descartable por cualquier estudiante que haya leído el enunciado. No confunde: descarta. El distractor debe ser **plausible en el contexto de la pregunta**, no plausible en abstracto. Un distractor sobre PCA en una pregunta de Q-learning no engaña a nadie que haya leído la pregunta.

**Regla:** Todos los distractores deben pertenecer conceptualmente al mismo dominio que la pregunta. Si la pregunta es sobre Q-learning, los distractores deben introducir errores sobre Q-learning, no sobre PCA o CNNs.

### 2. Length Asymmetry (asimetría de longitud)

Cuando la respuesta correcta es notablemente más larga y detallada que los distractores, los estudiantes pueden identificarla por su mayor extensión, no por su corrección. Este es un heurístico conocido de los tests de opción múltiple.

**Regla:** Todos los distractores deben tener una longitud similar a la respuesta correcta (±30% de palabras aproximadamente). Si la respuesta correcta se acorta, los distractores también deben acortarse; si se alarga, lo mismo.

### 3. Feedback Mismatch (feedback inconsistente con el distractor)

Se observaron casos en que el texto del feedback de una respuesta incorrecta describía un error diferente al que cometía el distractor. Por ejemplo, el distractor afirmaba una cosa y el feedback la explicaba como si afirmase otra. Esto ocurre cuando se reciclan feedbacks de versiones anteriores del distractor.

**Regla:** El feedback debe responder exactamente al error que comete el distractor, no a un error genérico del tema. En particular, debe:
1. Indicar explícitamente por qué ese distractor específico es incorrecto.
2. Hacer referencia al contenido concreto del distractor.
3. No contradecir ninguna afirmación del distractor que sea correcta (el feedback solo debe aclarar la parte incorrecta).

### 4. Absurdity (distractores absurdos o infantiles)

Distractores que son obviamente falsos para cualquier persona con conocimientos mínimos del tema, incluso sin haber estudiado el curso. Ejemplos:

- "El algoritmo es equivalente a una regresión lineal clásica ajustada con mínimos cuadrados."
- "El agente realiza una proyección ortogonal PCA de los estados de entrada."
- "Se calcula el producto escalar de las características del nodo hoja con respecto a la desviación estándar."

Estos distractores fallan porque mezclan términos técnicos de forma aleatoria sin coherencia semántica. Un buen distractor introduce un **error categórico específico** (invertir roles, confundir métricas similares, atribuir propiedades de un algoritmo a otro), no una frase sin sentido.

**Regla:** Antes de añadir un distractor, comprobar que un estudiante de nivel medio podría razonablemente confundirlo con la respuesta correcta si no domina el concepto concreto. Si es obvio que es falso a simple vista, hay que rediseñarlo.