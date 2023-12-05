Qui est le fournisseur de ses données et pourquoi publier les données de bornes de recharge? Grace à la [legislation](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000043475441) c'est devenu une obligation légale.

La reglementation impose de respecter un schema de données précise et de referencer le dataset sur le [site gouvernemental](https://www.data.gouv.fr).

En pratique pour les gestionnaires de point de charge c'est plus avantageux de passer par un intermediaire : une plate-forme d'itinerance où les données sont d'abord consolidées. En France la plate-forme le plus connue est [Girève](https://www.gireve.com/) qui en plus accompagne ses clients dans la mise en place de diverses services lié à l'écosystème de véhicules électrifiés.

Ce modèle de données inclut des champs spécifiques pour assurer la standardisation des données. Des efforts ont été faits pour valider la qualité et l'uniformité de ces données. Voici quelques-uns des critères de cohérence établis :  
* Chaque borne de recharge (notée PDC pour "point de charge") est unique et correspond à une entrée distincte dans la base de données.
* Un PDC est identifié par un identifiant unique, noté 'id_pdc_itinerance'.  
Chaque PDC est rattaché à une seule station de recharge, identifiée par 'id_station_itinerance'.
* Chaque station est associée à une seule localisation géographique, indiquée par le champ 'coordonneesXY'.  
Ces critères permettent de structurer les informations de manière claire et uniforme, assurant ainsi une meilleure gestion et accessibilité des données sur les infrastructures de recharge pour véhicules électriques.