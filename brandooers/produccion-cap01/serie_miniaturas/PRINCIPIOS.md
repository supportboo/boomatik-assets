# Miniaturas y banners de SkillUp Brandooers · principios aplicados

Fecha: 29-oct-2026. Serie: «Tu tienda vende más». Certeza de cada fuente: HECHO (lo he visto o leído en la fuente), INFERENCIA (resumen de terceros, no la fuente original).

No se copia ningún recurso de nadie: solo se aplican principios. Todo el texto se compone en HTML y se renderiza con Chrome.

**Figura de la derecha: la mascota de los ojos de Brandooers, no la cara de Marc.** Marc lo pidió el 29-oct y lo repitió («ya te dije de eliminarla»): su cara, ni en foto ni en avatar, no va en portadas, vistas previas, fotos de perfil ni imágenes de Substack. Su avatar solo habla en los vídeos. Por eso las piezas definitivas llevan los renders 3D de la mascota (`assets/mascota_*.jpg`, copiados de `brandooers/public/images`): la de la lupa en el curso «Tu tienda vende más» y la de los dos ojos con luz en las piezas de marca. Las versiones con la foto nueva de Marc recortada (`assets/marc_recorte.png`) están en `con_foto/` y solo se usan si Marc levanta la regla. Las plantillas sirven para las dos opciones: `--foto` en las miniaturas y en los banners.

## Qué dice cada experto

| Experto | Principio | Fuente | Certeza |
|---|---|---|---|
| Sabrina Ramonov (líder de referencia) | Ella recortada sobre un fondo de color, mirando a cámara; 1-3 palabras enormes; un solo bloque de color fuerte (amarillo, negro); a veces una mano señala el texto. | Sus 6 vídeos largos más vistos del inventario (`lideres/ramonov/inventario.csv`): C0ZKtSx8gyA, AP-fOOmm02g, Xl57Pki6ChE, L2CXXmDG-mM, WvsWbgE_kWg, 3HVH2Iuplqo. Miniaturas públicas en `i.ytimg.com`, copia de consulta en `_ref/ramonov_hoja.jpg`. | HECHO |
| MrBeast | El título y la miniatura fijan lo que el espectador espera; si el vídeo no lo cumple, se va. La miniatura es un «componente crítico» del vídeo. Se mide por el CTR. | «How to Succeed in MrBeast Production» (documento interno filtrado en 2024), págs. 5 y 14: https://prog.sijanec.eu/dir/How-To-Succeed-At-MrBeast-Production.pdf | HECHO |
| Paddy Galloway | La miniatura tiene que pasar la «prueba del vistazo»; el texto, corto (cinco o seis palabras como máximo); importa más la psicología del clic que el diseño; enseñar una situación a punto de pasar; hacer varias versiones y elegir. | Resumen de su entrevista «Meet The Godfather of YouTube Strategy»: https://videohighlight.com/v/UHhTKwclHCs | INFERENCIA (resumen automático, no transcripción) |
| Colin and Samir | Una buena miniatura detiene el scroll, cuenta una historia y plantea una pregunta o sugiere una transformación. | Resumen de su episodio sobre el «YouTube Playbook» que devuelve la búsqueda web; la página del episodio (https://pv.suorcd.us/episode/txHeUpCATp) no cargó (HTTP 500). | INFERENCIA |
| Ali Abdaal | Si no se le ocurre una miniatura que intrigue, no hace el vídeo. Estilo: una cara con una emoción clara, contraste, un indicio de la historia y colores poco saturados que transmiten autoridad tranquila. | Buffer: https://buffer.com/resources/youtube-thumbnails/ · Alici.ai: https://alici.ai/blog/ali-abdaal-thumbnail-playbook-2026 | INFERENCIA (terceros) |

## Lo que aplico en las tres miniaturas

1. **Un solo foco a la derecha con una emoción clara, mirando a cámara.** Es la mascota de los ojos con la lupa: está buscando por qué no vende la tienda. Ningún texto la toca. Ramonov y Ali Abdaal ponen ahí su cara; nosotros, por la regla de Marc, ponemos la mascota con la misma función.
2. **Gancho de 2 a 4 palabras, enorme, a la izquierda.** Dentro del límite de Galloway. En el capítulo 1 son cuatro: «¿POR QUÉ NO VENDE?».
3. **Un único color fuerte en la palabra clave.** Es el bloque de color de Ramonov y de la serie aprobada (miniatura 6).
4. **Prueba del vistazo medida.** Cada miniatura se exporta a 168x94 y 320x180 (`pequenas/`) y el gancho tiene que leerse a 168x94.
5. **Promesa que el vídeo cumple.** Es la regla de MrBeast: el capítulo explica los 4 pasos en los que se rompe la venta. La miniatura no promete cifras ni precios.
6. **Serie reconocible.** La insignia «TU TIENDA VENDE MÁS» y «CAPÍTULO N» van siempre arriba a la izquierda, el logo SkillUp Brandooers abajo a la izquierda, el fondo es el oscuro de brandooers.com y la mascota del curso está a la derecha.
7. **Esquina inferior derecha sin texto.** Ahí pone YouTube la duración, y solo tapa el fondo de la imagen.
8. **Varias versiones para elegir.** Galloway pide varias opciones; Marc elige.

## Las tres versiones del capítulo 1

| Versión | Experto que sigue | Qué la distingue |
|---|---|---|
| A (`cap01_miniatura_1280x720.jpg`) | **Sabrina Ramonov**, el líder de referencia | Figura fundida con el fondo de marca y un halo violeta. Gancho en Anton blanco con la palabra clave en un bloque cian. Subtítulo en Caveat subrayado en rosa. Es la más cercana a la miniatura 6, que ya está aprobada. |
| B (`cap01_miniatura_B_1280x720.jpg`) | **Colin and Samir**: contar una historia y plantear una pregunta | Debajo del gancho va la cadena de los 4 pasos (encontrar, entender, comprar, pagar) con un eslabón roto en rosa: se ve dónde «se rompe la venta». |
| C (`cap01_miniatura_C_1280x720.jpg`) | **Ali Abdaal**: autoridad tranquila | Sin bloques de color: gancho en Space Grotesk (la fuente de brandooers.com) con la palabra clave en el degradado cian, violeta y rosa. Imagen menos saturada y mucho aire. |

Todas las versiones cumplen las reglas de MrBeast (la promesa que el vídeo cumple) y de Galloway (la prueba del vistazo y varias opciones).

## Tres niveles: marca, curso y capítulo

El canal es de marca: SkillUp Brandooers, formación en Innovación, Desarrollo y Estrategia (I+D+E). Cada curso es una lista dentro del canal y una temporada del pódcast. Las piezas comparten sistema (fondo, halo, bloques Anton, logo y mascota a la derecha), pero cada nivel dice una cosa distinta:

| Nivel | Qué dice | Piezas | Script |
|---|---|---|---|
| Marca | «SkillUp Brandooers», «Innovación · Desarrollo · Estrategia» y la promesa: formación práctica para hacer crecer tu negocio con innovación, IA y estrategia. Sin nombre de serie ni «capítulo». | Banners de YouTube, Facebook, LinkedIn y Substack; fotos de perfil; portada del pódcast «SkillUp Brandooers · el pódcast» | `banners.py` |
| Curso | «CURSO» o «TEMPORADA N» y el nombre del curso | Portada de la lista de YouTube (1280x720); portada de la temporada del pódcast (3000x3000) | `banners.py --serie "Nombre *clave*" --temporada N`, o se añade el curso a `SERIES` |
| Capítulo | Insignia de la serie, «CAPÍTULO N» y gancho | Miniatura del vídeo (A, B o C) | `miniatura_capitulo.py` |

Que el nivel de marca no lleve el nombre de ninguna serie sigue la regla de MrBeast de no prometer lo que el contenido no es: el canal tendrá muchos cursos.

## Banners y perfiles (mismo sistema)

Usan el mismo fondo, el mismo halo, los mismos bloques Anton (aquí, INNOVACIÓN, DESARROLLO y ESTRATEGIA) y el mismo logo «SkillUp Brandooers», con la mascota de los dos ojos a la derecha. El contenido clave va siempre dentro de la zona segura de cada red; `index.html` la dibuja con un interruptor en cada pieza.

| Pieza | Tamaño | Zona segura | Fuente del tamaño |
|---|---|---|---|
| Banner de YouTube | 2560x1440 (JPG ≤ 6 MB) | 1546x423 centrada | Ayuda de YouTube (banner del canal) |
| Portada de Facebook | 1640x624 | centro 16:9 para móvil; la foto de perfil tapa abajo a la izquierda | Guía de Facebook para portadas de página |
| Portada de LinkedIn (página de empresa) | 1128x191 | se deja libre la izquierda, donde va el logo | Ayuda de LinkedIn |
| Substack · wordmark | 1344x256 (21:4), transparente, versiones con texto oscuro y con texto blanco | entero | moda.app, verificado el 28-ago-2026 (tercero; Substack no publica una tabla oficial) |
| Substack · banner del correo | 1100x220 | entero | mismo |
| Substack · logo | 512x512 (mínimo 256) | se ve en círculo | mismo |
| Foto de perfil | 1080x1080: los ojos de la mascota con un aro fino de marca (en `con_foto/` está la versión con la foto, en fondo oscuro y en claro) | círculo | — |
| Portada del pódcast (marca) y de cada temporada | 3000x3000 (+ comprobación a 200x200) | tiene que leerse a 200 px | Apple Podcasts (mínimo 1400, máximo 3000) |
| Portada de la lista de YouTube de cada curso | 1280x720 | igual que una miniatura | — |
