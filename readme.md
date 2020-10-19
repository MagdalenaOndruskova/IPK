# Počítačové komunikácie a siete - PROJEKT 1 
## Implementácia serveru na preklad doménových mien
##### **Autor:** Magdaléna Ondrušková <xondru16@stud.fit.vutbr.cz>
##### **Jazyk:** Python
##### **Hodnotenie:** 16/20b

Popis vypracovania:
Vytvorenie serveru za použitia knižnice `socket`. Server podporuje dve operácie: GET a POST. 
Ak server nenájde ani jednu z týchto operácii, vráti `405 Method Not Allowed`. 
Ak sa jedná o operáciu GET zavolá sa funkcia `operation_GET`, ktorá získa požadovaný výsledok. Podopne aj u operácii POST ( funkcia `operation_POST`). 
Obe operácie volajú funkciu `get_result`, ktorá vyhodnotí jednotlivé vstupy. 
Pri operácii POST, ak sa tam nachádza čo i len jeden správny vstup, server pošle naspäť clientovi odpoveď s hlavičkou `HTTP/1.1 200 OK` a so správnym preloženým výstupom. Chybné riadky ignoruje. 
Ak sa nenájde ani jeden správny vstup, funkcia vracia hlavičku `HTTP/1.1 400 Bad Request`. 
Pri stlačení na klávesnici `ctrl + c` je server ukončný, inak beží bez prerušenia stále. 
