# mybudget

Petit outil en ligne de commande pour suivre ses dépenses et revenus.

## Installation

```
pip install -e .
```

## Utilisation

### Ajouter une transaction

```
python -m mybudget add --amount 50 --description "Courses Leclerc" --type expense --category alimentation --date 2026-01-10
python -m mybudget add --amount 1500 --description "Salaire" --type income --date 2026-01-01
```

### Lister les transactions

```
python -m mybudget list
python -m mybudget list --category alimentation
python -m mybudget list --from 2026-01-01 --to 2026-01-31
```

### Définir un budget par catégorie

```
python -m mybudget budget-set --category alimentation --amount 300 --month 1 --year 2026
```

### Consulter l'état d'un budget

```
python -m mybudget budget-status --category alimentation --month 1 --year 2026
```

Exemple de sortie :

```
Category: alimentation
Budget: 300
Spent: 80
Remaining: 220
Consumed: 26.7%
```

## Tests

```
pytest
```

Avec couverture :

```
pytest --cov=mybudget --cov-report=term-missing
```

## Scénarios BDD

Les scénarios BDD se trouvent dans `tests/bdd/` et couvrent les features supplémentaires :

**Modification de transaction** (`tests/bdd/test_modification_transaction.py`)
- Modifier le montant d'une transaction existante
- Modifier la description d'une transaction existante

**Suppression de transaction** (`tests/bdd/test_suppression_transaction.py`)
- Supprimer une transaction et vérifier qu'elle disparaît de la liste

**Filtre par type** (`tests/bdd/test_filtre_par_type.py`)
- Filtrer les transactions pour n'afficher que les dépenses

**Export CSV** (`tests/bdd/test_export_csv.py`)
- Exporter les transactions en CSV avec en-tête et données complètes
