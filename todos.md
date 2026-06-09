
# TODOs


## Editor Features

- [x] Add a box for notes on each question selected as "Revisar" to allow the reviewer to specify the reason for that status and any specific feedback for the automatic reviewer (Also clarify notation: human reviewer (stage 4) vs automatic reviewer (stage 5); and in fact that stage 5 is a loop with stage 4, since a new human review is still required before marking questions as "Lista").
- [x] Also a way to write notes on other questions that should be created.
- [x] Ver el modo de recuperar la forma de indicar en el feedback de cada pregunta una referencia al material de clase indicando dónde está explicada (esto también es un mecanismo de robustez para evitar alucionaciones y garantizar el rigor)
- [x] botón para añadir notas para anexar un documento de incidencias o futuras especificaciones (como estas mismas)
- [x] para cada pregunta, añadir opción para marcar como correcto-revisado un distractor (y que cambie ligeramente su color), y opción para eliminar todos los no marcados como correctos.
- [x] Identificar cuando la pregunta que se está editando cumple los requisitos básicos de formato (respuesta correcta + 3 distractores). Impedir en caso contrario marcarla como lista (desmarcar el botón y mostrar un mensaje de error indicando qué falta si igualmente se hace click en él).
- [x] Al marcar una pregunta como "Lista" se salta automaticamente a la siguiente, para agilizar el proceso de revisión.

- El botón "Eliminar no marcados" debería solo poder usarse cuando se haya marcado al menos 3 distractores como correctos para evitar dejar una pregunta no válida por error. Además, al eliminar los no marcados, se debería marcar automáticamente la pregunta como "Lista" si cumple los requisitos de formato, para agilizar el proceso de revisión. Quizá el botón debería estar desactivado mientras no se cumplan los requisitos para su uso. Y tal vez esto sería bueno también para "Lista", que solo se pueda marcar como lista si se cumplen los requisitos de formato, en lugar de sacar la ventana de warning después de hacer click en él. ¿Podría el mensaje equivalente al warning aparecer al intentar marcar como "Lista" pero no como una ventana emergente sino como un mensaje temporal sobre él, al estilo de los hints????? de javascript (Revisar si pyQt permite eso)
- feature: "abrir sesión reciente", que guarde las rutas de aquellas que han sido abiertas previamente para poder cambiar entre ellas con más fluidez. En cualquier caso, siempre que se cambia sesión, si la anterior no ha sido guardada, debe guardarse. 
- Bien pensado, en lugar de guardar cada sesión haciendo click, debería guardarse cada cambio directamente en el fichero de persistencia. No veo un motivo para dejarlo en memoria y fijar todo haciendo click. Deberíamos eliminar el botón de guardar y simplemente guardar cada cambio en el momento que se realiza.
- Es necesario crear un sistema de idiomas siguiendo una arquitectura limpia, con un fichero de configuración con todos los strings de la interfaz. Debería existir por lo menos una versión en inglés y otra en castellano.
- Si una pregunta empieza por "Por qué", es esperable que las respuestas empiecen por "Porque".

## General features

- Remove unnecessary customizations as those about development and SDD. They are currently overcomplex and a simple implementation based on this same document (once its structure is also polished) with built-in agents should be enough.
- Modular defininendo en un documento concreto las reglas de diseño de las preguntas (como que todas las preguntas tengan la misma longitud o que no sean ambiguas) para mejor mantenimeinto y escalabilidad del proyecto.
- Mejorar la salida del stage 3 para indicar cuántas preguntas se generaron, todavía suele haber problemas con la exahustividad.
- Crear un prompt que subdivida en 2 exámenes separando las preguntas más parecidas o que puedan dar información para resolver otra.
- Currently a single batch seems to be generated for each topic when using the skill. I want complete coverage of all topics.
- It's important to define a new base category for each new exam, to avoid confusion between questions of different exams







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
- Han aparecido alucionaciones que eno estaban 
