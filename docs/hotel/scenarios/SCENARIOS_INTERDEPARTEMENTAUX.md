# SCÉNARIOS INTERDÉPARTEMENTAUX — ZIRI.PMS

## Scénario 1 : Parcours complet d’un client
**Départements :** Réservations → Réception → Hébergement → Service des étages → Caisse
**Interfaces :** Booking, Tape Chart, Folio
**Preuve :** Flux documenté via DocTypes Reservation → Check In → Folio

## Scénario 2 : Consommation au restaurant
**Départements :** Restauration → Caisse → Réception
**Interfaces :** POS Screen → Folio
**Preuve :** POS Order lié au Folio

## Scénario 3 : Panne dans une chambre
**Départements :** Réception → Maintenance → Service des étages
**Interfaces :** Service Ticket → Room Status
**Preuve :** DocType maintenance et Room

## Scénario 4 : Clôture journalière
**Départements :** Réception → Caisse → Finance
**Interfaces :** Audit de nuit, Cashier Session
**Preuve :** Night Audit Run
