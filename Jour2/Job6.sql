SELECT CONCAT('La capacité de toutes les salles est de : ', SUM(capacite)) 
AS resultat
FROM salles;
