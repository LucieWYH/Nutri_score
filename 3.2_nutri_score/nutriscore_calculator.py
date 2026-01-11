# nutriscore_calculator.py

def calculer_points(valeur, table):
    for seuil, points in table:
        if valeur <= seuil:
            return points
    return table[-1][1]

def calculer_nutriscore(energie_kj, acides_gras, sucres, sodium_mg,
                        proteines, fibres, fruits_legumes):
    """Calcule le Nutri-Score (algorithme officiel simplifié pour aliments solides)."""

    sodium_g = sodium_mg / 1000  # 转换 mg -> g

    # ---- Négatifs ----
    POINTS_ENERGIE = [(335, 0), (670, 1), (1005, 2), (1340, 3), (1675, 4),
                      (2010, 5), (2345, 6), (2680, 7), (3015, 8), (3350, 9), (99999, 10)]
    POINTS_ACIDES = [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4),
                     (6, 5), (7, 6), (8, 7), (9, 8), (10, 9), (99999, 10)]
    POINTS_SUCRES = [(3.4, 0), (6.8, 1), (10, 2), (13.5, 3), (17, 4),
                     (20, 5), (24, 6), (27, 7), (31, 8), (34, 9),
                     (37, 10), (41, 11), (44, 12), (48, 13), (51, 14), (99999, 15)]
    POINTS_SODIUM = [(0.2, 0), (0.4, 1), (0.6, 2), (0.8, 3), (1.0, 4),
                  (1.2, 5), (1.4, 6), (1.6, 7), (1.8, 8), (2.0, 9),
                  (2.2, 10), (2.4, 11), (2.6, 12), (2.8, 13), (3.0, 14),
                  (3.2, 15), (3.4, 16), (3.6, 17), (3.8, 18), (4.0, 19), (99999, 20)]

    pts_neg = (
        calculer_points(energie_kj, POINTS_ENERGIE)
        + calculer_points(acides_gras, POINTS_ACIDES)
        + calculer_points(sucres, POINTS_SUCRES)
        + calculer_points(sodium_g, POINTS_SODIUM)
    )

    # ---- Positifs ----
    POINTS_PROTEINES = [(2.4, 0), (4.8, 1), (7.2, 2), (9.6, 3),
                        (12, 4), (14, 5), (17, 6), (99999, 7)]
    POINTS_FIBRES = [(3.0, 0), (4.1, 1), (5.2, 2), (6.3, 3),
                     (7.4, 4),  (99999, 7)]
    POINTS_FRUITS = [(40, 0), (60, 1), (80, 2), (99999, 5)]

    pts_proteines = calculer_points(proteines, POINTS_PROTEINES)
    pts_fibres = calculer_points(fibres, POINTS_FIBRES)
    pts_fruits = calculer_points(fruits_legumes, POINTS_FRUITS)

    # règle spéciale
    if pts_neg >= 11 and fruits_legumes < 80:
        score_final = pts_neg - (pts_fibres + pts_fruits)
        proteines_comptees = False
    else:
        score_final = pts_neg - (pts_proteines + pts_fibres + pts_fruits)
        proteines_comptees = True

    # 转换成等级
    if score_final <= 0:
        grade = "A"
    elif score_final <= 2:
        grade = "B"
    elif score_final <= 10:
        grade = "C"
    elif score_final <= 18:
        grade = "D"
    else:
        grade = "E"

    return {
        "score": score_final,
        "grade": grade,
        "details": {
            "negatif": pts_neg,
            "proteines": pts_proteines,
            "fibres": pts_fibres,
            "fruits_legumes": pts_fruits,
            "proteines_comptees": proteines_comptees
        }
    }
