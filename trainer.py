from app import chatbot
from chatterbot.trainers import ListTrainer
trainer = ListTrainer(chatbot)
trainer.train([('Los coronavirus son una extensa familia de virus que pueden causar enfermedades tanto en animales como en humanos. En los humanos, se sabe que varios coronavirus causan infecciones respiratorias que pueden ir desde el resfriado común hasta enfermedades más graves como el síndrome respiratorio de Oriente Medio (MERS) y el síndrome respiratorio agudo severo (SRAS). El coronavirus que se ha descubierto más recientemente causa la enfermedad por coronavirus COVID-19.'),
    ('La COVID‑19 es la enfermedad infecciosa causada por el coronavirus que se ha descubierto más recientemente. Tanto este nuevo virus como la enfermedad que provoca eran desconocidos antes de que estallara el brote en Wuhan (China) en diciembre de 2019. Actualmente la COVID‑19 es una pandemia que afecta a muchos países de todo el mundo.'),
    ('Los síntomas más habituales de la COVID-19 son la fiebre, la tos seca y el cansancio. Otros síntomas menos frecuentes que afectan a algunos pacientes son los dolores y molestias, la congestión nasal, el dolor de cabeza, la conjuntivitis, el dolor de garganta, la diarrea, la pérdida del gusto o el olfato y las erupciones cutáneas o cambios de color en los dedos de las manos o los pies. Estos síntomas suelen ser leves y comienzan gradualmente. Algunas de las personas infectadas solo presentan síntomas levísimos.'),
    ('La mayoría de las personas (alrededor del 80%) se recuperan de la enfermedad sin necesidad de tratamiento hospitalario. Alrededor de 1 de cada 5 personas que contraen la COVID‑19 acaba presentando un cuadro grave y experimenta dificultades para respirar. Las personas mayores y las que padecen afecciones médicas previas como hipertensión arterial, problemas cardiacos o pulmonares, diabetes o cáncer tienen más probabilidades de presentar cuadros graves. Sin embargo, cualquier persona puede contraer la COVID‑19 y caer gravemente enferma. Las personas de cualquier edad que tengan fiebre o tos y además respiren con dificultad, sientan dolor u opresión en el pecho o tengan dificultades para hablar o moverse deben solicitar atención médica inmediatamente. Si es posible, se recomienda llamar primero al profesional sanitario o centro médico para que estos remitan al paciente al establecimiento sanitario adecuado.'),
    ('Si tiene síntomas leves, como tos o fiebre leves, generalmente no es necesario que busque atención médica. Quédese en casa, aíslese y vigile sus síntomas. Siga las orientaciones nacionales sobre el autoaislamiento. Sin embargo, si vive en una zona con paludismo (malaria) o dengue, es importante que no ignore la fiebre. Busque ayuda médica. Cuando acuda al centro de salud lleve mascarilla si es posible, manténgase al menos a un metro de distancia de las demás personas y no toque las superficies con las manos. En caso de que el enfermo sea un niño, ayúdelo a seguir este consejo.'),
    ('Busque inmediatamente atención médica si tiene dificultad para respirar o siente dolor o presión en el pecho. Si es posible, llame a su dispensador de atención de la salud con antelación para que pueda dirigirlo hacia el centro de salud adecuado.'),
    ('Una persona puede contraer la COVID‑19 por contacto con otra que esté infectada por el virus. La enfermedad se propaga principalmente de persona a persona a través de las gotículas que salen despedidas de la nariz o la boca de una persona infectada al toser, estornudar o hablar. Estas gotículas son relativamente pesadas, no llegan muy lejos y caen rápidamente al suelo. Una persona puede contraer la COVID‑19 si inhala las gotículas procedentes de una persona infectada por el virus. Por eso es importante mantenerse al menos a un metro de distancia de los demás. Estas gotículas pueden caer sobre los objetos y superficies que rodean a la persona, como mesas, pomos y barandillas, de modo que otras personas pueden infectarse si tocan esos objetos o superficies y luego se tocan los ojos, la nariz o la boca. Por ello es importante lavarse las manos frecuentemente con agua y jabón o con un desinfectante a base de alcohol. '),
    ('La OMS está estudiando las investigaciones en curso sobre las formas de propagación de la COVID‑19 y seguirá informando sobre las conclusiones que se vayan obteniendo.'),
    ('La principal forma de propagación de la COVID‑19 es a través de las gotículas respiratorias expelidas por alguien que tose o que tiene otros síntomas como fiebre o cansancio. Muchas personas con COVID‑19 presentan solo síntomas leves. Esto es particularmente cierto en las primeras etapas de la enfermedad. Es posible contagiarse de alguien que solamente tenga una tos leve y no se sienta enfermo.'),
    ('Según algunas informaciones, las personas sin síntomas pueden transmitir el virus. Aún no se sabe con qué frecuencia ocurre. La OMS está estudiando las investigaciones en curso sobre esta cuestión y seguirá informando sobre las conclusiones que se vayan obteniendo.'),
    ('Practicar la higiene respiratoria y de las manos es importante en TODO momento y la mejor forma de protegerse a sí mismo y a los demás. '),
    ('Cuando sea posible, mantenga al menos un metro de distancia entre usted y los demás. Esto es especialmente importante si está al lado de alguien que esté tosiendo o estornudando. Dado que es posible que algunas personas infectadas aún no presenten síntomas o que sus síntomas sean leves, conviene que mantenga una distancia física con todas las personas si se encuentra en una zona donde circule el virus de la COVID‑19.'),
    ('Si ha estado en contacto estrecho con alguien con COVID‑19, puede estar infectado. '),
    ('Contacto estrecho significa vivir con alguien que tiene la enfermedad o haber estado a menos de un metro de distancia de alguien que tiene la enfermedad. En estos casos, es mejor quedarse en casa.'),
    ('Sin embargo, si usted vive en una zona con paludismo (malaria) o dengue, es importante que no ignore la fiebre. Busque ayuda médica. Cuando acuda al centro de salud lleve mascarilla si es posible, manténgase al menos a un metro de distancia de las demás personas y no toque las superficies con las manos. En caso de que el enfermo sea un niño, ayúdelo a seguir este consejo.'),
    ('Si ha tenido indudablemente COVID‑19 (confirmada mediante una prueba), aíslese durante 14 días incluso después de que los síntomas hayan desaparecido como medida de precaución. Todavía no se sabe exactamente cuánto tiempo las personas siguen siendo contagiosas después de recuperarse. Siga los consejos de las autoridades nacionales sobre el aislamiento.'),
    ('El aislamiento es una medida importante que adoptan las personas con síntomas de COVID‑19 para evitar infectar a otras personas de la comunidad, incluidos sus familiares.'),
    ('El aislamiento se produce cuando una persona que tiene fiebre, tos u otros síntomas de COVID‑19 se queda en casa y no va al trabajo, a la escuela o a lugares públicos. Lo puede hacer voluntariamente o por recomendación de su dispensador de atención de salud. Sin embargo, si vive en una zona con paludismo (malaria) o dengue, es importante que no ignore la fiebre. Busque ayuda médica. Cuando acuda al centro de salud use una mascarilla si es posible, manténgase al menos a un metro de distancia de las demás personas y no toque las superficies con las manos. En caso de que el enfermo sea un niño, ayúdelo a seguir este consejo.'),
    ('Ponerse en cuarentena significa separarse de los demás porque ha estado expuesto a alguien con COVID‑19 aunque usted mismo no tenga síntomas. Durante la cuarentena, debe vigilar su estado para detectar síntomas. El objetivo de la cuarentena es prevenir la transmisión. Dado que las personas que enferman de COVID‑19 pueden infectar a otros inmediatamente, la cuarentena puede evitar que se produzcan algunas infecciones.'),
    ('Sin embargo, si vive en una zona con paludismo (malaria) o dengue, es importante que no ignore la fiebre. Busque ayuda médica. Cuando acuda al centro de salud use una mascarilla si es posible, manténgase al menos a un metro de distancia de las demás personas y no toque las superficies con las manos. En caso de que el enfermo sea un niño, ayúdelo a seguir este consejo. '),
    ('La cuarentena significa restringir las actividades o separar a las personas que no están enfermas pero que pueden haber estado expuestas a la COVID‑19. El objetivo es prevenir la propagación de la enfermedad en el momento en que las personas empiezan a presentar síntomas.'),
    ('El aislamiento significa separar a las personas que están enfermas con síntomas de COVID‑19 y pueden ser contagiosas para prevenir la propagación de la enfermedad.'),
    ('El distanciamiento físico significa estar físicamente separado. La OMS recomienda mantener una distancia de al menos un metro con los demás. Es una medida general que todas las personas deberían adoptar incluso si se encuentran bien y no han tenido una exposición conocida a la COVID‑19.'),
    ('Las investigaciones indican que los niños y los adolescentes tienen las mismas probabilidades de infectarse que cualquier otro grupo de edad y pueden propagar la enfermedad. '),
    ('Las pruebas hasta la fecha sugieren que los niños y los adultos jóvenes tienen menos probabilidades de desarrollar una enfermedad grave, pero con todo se pueden dar casos graves en estos grupos de edad. '),
    ('Los niños y los adultos deben seguir las mismas pautas de cuarentena y aislamiento si existe el riesgo de que hayan estado expuestos o si presentan síntomas. Es particularmente importante que los niños eviten el contacto con personas mayores y con otras personas que corran el riesgo de contraer una enfermedad más grave.'),
    ('Manténgase al día de la información más reciente sobre el brote de COVID‑19, a la que puede acceder en el sitio web de la OMS y a través de las autoridades de salud pública a nivel nacional y local. Se han registrado casos en la mayoría de los países del mundo, y en muchos de ellos se han producido brotes. Las autoridades de algunos países han conseguido ralentizar el avance de los brotes, pero la situación es impredecible y es necesario comprobar con regularidad las noticias más recientes.'),
    ('Lávese las manos a fondo y con frecuencia usando un desinfectante a base de alcohol o con agua y jabón.'),
    ('Lavarse las manos con agua y jabón o con un desinfectante a base de alcohol mata los virus que pueda haber en sus manos.'),
    ('Mantenga una distancia mínima de un metro entre usted y los demás.'),
    ('Cuando alguien tose, estornuda o habla despide por la nariz o la boca unas gotículas de líquido que pueden contener el virus. Si la persona que tose, estornuda o habla tiene la enfermedad y usted está demasiado cerca de ella, puede respirar las gotículas y con ellas el virus de la COVID‑19.'),
    ('Cuando hay aglomeraciones, hay más probabilidades de que entre en contacto estrecho con alguien que tenga COVID‑19 y es más difícil mantener una distancia física de un metro.'),
    ('Las manos tocan muchas superficies y pueden recoger virus. Una vez contaminadas, las manos pueden transferir el virus a los ojos, la nariz o la boca. Desde allí, el virus puede entrar en su cuerpo y causarle la enfermedad.'),
    ('Tanto usted como las personas que lo rodean deben asegurarse de mantener una buena higiene respiratoria. Eso significa cubrirse la boca y la nariz con el codo flexionado o con un pañuelo al toser o estornudar. Deseche de inmediato el pañuelo usado y lávese las manos.'),
    ('Los virus se propagan a través de las gotículas. Al mantener una buena higiene respiratoria protege a las personas que lo rodean de virus como los del resfriado, la gripe y la COVID‑19.'),
    ('Permanezca en casa y aíslese incluso si presenta síntomas leves como tos, dolor de cabeza y fiebre ligera hasta que se recupere. Pida a alguien que le traiga las provisiones. Si tiene que salir de casa, póngase una mascarilla para no infectar a otras personas.'),
    ('Evitar el contacto con otras personas las protegerá de posibles infecciones por el virus de la COVID‑19 u otros.'),
    ('Si tiene fiebre, tos y dificultad para respirar, busque atención médica, pero en la medida de lo posible llame por teléfono con antelación y siga las indicaciones de la autoridad sanitaria local.'),
    ('Las autoridades nacionales y locales dispondrán de la información más actualizada sobre la situación en su zona. Llamar con antelación permitirá que su dispensador de atención de salud le dirija rápidamente hacia el centro de salud adecuado. Esto también lo protegerá a usted y ayudará a prevenir la propagación de virus y otras infecciones.'),
    ('Las autoridades locales y nacionales son los interlocutores más indicados para dar consejos sobre lo que deben hacer las personas de su zona para protegerse.')])
