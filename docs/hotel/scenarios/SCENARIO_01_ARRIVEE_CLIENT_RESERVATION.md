# SCÉNARIO OPÉRATIONNEL — Arrivée d’un client avec réservation

## Code : REC-01
## Service : Réception

### Objectif métier
Enregistrer le client et lui attribuer une chambre.

### Préconditions
Réservation confirmée dans le système.

### Étapes
1. Ouvrir Tape Chart et identifier l’arrivée.
2. Vérifier l’identité du client.
3. Valider l’affectation de chambre.
4. Générer la carte d’accès si disponible.
5. Remettre les clés et informations.

### Statut réel dans Ziri.PMS
Opérationnel. DocTypes Reservation, Check In vérifiés.

### Preuve technique
`kamra/doctype/reservation/reservation.py`
`frontend/src/screens/TapeChart.tsx`
