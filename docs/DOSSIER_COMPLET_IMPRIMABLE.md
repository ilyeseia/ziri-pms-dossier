# DOSSIER COMPLET ZIRI.PMS — VERSION IMPRIMABLE
## Pour réunion propriétaire / directeur d’hôtel en Algérie

---

## 1. PRÉSENTATION GÉNÉRALE
**ZIRI.PMS v2.6.5** — Property Management System open-source, base Frappe Framework, interface React SPA.
**Localisation Algérie** : DZD, RC, NIS, AI, NIF, TVA, taxe de séjour.
**Langues** : Français (interface), Arabe (interface), Anglais (technique).

---

## 2. AUDIT TECHNIQUE — RÉSUMÉ
| Composant | Version / État | Preuve |
|---|---|---|
| Projet | 2.6.5 | `kamra/__init__.py` |
| Framework | Frappe v15+ | `hooks.py` |
| Apps installées | Kamra, Smart Access, payments | `modules.txt` |
| DocTypes noyau | 50+ | `kamra/doctype/*` |
| Frontend routes | `/ziri`, `/ziri/pos`, `/ziri/hk`, `/ziri/tape-chart`, `/book` | `frontend/src/screens/` |

**Statuts maturité** : A=Implémenté vérifié, B=Partiel, F=Dépendant équipement

---

## 3. INVENTAIRE DES 13 SERVICES HÔTELIERS

| N° | Service | Module | Statut |
|---|---|---|---|
| 1 | Direction & Admin | Kamra Core | A |
| 2 | Réception | Front Office | A |
| 3 | Réservations | Booking Engine | A |
| 4 | Hébergement | Room Mgmt | A |
| 5 | Revenue Mgmt | Pricing Engine | A |
| 6 | Caisse & Facturation | Finance | A |
| 7 | Service des étages | Housekeeping | A |
| 8 | Restauration / POS | F&B / POS | A |
| 9 | Banquets & Événements | Banquet | A |
| 10 | Maintenance | Technical | A |
| 11 | RH & Pointage | HR Basic | B |
| 12 | Smart Access | Smart Access | B / F |
| 13 | Stocks & Achats | Inventory | A |

**11 opérationnels, 2 partiels, 1 dépendant équipement externe**

---

## 4. POINTS DE VENTE — CAPACITÉS
- Multi-outlet illimité : Restaurant, Bar, Room Service, Spa, Snack
- Transfert chambre temps réel → Folio client
- Gestion tables, menus, ingrédients, stocks
- Sessions caissier, clôture, audit nuit
- Écrans cuisine (KDS) supportés

---

## 5. INTERFACES UTILISATEURS — 12 VÉRIFIÉES
| Interface | Route | Utilisateur |
|---|---|---|
| Dashboard Direction | `/ziri` | Direction |
| Tape Chart | `/ziri/tape-chart` | Réception |
| CRS Réservations | `/ziri/crs` | Réception |
| Liste Chambres | `/ziri/rooms` | Réception/HK |
| Folio Client | `/ziri/folio/{id}` | Réception/Caisse |
| HK Board | `/ziri/hk` | Gouvernante |
| POS Screen | `/ziri/pos` | Caissier/Serveur |
| Banquet Screen | `/ziri/banquet` | Banquet |
| Smart Lock Dashboard | `/ziri/smart-access` | Réception |
| Public Booking | `/book` | Client |

---

## 6. FICHES TECHNIQUES — POINTS CLÉS
Chaque fiche FT_01 à FT_17 contient : Identification, Métier, Fonctionnalités, Interfaces, Utilisateurs, Permissions, Flux, Procédures, Exceptions, KPI, Dépendances, Limites, Améliorations, Critères acceptation, Questions responsable.

**Exemples limites documentées :**
- FT_11 RH : workflow achats/conges non complet
- FT_12 Pointage : non implémenté, nécessite matériel
- FT_13 Smart Access : API fournisseur non vérifiée

---

## 7. ORGANISATION UTILISATEURS — MATRICE RÔLES

| Fonction | Consult | Créer | Modifier | Valider | Annuler | Exporter |
|---|---|---|---|---|---|---|
| Directeur | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Responsable Finance | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Chef Réception | ✓ | ✓ | ✓ | ✓ | ✓ | |
| Réceptionniste | ✓ | ✓ | ✓ | | | |
| Gouvernante | ✓ | | ✓ | | | |
| Caissier POS | ✓ | ✓ | ✓ | ✓ | ✓ | |
| Responsable Maintenance | ✓ | ✓ | ✓ | ✓ | | |

3 modèles organisationnels : équipe réduite, intermédiaire, complète (effectifs indicatifs).

---

## 8. SCÉNARIOS OPÉRATIONNELS — 7 VÉRIFIÉS
1. **REC-01** Arrivée client avec réservation
2. **REC-02** Départ et clôture séjour
3. **F&B-01** Commande restaurant + transfert chambre
4. **HK-01** Nettoyage et contrôle chambre
5. **MAINT-01** Signalement panne et réparation
6. **FIN-01** Audit de nuit
7. **POS-01** Clôture caisse restaurant

+ 6 scénarios interdépartementaux : parcours client complet, consommation restaurant, panne chambre, clôture journalière, arrivée groupe, perte carte accès.

---

## 9. DOSSIER COMMERCIAL — RÉUNION PROPRIÉTAIRE

### Documents remis
- Questionnaire général hôtel (12 questions)
- Questionnaire par département (8 sections)
- Grille analyse besoins avec priorités P0-P3
- Plan démonstration 60 min (5 modules)
- Modèle compte rendu signé
- Limites et dépendances transparentes

### Prochaines étapes
1. Réponses questionnaires → Grille écarts personnalisée
2. Visite technique sur site → Checklist matériel
3. Proposition commerciale chiffrée
4. Planning déploiement + formation

---

## 10. GLOSSAIRE TRILINGUE — EXTRAIT CLÉ

| Français | Anglais | Arabe |
|---|---|---|
| Réception | Front Desk | الاستقبال |
| Arrivée / Check-in | Check-in | الوصول |
| Départ / Check-out | Check-out | المغادرة |
| Compte client / Folio | Guest Folio | حساب الضيف |
| Point de vente | Point of Sale | نقطة البيع |
| Service des étages | Housekeeping | النظافة |
| État de chambre | Room Status | حالة الغرفة |
| Plan tarifaire | Rate Plan | خطة الأسعار |
| Audit de nuit | Night Audit | تدقيق الليلة |
| Taux occupation | Occupancy Rate | معدل الإشغال |
| ADR | Average Daily Rate | متوسط السعر اليومي |
| RevPAR | Revenue per Available Room | الإيراد للغرفة المتاحة |
| RC / NIS / AI / NIF | Registres légaux | السجلات القانونية |

---

## 11. LIMITES & DÉPENDANCES — RAPPEL
- **Smart Access** : Intégration serrures à valider avec fournisseur (marque, modèle, protocole, API/SDK)
- **Pointage RH** : Non implémenté, étude matériel requise
- **Configuration initiale** : Chambres, tarifs, menus, stocks à saisir
- **Infrastructure** : Serveur, Internet, UPS, imprimantes thermiques, écrans KDS
- **Aucun déploiement production** sans validation expresse propriétaire

---

## 12. CONTACT & SUIVI
- **Accès démo** : http://172.23.0.10:8080 (Tailscale tunnel)
- **Dépôt** : `kamra-pms-algeria` — lecture seule
- **Prochaine livraison** : Proposition commerciale après questionnaire

---

*Document consolidé issu de 48 fichiers Markdown, basé sur audit réel du code source ZIRI.PMS v2.6.5. Aucune fonctionnalité n’est inventée. Tous les statuts A/B/F sont justifiés par des chemins de fichiers, DocTypes ou routes vérifiés.*